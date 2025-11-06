import io
import json
import logging
import os
import time
from datetime import timedelta

from changes.code_change_expr import ChangeHierGroup
from changes.entity import Entity
from changes.read_changes_group_info import CodeChangeInput
from changes.run_change_hier_jar import run_jar_analysis
from git_info.git_analyzer import GitUtil, GitDiffAnalyzer
from llm.build_order import EntityOrder
from llm.demo.qwen.use import call_qwen
from llm.input_expr import EntityInput
from concurrent.futures import ThreadPoolExecutor, as_completed
# from llm.demo.openrouter.use import call_llm
from use import call_llm


class AnalysisInput:
    def __init__(self, url, old_revision, new_revision, local_root_save_path, local_analysis_path):
        self.url = url
        self.old_rev = old_revision
        self.new_rev = new_revision
        self.local_root_save_path = local_root_save_path  # 输出根路径
        self.local_analysis_path = local_analysis_path  # 仓库裸克隆地址
        # self.local_root_save_path = 'D:/my/intern/mlccd/changeHierOut/rapid3' # 输出根路径
        # self.local_analysis_path = "D:/my/intern/mlccd/changeHierTemp" # 仓库裸克隆地址


class SemanticChangeAnalyzer:
    _json_change_info_id = 1

    def __init__(self, input_config: AnalysisInput):
        self.config = input_config
        self.git_analyzer = self._create_git_analyzer()
        self.language = self.git_analyzer.language
        self.entity_order = None
        self.code_change_input = None
        self.before_version_hash = self.git_analyzer.resolve_reference(self.config.old_rev)[:8]
        self.after_version_hash = self.git_analyzer.resolve_reference(self.config.new_rev)[:8]
        self.repo_name = input_config.url.split('/')[-1].replace('.git', '')
        self.changes_root_path = (
            f"{self.config.local_root_save_path}/"
            f"{self.repo_name}-{self.before_version_hash}-{self.after_version_hash}"
        )
        self.all_change_entities_info = []

    def _create_git_analyzer(self) -> GitDiffAnalyzer:
        return GitDiffAnalyzer(
            url=self.config.url,
            local_analysis_path=GitUtil.normalize_path(self.config.local_analysis_path),
            old_rev=self.config.old_rev,
            new_rev=self.config.new_rev
        )

    def _prepare_code_change_input(self):

        self.code_change_input = CodeChangeInput(
            root_save_path=self.config.local_root_save_path,
            change_hier_group=ChangeHierGroup(self.language),
            repo_name=self.repo_name,
            before_version=self.before_version_hash,
            after_version=self.after_version_hash,
            changes_root_path=self.changes_root_path,
            language=self.language
        )

        self.code_change_input.url = self.config.local_root_save_path

    def _build_entity_order(self):
        self.code_change_input.read_changes_info()
        self.entity_order = EntityOrder(self.code_change_input)
        self.entity_order.build_entity_map_order()

    def _analyze_single_entity_input(self, entity: Entity):
        entity_input = self.entity_order.entity_input_map[entity]

        ranges = [-1, -1, -1, -1]

        if entity.entity_granularity == 'Function':
            ranges[0] = int(entity.before_begin_line)
            ranges[1] = int(entity.before_end_line)
            ranges[2] = int(entity.after_begin_line)
            ranges[3] = int(entity.after_end_line)

            entity_input.commits = self.git_analyzer.get_commit_messages_for_entity(
                entity.file_name, ranges, entity.entity_name)

            src_codes = self.git_analyzer.get_function_source(entity.file_name, entity.entity_name, ranges)
            entity_input.before_code = src_codes[0]
            entity_input.after_code = src_codes[1]
        else:
            entity_input.commits = self.git_analyzer.get_commit_messages_for_entity(
                entity.file_name, ranges=ranges
            )

        input_str = entity_input.get_input_string()

        if not input_str:
            print(f"Entity {entity.entity_name} has empty prompt")
            input_str = "null"
            # return

        # 保留原始代码中的写文件逻辑（注释状态）
        input_path = os.path.join(entity_input.entity_path, 'input.txt')
        with open(input_path, 'w', encoding='utf-8') as file:
            file.write(input_str)

        print('end========================')

    def _analyze_single_entity_output(self, entity: Entity):
        print(entity.file_name,entity.entity_name)
        entity_input = self.entity_order.entity_input_map[entity]
        input_path = os.path.join(entity_input.entity_path, 'input.txt')
        with open(input_path, 'r', encoding='utf-8') as file:
            input_str = file.read()

        # semantic_str = call_qwen(input_str)
        semantic_str = 'test'
        # semantic_str = call_llm(input_str)
        semantic_path = os.path.join(entity_input.entity_path, "semantic.txt")
        with open(semantic_path, 'w', encoding='utf-8') as file:
            file.write(semantic_str)
        print(semantic_str[:50])

    def _save_entity_change_info_to_json(self, entity: Entity):
        entity_input = self.entity_order.entity_input_map[entity]

        input_path = os.path.join(entity_input.entity_path, 'input.txt')
        semantic_path = os.path.join(entity_input.entity_path, "semantic.txt")

        try:
            with open(input_path, 'r', encoding='utf-8') as file:
                input_str = file.read()
        except FileNotFoundError:
            input_str = ''
            print(f"Tip: Changes file not found at {input_path}")

        try:
            with open(semantic_path, 'r', encoding='utf-8') as file:
                semantic_str = file.read()
        except FileNotFoundError:
            semantic_str = ''
            print(f"Tip: Changes file not found at {semantic_path}")

        entity_info = {
            "id": SemanticChangeAnalyzer._json_change_info_id,
            "entity_name": entity.entity_name,
            "entity_id": entity.entity_id,
            "entity_granularity": entity.entity_granularity,
            "entity_file_name": entity.file_name,
            "entity_parent_id": entity.parent_id,
            "entity_path": entity_input.entity_path,
            "input_string": input_str,
            "semantic_string": semantic_str,
            "before_code": entity_input.before_code,
            "after_code": entity_input.after_code,
        }

        self.all_change_entities_info.append(entity_info)
        SemanticChangeAnalyzer._json_change_info_id += 1

    def check_history(self):
        if not os.path.exists(self.changes_root_path):
            return False
        file_path = os.path.join(self.changes_root_path, 'entities_changes_info.json')

        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            return True
        else:
            return False

    def run_analysis(self):

        start_time = time.time()

        if self.check_history():
            return
        
        print(f"开始分析代码变更 {self.repo_name} ({self.config.old_rev}: {self.before_version_hash} -> "
              f"{self.config.new_rev}: {self.after_version_hash})")
        print(f"项目语言: {self.language}")

        run_jar_analysis(
            local_analysis_path=self.config.local_analysis_path,
            before_version_hash=self.before_version_hash,
            after_version_hash=self.after_version_hash,
            output_dir=self.config.local_root_save_path,
            repo_name=self.repo_name,
            language=self.language
        )



        self._prepare_code_change_input()
        self._build_entity_order()

        print(f"需要分析的变更语义的数量: {len(self.entity_order.order)}")

        with ThreadPoolExecutor(max_workers=10) as executor:  # 根据系统资源调整线程数
            futures = {
                executor.submit(self._analyze_single_entity_input, entity): entity
                for entity in self.entity_order.order
            }

            for i, future in enumerate(as_completed(futures), 1):
                entity = futures[future]
                try:
                    future.result()  # 获取结果（主要是捕获异常）
                    print(f"实体输入分析完成: {i}/{len(self.entity_order.order)}")
                except Exception as e:
                    print(f"实体输入分析失败---: {i}/{len(self.entity_order.order)}")
                    print(f"实体 {entity.entity_name} 分析失败: {str(e)}")
                    print(entity.file_name)


        # 输出分析 - 使用线程池并发生成语义
        print("\n开始并发处理实体输出分析...")
        self._output_counter = 0  # 重置进度计数器

        # 根据模型API的并发限制调整线程数
        # 假设模型API允许最大10个并发请求
        max_concurrent_api_calls = 10
        with ThreadPoolExecutor(max_workers=min(max_concurrent_api_calls, os.cpu_count() * 2)) as executor:
            futures = {executor.submit(self._analyze_single_entity_output, entity): entity
                       for entity in self.entity_order.order}

            for future in as_completed(futures):
                entity = futures[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"实体 {entity.entity_name} 输出分析失败: {str(e)}")

        # i = 1
        # for entity in self.entity_order.order:
        #     print('entity # save: ', i)
        #     self._analyze_single_entity_output(entity)
        #     i += 1

        # i = 1
        # for entity in self.entity_order.order:
        #     # if i < 430:
        #     #     i += 1
        #     #     continue
        #     print(f"entity # input: {i}/{len(self.entity_order.order)}")
        #     # if i == 431:
        #     #     print("fs")
        #     self._analyze_single_entity_input(entity)
        #     i += 1
        #
        # i = 1
        # for entity in self.entity_order.order:
        #     print('entity # out: ', i)
        #     self._analyze_single_entity_output(entity)
        #     i += 1

        i = 1
        for entity in self.entity_order.order:
            print('entity # save: ', i)
            self._save_entity_change_info_to_json(entity)
            i += 1

        with io.open(self.changes_root_path + "/entities_changes_info.json", 'w', encoding='utf-8') as json_file:
            json.dump(self.all_change_entities_info, json_file, indent=4, ensure_ascii=False)

        elapsed = time.time() - start_time
        print(f"\n分析完成! 总耗时: {timedelta(seconds=elapsed)} [时:分:秒]")
        #
        # # 返回分析结果数
        # return len(self.entity_order.order)


if __name__ == '__main__':
    # input_config = AnalysisInput("https://github.com/libuv/libuv.git",
    #                              "v1.44.2",
    #                              "v1.48.0",
    #                              'D:/my/intern/mlccd/changeHierOut/rapid3',
    #                              "D:/my/intern/mlccd/changeHierTemp/libuv.git")
    # analyzer = SemanticChangeAnalyzer(input_config)
    # num_entities = analyzer.run_analysis()

    input_config = AnalysisInput("https://github.com/libuv/libuv.git",
                                 "v1.44.2",
                                 "v1.48.0",
                                 'D:/my/intern/mlccd/changeHierOut/rapid5',
                                 "D:/my/intern/mlccd/changeHierTemp/libuv.git")

    input_config1 = AnalysisInput("https://github.com/google/skia.git",
                                  "20164f3",
                                  "84d9fd6",
                                  'D:/my/intern/mlccd/changeHierOut/rapid1',
                                  "D:/my/intern/repo/skia.git")

    input_config2 = AnalysisInput("https://github.com/google/skia.git",
                                  "chrome/m131",
                                  "chrome/m133",
                                  'D:/my/intern/mlccd/changeHierOut/rapid6',
                                  "D:/my/intern/repo/skia.git")

    input_config3 = AnalysisInput("https://github.com/google/cef.git",
                                  "5735",
                                  "6834",
                                  'D:/my/intern/mlccd/changeHierOut/rapid8',
                                  "D:/my/intern/repo/cef.git")

    input_config4 = AnalysisInput("https://github.com/google/curve.git",
                                  "v0.1.0",
                                  "v0.2.0-beta",
                                  'D:/my/intern/mlccd/changeHierOut/rapid9',
                                  "D:/my/intern/repo/curve.git")

    input_config01 = AnalysisInput("https://github.com/libuv/libuv.git",
                                 "v1.44.2",
                                 "v1.48.0",
                                 'D:/Huawei/new/semarc_backend/results/libuv-v1.44.2v1.48.0/code_changes',
                                 "D:/Huawei/new/semarc_backend/libuv")

    input_config6 = AnalysisInput("https://github.com/GNOME/libxml2.git",
                                  "v2.10.0",
                                  "v2.14.0",
                                  'D:/Huawei/new/semarc_backend/results/libxml2-v2.10.0v2.14.0/code_changes',
                                  "D:/Huawei/new/semarc_backend/libxml2")
    
    analyzer = SemanticChangeAnalyzer(input_config6)
    analyzer.run_analysis()
    
    # print(call_llm("介绍二分法算法python实现"))

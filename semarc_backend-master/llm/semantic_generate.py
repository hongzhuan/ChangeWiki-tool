
import time
from datetime import timedelta
from typing import List

from changes.code_change_expr import ChangeHierGroup
from changes.entity import Entity
from changes.read_changes_group_info import CodeChangeInput
from llm.build_order import EntityOrder
from git_info.git_analyzer import GitUtil, GitDiffAnalyzer
from llm.demo.use import call_qwen


def create_git_analyzer(url, local_analysis_path, old_rev, new_rev) :

    analyzer = GitDiffAnalyzer(
        url=url,
        local_analysis_path=local_analysis_path,
        old_rev=old_rev,
        new_rev=new_rev
    )
    return analyzer


def main():


    url = "https://github.com/libuv/libuv.git"
    local_analysis_path = "D:/my/intern/mlccd/changeHierTemp"
    local_analysis_path = GitUtil.normalize_path(local_analysis_path)
    old_rev = "v1.44.2"
    new_rev = "v1.48.0"
    git_analyzer = create_git_analyzer(url, local_analysis_path, old_rev, new_rev)
    language = git_analyzer.language
    print(language)


    local_root_save_path = 'D:/my/intern/mlccd/changeHierOut/rapid3'
    repo_name = "libuv"
    before_version_hash = git_analyzer.resolve_reference_to_hash(old_rev)
    after_version_hash = git_analyzer.resolve_reference_to_hash(new_rev)
    print(before_version_hash)
    print(after_version_hash)
    changes_root_path = local_root_save_path + '/' + repo_name + '-' + before_version_hash + '-' + after_version_hash

    code_change_input = CodeChangeInput(root_save_path=local_root_save_path,
                                        change_hier_group=ChangeHierGroup(language),
                                        repo_name=repo_name,
                                        before_version=before_version_hash,
                                        after_version=after_version_hash,
                                        changes_root_path=changes_root_path,
                                        language=language)

    code_change_input.url = local_root_save_path


    code_change_input.read_changes_info()
    entity_order = EntityOrder(code_change_input)
    entity_order.build_entity_order()




    # i = 1
    for entity in entity_order.order:
        # print(i)
        print(entity.file_name + "  " + entity.entity_name)
        entity_input = entity_order.entity_input_map[entity]
        if entity.entity_granularity == 'Function':
            entity_input.commits = git_analyzer.get_commit_messages_for_entity(entity.file_name, entity.entity_name)
        else:
            entity_input.commits = git_analyzer.get_commit_messages_for_entity(entity.file_name)

        prompt_str = entity_input.get_input_string()

        if prompt_str == '':
            semantic_str = ''
            print("null")
        else:
            # semantic_str = call_qwen(entity_input.get_input_string())
            semantic_str = 'test analysis'
            print(entity.entity_name + "not null")

        # with open(entity_input.entity_path + "/input.txt", 'w', encoding='utf-8') as file:
        #     file.write(prompt_str)
            # file.write(semantic_str)

        # with open(entity_input.entity_path + "/semantic.txt", 'w', encoding='utf-8') as file:
            # if prompt_str != '':
            #     file.write(prompt_str)
            # file.write(semantic_str)
        print('prompt:' + prompt_str)
        # print('answer: ' + semantic_str)
        # print(i)
        print('ieni---------------------------------------------')
        # i = i+1


if __name__ == '__main__':
    start_time = time.time()
    main()
    elapsed = time.time() - start_time
    print(f"\n程序总运行时间: {timedelta(seconds=elapsed)} [时:分:秒.毫秒]")

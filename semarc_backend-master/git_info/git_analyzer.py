import os
import re
import json
import subprocess


class GitUtil:

    @staticmethod
    def normalize_path(path: str) -> str:
        path.replace("\\", "/")
        path.replace("//", "/")
        path.replace("\\\\", "/")
        return path

    @staticmethod
    def extract_repo_name_from_url(url):
        if url.endswith('.git'):
            url = url[:-4]
        repo_name = url.split('/')[-1]
        if '/' in repo_name:
            repo_name = repo_name.split('/')[-1]
        repo_name = re.sub(r'[^a-zA-Z0-9_-]', '', repo_name)
        if not repo_name:
            repo_name = "repository"

        return repo_name


class GitDiffAnalyzer:
    def __init__(self, url, local_analysis_path, old_rev=None, new_rev=None, commit_hash=None):
        self.url = url
        self.local_path = os.path.abspath(local_analysis_path)

        self.is_consecutive = None

        os.makedirs(self.local_path, exist_ok=True)

        self.repo_name = GitUtil.extract_repo_name_from_url(url)
        self.bare_repo_path = self.local_path
        self.check_bare_repo_exists()

        # self.clone_bare_repository()

        self.language = self.detect_primary_language()
        if self.language not in ['c', 'c++']:
            raise ValueError("Unsupported language. Only C/C++ are supported.")

        if commit_hash:
            self.new_commit = self.resolve_reference(commit_hash)
            self.old_commit = self._get_parent_commit(self.new_commit)
            self.is_consecutive = True
        else:
            if old_rev is None or new_rev is None:
                raise ValueError("Both old_rev and new_rev must be provided if commit is not specified.")
            self.old_commit = self.resolve_reference(old_rev)
            self.new_commit = self.resolve_reference(new_rev)
            self._detect_consecutive()

        print(f"Analyzing changes from {self.old_commit[:7]} to {self.new_commit[:7]}")
        print(f"Versions are {'consecutive' if self.is_consecutive else 'non-consecutive'}")

    def check_bare_repo_exists(self):
        if not self.bare_repo_path.endswith(self.repo_name):
            self.bare_repo_path = os.path.join(self.bare_repo_path, self.repo_name)
            
    def clone_bare_repository(self):
        if os.path.exists(os.path.join(self.bare_repo_path, "HEAD")):
            print(f"Bare repository already exists at {self.bare_repo_path}")
            return

        git_bare_clone_result = subprocess.run(
            ["git", "clone", "--bare", self.url, self.bare_repo_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if git_bare_clone_result.returncode != 0:
            raise RuntimeError(f"Bare clone failed: {git_bare_clone_result.stderr.decode()}")
        print(f"Bare repository cloned to {self.bare_repo_path}")

    def resolve_reference(self, reference):
        # 检查是否为完整的40位SHA-1
        if re.match(r"^[0-9a-f]{40}$", reference):
            return reference

        print(f"本地仓库地址{self.bare_repo_path}")
        ref_types = [
            ("branch", f"refs/heads/{reference}"),
            ("tag", f"refs/tags/{reference}"),
            ("remote branch", f"refs/remotes/origin/{reference}"),
            ("generic", reference)  # 最后尝试原始输入
        ]

        all_errors = []  # 收集所有错误信息

        for ref_type, ref in ref_types:
            git_rev_parse_result = subprocess.run(
                ["git", "rev-parse", ref],
                cwd=self.bare_repo_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            if git_rev_parse_result.returncode == 0:
                return git_rev_parse_result.stdout.decode().strip()
            else:
                err_msg = git_rev_parse_result.stderr.decode().strip()
                all_errors.append(f"{ref_type} '{ref}': {err_msg}")

        # 所有尝试都失败时抛出包含详细错误的异常
        error_details = "\n".join(all_errors)
        raise ValueError(
            f"Invalid reference '{reference}'. 地址'{self.bare_repo_path}'Tried:\n{error_details}"
        )

    def _detect_consecutive(self):
        # git_parent_result = subprocess.run(
        #     ["git", "rev-list", "--parents", "-n", "1", self.new_commit],
        #     cwd=self.bare_repo_path,
        #     stdout=subprocess.PIPE,
        #     stderr=subprocess.PIPE
        # )
        # if git_parent_result.returncode != 0:
        #     raise RuntimeError(f"Revision history check failed: {git_parent_result.stderr.decode()}")

        # commits = git_parent_result.stdout.decode().split()
        self.is_consecutive = False

    def get_function_diff(self, filename, function_name, ranges):
        full_diff = self._get_file_diff(filename)

        old_range = [int(ranges[0]), int(ranges[1])]
        new_range = [int(ranges[2]), int(ranges[3])]

        if ranges[0] == -1 or ranges[1] == -1:
            old_range = None
        else:
            old_range = [int(ranges[0]), int(ranges[1])]

        if ranges[2] == -1 or ranges[3] == -1:
            new_range = None
        else:
            new_range = [int(ranges[2]), int(ranges[3])]

        if ranges[0] and not new_range:
            return json.dumps([{"error": f"Function '{function_name}' not found in either version"}], indent=2)

        function_diffs = self._extract_function_diff(full_diff, old_range, new_range)

        result = []
        for i, diff in enumerate(function_diffs, 1):
            result.append({"id": i, "diff": diff})

        if not result:
            result.append({"info": "No changes detected in the function body"})

        return json.dumps(result, indent=2)

    def _get_file_diff(self, filename):
        result = subprocess.run(
            ["git", "diff", self.old_commit, self.new_commit, "--", filename],
            cwd=self.bare_repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode != 0:
            error_msg = result.stderr.decode()
            if "fatal: bad object" in error_msg:
                return ""
            raise RuntimeError(f"File diff failed: {error_msg}")
        return result.stdout.decode()

    def _get_file_content(self, commit, filename):
        try:
            result = subprocess.run(
                ["git", "show", f"{commit}:{filename}"],
                cwd=self.bare_repo_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            return result.stdout.decode()
        except subprocess.CalledProcessError:
            return None

    def _get_function_range(self, commit, filename, function_name):
        content = self._get_file_content(commit, filename)
        if content is None:
            return None

        lines = content.splitlines()
        start_line = None
        brace_count = 0
        in_function = False
        in_comment = False

        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue

            if '/*' in line:
                in_comment = True
            if '*/' in line:
                in_comment = False
                continue
            if in_comment:
                continue

            line = re.sub(r'//.*', '', line)

            # 检测函数开始
            if not in_function:
                if self._is_function_start(line, function_name):
                    start_line = i + 1  # 转换为1-based
                    # 检查是否在同一行有左大括号
                    if '{' in line:
                        brace_count += line.count('{')
                        in_function = True
                    continue

                # 处理多行函数声明
                elif start_line is not None and not in_function:
                    if '{' in line:
                        brace_count += line.count('{')
                        in_function = True
                    continue
            else:
                # 函数体内，精确计数大括号
                in_string = False
                for char in line:
                    if char == '"':
                        in_string = not in_string
                    elif not in_string:
                        if char == '{':
                            brace_count += 1
                        elif char == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                return start_line, i + 1  # 结束行(1-based)

        # 如果函数开始但未结束(文件末尾)
        if in_function:
            return start_line, len(lines)

        return None

    def _is_function_start(self, line, function_name):
        # 更宽松的函数开始检测，允许跨行
        line = re.sub(r'//.*', '', line)  # 移除单行注释
        line = re.sub(r'/\*.*?\*/', '', line)  # 移除块注释

        if self.language == "c":
            pattern = rf"[\w\s\*]+{function_name}\s*\("
        else:
            pattern = rf"((\w+::)|(template\s*<[^>]+>\s*))?(\w+\s+)*{function_name}\s*\("

        return re.search(pattern, line) is not None

    def _extract_function_diff(self, full_diff, old_range, new_range):

        if not full_diff.strip():
            return []

        hunks = []
        current_hunk = []
        in_hunk = False

        for line in full_diff.splitlines():
            if line.startswith("@@"):
                if current_hunk:
                    hunks.append("\n".join(current_hunk))
                current_hunk = [line]
                in_hunk = True
            elif in_hunk:
                current_hunk.append(line)
            elif line.startswith("diff --git"):
                if current_hunk:
                    hunks.append("\n".join(current_hunk))
                current_hunk = []
                in_hunk = False

        if current_hunk:
            hunks.append("\n".join(current_hunk))

        function_hunks = []
        for hunk in hunks:
            header_line = hunk.split('\n')[0]
            match = re.search(r"@@ -(\d+),?(\d+)? \+(\d+),?(\d+)? @@", header_line)
            if not match:
                continue

            old_start = int(match.group(1))
            old_size = int(match.group(2)) if match.group(2) else 1
            new_start = int(match.group(3))
            new_size = int(match.group(4)) if match.group(4) else 1

            old_end = old_start + old_size - 1
            new_end = new_start + new_size - 1

            if old_range:
                if old_start <= old_range[1] and old_end >= old_range[0]:
                    function_hunks.append(hunk)
                    continue

            if new_range:
                if new_start <= new_range[1] and new_end >= new_range[0]:
                    function_hunks.append(hunk)

        return function_hunks

    def _get_parent_commit(self, commit):
        try:
            result = subprocess.run(
                ["git", "rev-parse", f"{commit}^@"],
                cwd=self.bare_repo_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            parents = result.stdout.decode().splitlines()
            return parents[0] if parents else None
        except subprocess.CalledProcessError:
            try:
                result = subprocess.run(
                    ["git", "rev-parse", f"{commit}^"],
                    cwd=self.bare_repo_path,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True
                )
                return result.stdout.decode().strip()
            except subprocess.CalledProcessError:
                return None

    def get_commit_messages_for_entity(self, filename, ranges, function_name=None):
        if self.is_consecutive:
            return self._get_single_commit_message(self.new_commit)
        else:
            if function_name:
                return self._get_function_commit_messages(filename, function_name)
            else:
                return self._get_file_commit_messages(filename)

    def _get_single_commit_message(self, commit_hash):
        result = subprocess.run(
            ["git", "show", "-s", "--format=full", commit_hash],
            cwd=self.bare_repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            return [f"Error getting commit message for {commit_hash}: {result.stderr}"]
        return [result.stdout.strip()]

    def _get_file_commit_messages(self, filename):
        result = subprocess.run(
            ["git", "log", "--format=full", f"{self.old_commit}..{self.new_commit}", "--", filename],
            cwd=self.bare_repo_path,
            encoding="utf-8",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            return [f"Error getting commit messages for file {filename}: {result.stderr}"]

        commits = result.stdout.strip().split("\ncommit ")
        if commits[0].startswith("commit "):
            return commits

        commits[0] = "commit " + commits[0]
        return commits

    def _get_function_commit_messages(self, filename, function_name):
        # 首选：精确函数签名搜索（-L 模式）
        result = subprocess.run(
            ["git", "log", "-L", f":{function_name}:{filename}",
             f"{self.old_commit}..{self.new_commit}", "--no-patch"],
            cwd=self.bare_repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8',
            text=True
        )

        # 成功获取到提交记录
        if result.returncode == 0 and result.stdout is not None:
            commits = self._format_commit_output(result.stdout)
            if commits:
                return commits

        # 函数签名搜索失败，直接回退到增强函数名搜索
        print("Function signature search failed, falling back to enhanced function-name search")
        return self._get_commit_messages_by_function_name(filename, function_name)

    def _get_commit_messages_by_function_name(self, filename, function_name):
        """在diff内容中搜索函数名（增强搜索）"""
        try:
            result = subprocess.run(
                ["git", "log", f"{self.old_commit}..{self.new_commit}",
                 "--no-patch",
                 "-G", function_name,
                 "--", filename],
                cwd=self.bare_repo_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding='utf-8',
                text=True
            )

            if result.returncode == 0:
                return self._format_commit_output(result.stdout)
        except Exception as e:
            print(f"Enhanced function search failed: {str(e)}")

        # 最终回退：获取整个文件的提交历史
        print("Falling back to file-level commit messages")
        return self._get_file_commit_messages(filename)

    def _format_commit_output(self, output):
        """统一格式化commit输出，确保与原始方法相同"""
        if not output.strip():
            return []

        commits = output.strip().split("\ncommit ")
        if commits[0].startswith("commit "):
            return commits

        # 确保第一个commit有"commit "前缀
        commits[0] = "commit " + commits[0]
        return commits

    def detect_primary_language(self) -> str:
        cpp_extensions = {'.cpp', '.cc', '.cxx', '.hpp', '.hxx', '.hh'}
        c_extensions = {'.c', '.h'}

        # 使用 git ls-tree -r 递归列出所有文件
        result = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", "HEAD"],
            cwd=self.bare_repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(f"Failed to list repository files: {result.stderr}{self.bare_repo_path}")

        has_cpp = False
        has_c = False

        for filename in result.stdout.splitlines():
            ext = os.path.splitext(filename)[1].lower()

            if ext in cpp_extensions:
                has_cpp = True
            elif ext in c_extensions:
                has_c = True

        return "c++" if has_cpp else "c" if has_c else "unknown"

    def get_function_source(self, filename, function_name, ranges):
        sources = [None, None]  # [old, new]

        old_start = ranges[0]
        old_end = ranges[1]
        new_start = ranges[2]
        new_end = ranges[3]

        old_content = self._get_file_content(self.old_commit, filename)
        if old_content is not None:
            if old_start != -1 and old_end != -1:
                lines = old_content.splitlines()

                if old_start == old_end:
                    sources[0] = lines[old_start - 1] if old_start < len(lines) else ""
                else:
                    sources[0] = "\n".join(lines[old_start - 1:old_end])

        new_content = self._get_file_content(self.new_commit, filename)
        if new_content is not None:
            if new_start != -1 and new_end != -1:
                lines = new_content.splitlines()

                if new_start == new_end:
                    sources[1] = lines[new_start - 1] if new_start < len(lines) else ""
                else:
                    sources[1] = "\n".join(lines[new_start - 1:new_end])

        return sources


def main():
    url = "https://github.com/libuv/libuv.git"
    local_analysis_path = "D:/my/intern/mlccd/changeHierTemp"
    local_analysis_path = GitUtil.normalize_path(local_analysis_path)
    old_rev = "v1.44.2"
    # old_rev = "8d4218d"

    new_rev = "v1.48.0"
    # new_rev = "a3b8cb9cc0410b3f40972179b1b430e3a450002a"
    language = "c"
    commit_hash = "0d4f54f0f6a803d7ec06c647d4899e94cd8607c4"

    analyzer1 = GitDiffAnalyzer(
        url=url,
        local_analysis_path=local_analysis_path,
        old_rev=old_rev,
        new_rev=new_rev,
    )

    # print(analyzer1.get_function_diff("src/unix/core.c", "uv_run"))

    # analyzer2 = GitDiffAnalyzer(
    #     url=url,
    #     local_analysis_path=local_analysis_path,
    #     commit_hash=commit_hash,
    #     language=language,
    # )

    # analyzer3 = GitDiffAnalyzer(
    #     url=url,
    #     local_analysis_path=local_analysis_path,
    #     language=language,
    #     old_rev=old_rev,
    #     new_rev=new_rev,
    # )

    # # 测试获取文件级别的commit messages
    # print("\nFile-level commit messages:")
    # file_commits = analyzer1.get_commit_messages_for_entity("src/unix/core.c")
    # for commit in file_commits[:2]:  # 只打印前2个
    #     print(commit[:500] + "..." if len(commit) > 500 else commit)
    #     print("-" * 80)
    #
    # # 测试获取函数级别的commit messages
    # print("\nFunction-level commit messages:")
    # function_commits = analyzer1.get_commit_messages_for_entity("src/unix/core.c", "uv_run")
    # for commit in function_commits:  # 只打印前2个
    #     print(commit)

    # # 测试连续版本的情况
    # analyzer2 = GitDiffAnalyzer(
    #     url=url,
    #     local_analysis_path=local_analysis_path,
    #     commit_hash=commit_hash,
    #     language=language,
    # )
    #
    # print("\nSingle commit message (consecutive versions):")
    # single_commit = analyzer2.get_commit_messages_for_entity("src/unix/core.c")
    # print(single_commit[0][:500] + "..." if len(single_commit[0]) > 500 else single_commit[0])

    print("\nFunction source code:")
    old_source, new_source = analyzer1.get_function_source("src/unix/core.c", "uv_run")
    print("Old version:")
    print(old_source or "Function not found in old version")
    print("\nNew version:")
    print(new_source or "Function not found in new version")


# 使用示例
if __name__ == "__main__":
    main()

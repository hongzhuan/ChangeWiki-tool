import os
import subprocess

from changes.entity import Entity
from git_info.git_analyzer import GitUtil


class EntityInput:
    def __init__(self, entity: 'Entity'):

        self.entity = entity
        self.commits = []
        self.entity_path = ''
        self.url = str
        self.before_code = ''
        self.after_code = ''
        self.isCommit = bool
        self.project_root = self.get_project_root()

    def get_input_string(self) -> str:


        input_parts = []
        print("root analysis: " + self.entity_path)
        if not os.listdir(self.entity_path):
            return ""
        prompt = self.read_json_as_str("prompt")
        if prompt:
            input_parts.append(prompt)

        input_parts.append("\n{changes}\n")
        changes = self.read_json_as_str("changes")
        if changes:
            input_parts.append(changes)


        input_parts.append("\n{innerChanges}\n")
        inner_changes = self.read_json_as_str("innerChanges")
        if inner_changes:
            input_parts.append(inner_changes)

        input_parts.append("\n{beforeCode}\n")
        if self.before_code:
            input_parts.append(self.before_code)

        input_parts.append("\n{afterCode}\n")
        if self.after_code:
            input_parts.append(self.after_code)


        input_parts.append("\n{Commits}\n")
        if self.commits:

            formatted_commits = []
            for i, commit in enumerate(self.commits, start=1):
                formatted_commits.append(f"{{commitMessage{i}}}\n{commit}")
            input_parts.append("\n".join(formatted_commits))

        return "".join(input_parts)


    def get_project_root(self, marker_dir=None):
        if marker_dir is None:
            marker_dir = ['llm']

        if isinstance(marker_dir, str):
            marker_dir = [marker_dir]

        current_dir = os.path.abspath(os.path.dirname(__file__))

        while current_dir != os.path.dirname(current_dir):
            if any(os.path.exists(os.path.join(current_dir, marker)) for marker in marker_dir):
                return current_dir
            current_dir = os.path.dirname(current_dir)

        return current_dir

    def read_json_as_str(self, content: str) -> str|None:
        llm_dir = GitUtil.normalize_path(os.path.join(self.project_root, 'llm'))


        if content == 'prompt':
            if self.entity.entity_granularity == "File":
                with open(f"{llm_dir}/prompt/file_prompt.txt", 'r', encoding='utf-8') as file:
                    return file.read()
            elif self.entity.entity_granularity == "Function":
                with open(f"{llm_dir}/prompt/function_prompt.txt", 'r', encoding='utf-8') as file:
                    return file.read()
            elif self.entity.entity_granularity == "Commit":
                with open(f"{llm_dir}/prompt/commit_prompt.txt", 'r', encoding='utf-8') as file:
                    return file.read()
        elif content == 'changes':
            changes_content = None

            changes_path = os.path.join(self.entity_path, 'changes.json')
            try:
                with open(changes_path, 'r', encoding='utf-8') as file:
                    changes_content = file.read()
            except FileNotFoundError:
                print(f"Tip: Changes file not found at {changes_path}")

            if self.entity.entity_granularity != "File":
                changes_path = os.path.join(self.entity_path, 'changes.txt')
                try:
                    with open(changes_path, 'r', encoding='utf-8') as file:
                        changes_content += "\n" + file.read()
                except FileNotFoundError:
                    print(f"Tip: Diff file not found at {changes_path}")

            return changes_content


        elif content == 'innerChanges':
            if not os.path.isdir(self.entity_path):
                return None
            semantic_contents = []
            for i, entry in enumerate(os.scandir(self.entity_path), start=1):
                if entry.is_dir():
                    semantic_path = os.path.join(entry.path, "semantic.txt")
                    if os.path.exists(semantic_path):
                        try:
                            with open(semantic_path, 'r', encoding='utf-8') as file:
                                content = file.read().strip()
                                if content:
                                    semantic_contents.append(f"{{innerChanges{i}}}\n{content}")
                        except IOError:
                            continue
            return "\n\n".join(semantic_contents) if semantic_contents else None
        return None



    def get_git_commits(self) -> None:

        if self.isCommit:
            return

        try:
            repo_path = self.url
            git_log_cmd = [
                "git",
                "-C",
                repo_path,
                "log",
                self.after_code,
                "-n", "1",
                "--pretty=format:%s"
            ]

            result = subprocess.run(
                git_log_cmd,
                check=True,
                capture_output=True,
                text=True
            )

            commit_message = result.stdout.strip()
            if commit_message:
                self.commits.append("commitMessage1" + commit_message)

        except subprocess.CalledProcessError as e:
            print(f"Error getting git commits: {e.stderr}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
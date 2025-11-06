import subprocess
import sys
from pathlib import Path


def get_jar_path():

    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    jar_path = project_root / "libs" / "ChangeHierDetect.jar"

    if not jar_path.exists():
        print(f"错误：JAR文件未找到于 {jar_path}")
        print("请检查：")
        print(f"1. 项目根目录是否为 {project_root}")
        print(f"2. libs/目录下是否存在ChangeHierDetect.jar")
        sys.exit(1)

    return jar_path


def run_jar_analysis(
        local_analysis_path: str,
        before_version_hash: str,
        after_version_hash: str,
        output_dir: str,
        repo_name: str,
        language: str
):
    """
    执行JAR分析工具

    参数:
        local_analysis_path: 仓库本地路径
        before_version_hash: 旧版本哈希
        after_version_hash: 新版本哈希
        output_dir: 输出目录路径
        repo_name: 仓库名称
        language: 项目语言(c/cpp/java等)
    """
    try:
        # 获取JAR路径
        jar_path = get_jar_path()

        # 准备参数
        args = [
            local_analysis_path,
            before_version_hash,
            after_version_hash,
            output_dir,
            repo_name,
            language.lower()
        ]

        # 打印执行的命令（调试用）
        print("执行命令:", ["java", "-jar", str(jar_path)] + args)

        # 执行命令
        subprocess.run(
            ["java", "-jar", str(jar_path)] + args,
            check=True,
            text=True,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        print("分析执行成功！")

    except subprocess.CalledProcessError as e:
        print(f"分析失败！错误代码: {e.returncode}")
        print("错误输出:", e.stderr)
        sys.exit(1)


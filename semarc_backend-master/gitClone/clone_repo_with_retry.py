import subprocess
import shutil
def clone_repo_with_retry(repo_url, selected_version, clone_dir):
    try:
        subprocess.run(
            ["git", "clone", "--branch", selected_version, repo_url, clone_dir],
            check=True,
            text=True
        )
        print(f"仓库已成功克隆到 {clone_dir}")
    except subprocess.CalledProcessError as e:
        error_message = e.stderr if e.stderr else str(e)
        if "OpenSSL SSL_connect" in error_message:
            print("检测到 SSL 错误，正在重新尝试克隆...")
            # 删除可能的残留目录
            shutil.rmtree(clone_dir, ignore_errors=True)
            subprocess.run(
                ["git", "clone", "--branch", selected_version, "--depth", "1", repo_url, clone_dir],
                check=True,
                text=True
            )
            print(f"重新克隆成功到 {clone_dir}")
        else:
            raise e


import os

def split_commit_log(file_path, output_dir, chunk_size=100):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 按照 commit 分割日志
    commit_logs = content.split('\n\ncommit ')
    commit_logs = ['commit ' + log for log in commit_logs if log.strip()]

    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 分割并写入新的文件
    for i in range(0, len(commit_logs), chunk_size):
        fragment = '\n\n'.join(commit_logs[i:i + chunk_size])
        output_file_path = os.path.join(output_dir, f'libuv_log_{(i + chunk_size)}.txt')
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(fragment)
        print(f'Created: {output_file_path}')

if __name__ == "__main__":
    input_file_path = 'd:\\胡杨林基金\\双周例会\\250320\\libuv\\libuv_log.txt'
    output_directory = 'd:\\胡杨林基金\\双周例会\\250320\\libuv_new\\split_logs'
    split_commit_log(input_file_path, output_directory)
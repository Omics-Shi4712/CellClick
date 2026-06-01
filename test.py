import os
import argparse


def count_file_lines(file_path):
    """
    统计单个.py文件的各类行数
    :param file_path: 文件路径
    :return: total_lines(总行数), blank_lines(空行数), comment_lines(注释行数), code_lines(有效代码行数)
    """
    total_lines = 0
    blank_lines = 0
    comment_lines = 0
    code_lines = 0
    in_multi_comment = False  # 标记是否处于多行注释中
    multi_comment_delimiter = None  # 记录多行注释的分隔符（""" 或 '''）

    # 处理文件读取的编码问题（优先utf-8，其次gbk）
    def read_file_lines():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.readlines()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='gbk') as f:
                    return f.readlines()
            except Exception as e:
                print(f"❌ 读取文件 {file_path} 失败：{str(e)}")
                return []
        except Exception as e:
            print(f"❌ 读取文件 {file_path} 失败：{str(e)}")
            return []

    lines = read_file_lines()
    for line in lines:
        total_lines += 1
        line_stripped = line.strip()  # 去除首尾空白字符

        # 处理多行注释
        if in_multi_comment:
            comment_lines += 1
            # 检查是否结束多行注释
            if multi_comment_delimiter in line_stripped:
                in_multi_comment = False
                multi_comment_delimiter = None
            continue

        # 空行（去除空白后无内容）
        if not line_stripped:
            blank_lines += 1
            continue

        # 单行注释（以#开头）
        if line_stripped.startswith('#'):
            comment_lines += 1
            continue

        # 多行注释开始（""" 或 '''）
        if line_stripped.startswith(('"""', "'''")):
            comment_lines += 1
            # 检查是否是单行多行注释（如 """这是注释"""）
            if line_stripped.count(line_stripped[:3]) == 2:
                continue
            # 标记进入多行注释
            in_multi_comment = True
            multi_comment_delimiter = line_stripped[:3]
            continue

        # 有效代码行（包含代码+行内注释的情况，如 print(1) # 注释）
        code_lines += 1

    return total_lines, blank_lines, comment_lines, code_lines


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='统计代码仓库中所有.py文件的行数')
    parser.add_argument('--path', type=str, default='.', help='代码仓库根路径（默认当前目录）')
    parser.add_argument('--exclude', nargs='*', default=['.git', '__pycache__', 'venv', 'env'],
                        help='需要排除的目录（默认：.git、__pycache__、venv、env）')
    args = parser.parse_args()

    root_path = os.path.abspath(args.path)
    exclude_dirs = [os.path.abspath(d) for d in args.exclude]
    file_stats = []  # 存储所有文件的统计结果
    # 总计初始化
    total_all = 0
    blank_all = 0
    comment_all = 0
    code_all = 0

    # 遍历目录下的所有.py文件
    for dirpath, dirnames, filenames in os.walk(root_path):
        # 排除指定目录
        dirpath_abs = os.path.abspath(dirpath)
        if any(exclude_dir in dirpath_abs for exclude_dir in exclude_dirs):
            continue
        # 过滤出.py文件
        for filename in filenames:
            if filename.endswith('.py'):
                file_path = os.path.join(dirpath, filename)
                # 统计当前文件行数
                total, blank, comment, code = count_file_lines(file_path)
                if total == 0:
                    continue  # 跳过读取失败的文件
                # 存储结果
                file_stats.append({
                    'path': file_path,
                    'total': total,
                    'blank': blank,
                    'comment': comment,
                    'code': code
                })
                # 累加总计
                total_all += total
                blank_all += blank
                comment_all += comment
                code_all += code

    # 输出统计结果
    print("=" * 120)
    print(f"代码仓库路径：{root_path}")
    print("=" * 120)
    # 打印表头
    print(f"{'文件路径':<70} {'总行数':<10} {'空行数':<10} {'注释行数':<10} {'有效代码行数':<10}")
    print("-" * 120)
    # 打印每个文件的统计
    for stat in file_stats:
        print(f"{stat['path']:<70} {stat['total']:<10} {stat['blank']:<10} {stat['comment']:<10} {stat['code']:<10}")
    # 打印总计
    print("-" * 120)
    print(f"{'总计':<70} {total_all:<10} {blank_all:<10} {comment_all:<10} {code_all:<10}")
    print("=" * 120)


if __name__ == '__main__':
    main()
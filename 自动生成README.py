"""
    module(main) - 生成readme的目录，脚本自动去掉第一个#以前的内容，并在开头添加目录.

    Main members:

        # __main__ - 主函数.
"""
import codecs
from collections import defaultdict
import re


def read_file_texts(file_name):
    """读取文件内容.

    Args:
        file_name: 文件名.

    Returns:
        文件内容列表，元素为每行.
    """
    with codecs.open(file_name, mode='r', encoding='utf8') as fr:
        texts = list()
        for line in fr:
            texts.append(line)
        return texts


def get_contents(file_texts):
    """ 获取内容列表，忽略掉开头的目录.

        @params:
            file_texts - 文件内容.

        @return:
            On success - 标题列表.
    """
    contents_lines = list()
    content_flag = False
    for row_data in file_texts:
        if not content_flag:
            # 正文开头判断，以单独的#作为开头
            re_obj = re.match('#+', row_data)
            if re_obj and len(re_obj.group()) == 1:
                content_flag = True
                contents_lines.append(row_data)
            continue
        contents_lines.append(row_data)
    return contents_lines


def get_head_texts(contents):
    """ 提取标题列表.

        @params:
            contents - 文件内容.

        @return:
            On success - 标题列表.
    """
    head_lines = list()
    code_line_flag = False
    # 提取标题文本，并对重复的文本自动补充后缀
    fixed_contents = list()
    head_count_dict = defaultdict(int)  # 初始化为 0
    for row_data in contents:
        # 代码注释判断
        if code_line_flag:
            if row_data.startswith('~~~'):
                code_line_flag = False
        elif row_data.startswith('~~~'):
            code_line_flag = True
        elif row_data.startswith('#'):
            head_count_dict[row_data] += 1
            head_count = head_count_dict[row_data]
            if head_count > 1:
                row_data = '{}-{}\n'.format(row_data.strip(), head_count)
            head_lines.append(row_data)
        fixed_contents.append(row_data)
    # 构造带有超链接的目录
    head_texts = list()
    for head_line in head_lines:
        level_chars = re.match('#+', head_line).group()
        head_text = head_line.lstrip(level_chars).strip()
        tab_str = ''.join(['  ' for i in range(len(level_chars)-1)])
        head_href_text = head_text.replace(' ', '-')
        head_texts.append('{}- [{}](#{})\n'.format(tab_str, head_text, head_href_text))
    return head_texts, fixed_contents


if __name__ == "__main__":
    """ readme生成目录.
    参考：https://github.com/houbb/markdown-toc/blob/master/doc/Github-MD-Href.md
    """
    file_ins = ['readme_tools.md', 'readme_model.md']
    for file_in in file_ins:
        file_texts = read_file_texts(file_in)
        contents = get_contents(file_texts)
        head_texts, contents = get_head_texts(contents)
        with codecs.open(file_in, mode='w', encoding='utf8') as fw:
            # 目录输出
            fw.write('**目录(Table of contents)**')
            fw.write('\n\n')
            for line in head_texts:
                fw.write(line)
                fw.write('\n')
            fw.write('\n')
            # 原始文本内容输出
            for line in contents:
                fw.write(line)
        print('{} 目录已更新完毕'.format(file_in))

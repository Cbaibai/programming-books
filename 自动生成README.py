"""
    module(main) - ����readme��Ŀ¼���ű��Զ�ȥ����һ��#��ǰ�����ݣ����ڿ�ͷ���Ŀ¼.

    Main members:

        # __main__ - ������.
"""
import codecs
from collections import defaultdict
import re


def read_file_texts(file_name):
    """��ȡ�ļ�����.

    Args:
        file_name: �ļ���.

    Returns:
        �ļ������б�Ԫ��Ϊÿ��.
    """
    with codecs.open(file_name, mode='r', encoding='utf8') as fr:
        texts = list()
        for line in fr:
            texts.append(line)
        return texts


def get_contents(file_texts):
    """ ��ȡ�����б����Ե���ͷ��Ŀ¼.

        @params:
            file_texts - �ļ�����.

        @return:
            On success - �����б�.
    """
    contents_lines = list()
    content_flag = False
    for row_data in file_texts:
        if not content_flag:
            # ���Ŀ�ͷ�жϣ��Ե�����#��Ϊ��ͷ
            re_obj = re.match('#+', row_data)
            if re_obj and len(re_obj.group()) == 1:
                content_flag = True
                contents_lines.append(row_data)
            continue
        contents_lines.append(row_data)
    return contents_lines


def get_head_texts(contents):
    """ ��ȡ�����б�.

        @params:
            contents - �ļ�����.

        @return:
            On success - �����б�.
    """
    head_lines = list()
    code_line_flag = False
    # ��ȡ�����ı��������ظ����ı��Զ������׺
    fixed_contents = list()
    head_count_dict = defaultdict(int)  # ��ʼ��Ϊ 0
    for row_data in contents:
        # ����ע���ж�
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
    # ������г����ӵ�Ŀ¼
    head_texts = list()
    for head_line in head_lines:
        level_chars = re.match('#+', head_line).group()
        head_text = head_line.lstrip(level_chars).strip()
        tab_str = ''.join(['  ' for i in range(len(level_chars)-1)])
        head_href_text = head_text.replace(' ', '-')
        head_texts.append('{}- [{}](#{})\n'.format(tab_str, head_text, head_href_text))
    return head_texts, fixed_contents


if __name__ == "__main__":
    """ readme����Ŀ¼.
    �ο���https://github.com/houbb/markdown-toc/blob/master/doc/Github-MD-Href.md
    """
    file_ins = ['readme_tools.md', 'readme_model.md']
    for file_in in file_ins:
        file_texts = read_file_texts(file_in)
        contents = get_contents(file_texts)
        head_texts, contents = get_head_texts(contents)
        with codecs.open(file_in, mode='w', encoding='utf8') as fw:
            # Ŀ¼���
            fw.write('**Ŀ¼(Table of contents)**')
            fw.write('\n\n')
            for line in head_texts:
                fw.write(line)
                fw.write('\n')
            fw.write('\n')
            # ԭʼ�ı��������
            for line in contents:
                fw.write(line)
        print('{} Ŀ¼�Ѹ������'.format(file_in))

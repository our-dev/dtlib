"""
文件
"""
import os


class TxtFileIteration(object):
    """
    读取一个索引文本文件，然后再去读取二进制文件
    # 使用迭代器读取 path目录中的文件
    example:
    
    .. code::
    
        def read_img_tag_file(tag_file_path):
            file = TxtFileIteration(tag_file_path)
            file_len = 0
        
            text_list = []
        
            for item in file:
                # print(item)
                text_list.append(item)
                file_len += 1
        
            print(file_len)
            return text_list
    
    
    """

    def __init__(self, path):
        self.path = path

    def __iter__(self):
        for line in open(self.path):
            yield line


def get_home_path():
    """
    获取home目录，在不同系统下能统一路径
    :return: 
    """
    # 下面的图像分类模型提供了模型搭建的代码和相应的预训练权重
    home_path = os.environ['HOME']

    return home_path


def get_parent_folder_name(file):
    """
    根据传入的文件对象，获取所在的目录的名称
    :param file: __file__
    :return:
    """
    full_path = os.path.realpath(file)
    folder = full_path.split(os.sep)[-2]
    return folder


def get_file_info(full_path):
    """
    根据完整的数据返回如下信息：
    1. 当前文件名称
    # 2. 父文件夹名称
    3. 文件父路径
    :param full_path:
    :return:
    """

    dir_name = os.path.dirname(full_path)
    file_name = os.path.basename(full_path)
    return dir_name, file_name


import os
 
 
def renaming(file):
    """修改后缀"""

    if(file.find("123")!=-1):
        #有问题
        print(file)
    ext = os.path.splitext(file)    # 将文件名路径与后缀名分开
 
    if ext[1] != '.jpg' and ext[1] != '.md':                    # 文件名：ext[0]
        new_name = ext[0] + '.jpg'         # 文件后缀：ext[1]
        os.rename(file, new_name)
        print(file)
 
 
def tree(path):
    """递归函数"""
    files = os.listdir(path)    # 获取当前目录的所有文件及文件夹
    for file in files:
        file_path = os.path.join(path, file)  # 获取该文件的绝对路径
        if os.path.isdir(file_path):    # 判断是否为文件夹
            tree(file_path)     # 开始递归
        else:
            os.chdir(path)      # 修改工作地址（相当于文件指针到指定文件目录地址）
            renaming(file)      # 修改后缀
 
try:
    tree("D:\\Project\\cjhbUpdate\\newest\\downloadserver")
except Exception as e:
    print(e)
    pass
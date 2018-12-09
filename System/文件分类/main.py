#遍历目录并打印
import os
import shutil

path = os.getcwd()+'/file/字体/'
file_image_path = os.getcwd()+'/file/字体/'
def listFile(path, file_image_path):
    try:
        dirs = os.listdir(path)
    except PermissionError as e:
        print (e)
    else:
        for files in dirs:
            temp = os.path.join(path,files)
            if os.path.isdir(temp):
                # if not os.listdir(temp):
                #     os.rmdir(temp)
                listFile(temp, file_image_path)
            else:
                if files.rfind('.rar') != -1:
                    if not os.path.exists(file_image_path):
                        os.makedirs(file_image_path)
                    shutil.move(temp, file_image_path)
listFile(path, file_image_path)
#遍历目录并打印
import os
import shutil
import re
path = 'G:/smzh12（有JS模式）'
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
                # if files.rfind('.rar') != -1:
                #     if not os.path.exists(file_image_path):
                #         os.makedirs(file_image_path)
                #     shutil.move(temp, file_image_path)
                if re.search('.*?([.*?])', files):
                    name = re.sub(' \[.*?\]', '', files)
                    os.rename(path+'\\'+files, path+'\\'+name)
listFile(path, file_image_path)
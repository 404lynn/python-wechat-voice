import os
from flask import Flask, request, jsonify
import queue
import threading
import uiautomator2 as u2
import re

# 创建一个线程安全的队列
task_queue = queue.Queue()

def worker():
    while True:
        task = task_queue.get()  # 获取任务
        print(task,"cccccccccccc")     
        try:
            isgroup, getname, content, atpeople,url = task
        except Exception as e:
            print(f"Error processing task: {e}")
        task_queue.task_done()  # 标记任务完成

api = Flask(__name__)

# 修改后的文件上传接口
@api.route('/upload_wx_file', methods=['POST'])
def handle_file_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    # 获取动态文件夹参数
    folder_name = request.form.get('folder', 'default')
    
    # 安全校验文件夹名称
    if not re.match(r'^[\w-]{1,20}$', folder_name):
        return jsonify({'error': 'Invalid folder name'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # 创建动态目录
    save_dir = os.path.join(os.getcwd(), folder_name)
    os.makedirs(save_dir, exist_ok=True)

    # 保存文件
    file_path = os.path.join(save_dir, file.filename)
    file.save(file_path)
    
    return jsonify({
        'status': 'success',
        'saved_path': file_path,
        'folder': folder_name,
        'file_size': os.path.getsize(file_path)
    }), 200

if __name__ == '__main__':
    thread = threading.Thread(target=worker, daemon=True)
    thread.start()
    # 移除原有的固定目录创建逻辑
    api.run(debug=True, port=9105, host='10.141.59.166', threaded=True)
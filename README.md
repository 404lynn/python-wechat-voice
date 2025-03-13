# python--
使用python对微信数据库的一些获取
# 编码格式
微信的语音文件虽然扩展名为.amr，但内部却用的SILK编码格式：
![alt text](image.png)
所以先将这个amr的改为正确的silk格式写入silk的空文件中
def modify_binary_data(data):
    new_header = b'\xFF\xFF'  # 23 21 41 4D 52 0A
    data =   data[1:-2]+new_header
    return data
found_file为获取的语音文件
 with open(found_file, 'rb') as file:
        data = file.read()
        modified_data = modify_binary_data(data)#修改参数
    with open('modified_amr_file.silk', 'wb') as file:
        file.write(modified_data)
此时就获取了正确编码的silk格式微信语音
后续就随意转格式为需要的。
duration = pilk.decode("modified_amr_file.silk", "test.pcm")#转pcm
pcm_file = 'test.pcm'
music1 = pcm_file
silk_file = 'modified_amr_file.silk'
music2 = silk_file
output_file = file_name+'.wav'
music3 = output_file
sample_rate = 24000
channel = 1
pcm2wav(pcm_file, output_file, channel, sample_rate)#转wav
total_size = os.path.getsize(output_file)

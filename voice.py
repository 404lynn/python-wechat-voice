#找语音
def modify_binary_data(data):
    new_header = b'\xFF\xFF'  # 23 21 41 4D 52 0A
    data =   data[1:-2]+new_header
    return data
def pcm2wav(pcm_path, out_path, channel, sample_rate):
    with open(pcm_path, 'rb') as pcm_file:
        pcm_data = pcm_file.read()
        pcm_file.close()
    with wave.open(out_path, 'wb') as wav_file:
        ## 不解之处， 16 // 8， 第4个参数0为何有效
        wav_file.setparams((channel, 16 // 8, sample_rate, 0, 'NONE', 'NONE'))
        wav_file.writeframes(pcm_data)
        wav_file.close()
def find_amr_file(voice2_dir, file_name):
    for root, dirs, files in os.walk(voice2_dir):
        for file in files:
            if file == file_name + '.amr':
                return os.path.join(root, file)
    return None
voice2_dir = os.path.join(outadress,'voice2')#放语音的文件夹
file_name ='msg_'+row[9]#数据库中的名称
found_file = find_amr_file(voice2_dir, file_name)#遍历获取
if found_file:
    with open(found_file, 'rb') as file:
        data = file.read()
        modified_data = modify_binary_data(data)#修改参数
    with open('modified_amr_file.silk', 'wb') as file:
        file.write(modified_data)
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
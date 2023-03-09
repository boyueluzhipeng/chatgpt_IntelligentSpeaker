import time
import subprocess
from lu_tts import play_voice
from get_token import get_yaml_token, get_yaml_apikey
token, _ = get_yaml_token()
api_key = get_yaml_apikey()   
import openai
openai.api_key = api_key
from ChatGPT.ChatGPT import Chatbot
bot = Chatbot(api_key=api_key)

if __name__ == "__main__":
    # nls.enableTrace(True)
    name = "thread" + str(0)
    
    is_use_audio = input("是否使用录音功能？(y/n)")
    if is_use_audio == 'y':
        is_use_audio = True
    else:
        is_use_audio = False
        
    is_play_voice = input("是否使用播放功能？(y/n)")
    if is_play_voice == 'y':
        is_play_voice = True
    else:
        is_play_voice = False
    
    while True:
        result = "未识别到您的声音"
        # 录制音频，如果声音中间有停顿，则结束录制，保存为test.pcm
        print("=" * 40)
        time_s = time.time()
        if is_use_audio:
            print("开始录制")
            # subprocess.call("sox -d -r 16000 -c 1 -b 16 test.wav silence 1 0.1 1% 1 1.0 1%", shell=True)
            # sox 录制音频，如果声音中间有停顿，则结束录制，保存为test.pcm
            subprocess.call("sox -d -r 16000 -c 1 -b 16 test.wav silence 1 0.1 1% 1 1.0 1%", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("录制结束")
            audio_file = open("test.wav", "rb")
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            transcript_text = transcript['text']
        else:
            transcript_text = input("请输入文字：")
        print('-' * 40)
        print(f'你说的是：{transcript_text}')
        print(f'消耗时间：{time.time() - time_s}')
        print('-' * 40)
        time_s = time.time()
        answer_text = ""
        bot_response = bot.ask_stream(transcript_text, 'user')
        print('ChatGPT: ', end='')
        for data in bot_response:
            print(data, end='', flush=True)
            answer_text += data
        print()
        print(f'消耗时间：{time.time() - time_s}')
        print('-' * 40)
        if is_play_voice:
            # 计算返回文字的长度，如果长度大于300，则分段播放
            for i in range(0, len(answer_text), 300):
                t = play_voice(answer_text[i:i+300], token)
                # 获取lu.wav文件的时长，用于延时
                # wav_file = AudioSegment.from_file("lu.wav", format="wav")
                # duration = wav_file.duration_seconds
                while t.is_completed == False:
                    time.sleep(0.1)

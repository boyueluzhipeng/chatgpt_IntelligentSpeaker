import os
import sys
import threading
import time

import subprocess
import nls
from get_token import *
AKID = get_AKID()    #获取AccessKey ID和AccessKey Secret请前往控制台：https://ram.console.aliyun.com/manage/ak
AKKEY = get_AKKEY()    #获取AccessKey ID和AccessKey Secret请前往控制台：https://ram.console.aliyun.com/manage/ak
APPKEY = get_APPKEY()    #获取AccessKey ID和AccessKey Secret请前往控制台：https://ram.console.aliyun.com/manage/ak
URL = get_url()

thread_lock = threading.Lock()
#以下代码会根据上述TEXT文本反复进行语音合成
class TestTts:
    def __init__(self, tid, test_file, text, token, voice='xiaoyun'):
        self.__th = threading.Thread(target=self.__test_run)
        self.__id = tid
        self.__test_file = test_file
        self.token = token
        self.is_completed = False
        self.voice = voice
        self.start(text)
   
    def start(self, text):
        self.__text = text
        self.__f = open(self.__test_file, "wb")
        self.__th.start()
    
    def test_on_metainfo(self, message, *args):
        # print("on_metainfo message=>{}".format(message))  
        pass

    def test_on_error(self, message, *args):
        # print("on_error args=>{}".format(args))
        pass

    def test_on_close(self, *args):
        return_code = subprocess.call(["afplay", "lu.wav"])
        if return_code:
            print("播放失败")
        else:
            print('播放结束')
            print("+" * 40)
        self.is_completed = True
        thread_lock.release()
        try:
            self.__f.close()
        except Exception as e:
            print("close file failed since:", e)

    def test_on_data(self, data, *args):
        try:
            self.__f.write(data)
        except Exception as e:
            print("write data failed:", e)

    def test_on_completed(self, message, *args):
        # print("on_completed:args=>{} message=>{}".format(args, message))
        pass


    def __test_run(self):
        thread_lock.acquire()
        # print(f'url={URL}, appkey={APPKEY}, token={self.token}')
        tts = nls.NlsSpeechSynthesizer(
                    url=URL,
                    appkey=APPKEY,
                    token=self.token,
                    on_metainfo=self.test_on_metainfo,
                    on_data=self.test_on_data,
                    on_completed=self.test_on_completed,
                    on_error=self.test_on_error,
                    on_close=self.test_on_close,
                    callback_args=[self.__id],
                )
        tts.start(self.__text, voice=self.voice, aformat="wav", sample_rate=16000, speech_rate=400)

        
def play_voice(text, token, voice='zhimiao_emo'):
    return TestTts(text, "lu.wav", text, token, voice)

def save_voice(user_name, res):
    token, _ = get_yaml_token()
    wav_path = '/www/wwwroot/h6.l-hate.com/'
    wav_file = wav_path + str(time.time()) + '.wav'
    TestTts('test', wav_file, res, token)

if __name__ == "__main__":
    save_voice(TEXT, "lu.wav")
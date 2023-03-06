#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac
import requests
import time
import uuid
from urllib import parse
import yaml
class AccessToken:
    @staticmethod
    def _encode_text(text):
        encoded_text = parse.quote_plus(text)
        return encoded_text.replace('+', '%20').replace('*', '%2A').replace('%7E', '~')
    @staticmethod
    def _encode_dict(dic):
        keys = dic.keys()
        dic_sorted = [(key, dic[key]) for key in sorted(keys)]
        encoded_text = parse.urlencode(dic_sorted)
        return encoded_text.replace('+', '%20').replace('*', '%2A').replace('%7E', '~')
    @staticmethod
    def create_token(access_key_id, access_key_secret):
        parameters = {'AccessKeyId': access_key_id,
                      'Action': 'CreateToken',
                      'Format': 'JSON',
                      'RegionId': 'cn-shanghai',
                      'SignatureMethod': 'HMAC-SHA1',
                      'SignatureNonce': str(uuid.uuid1()),
                      'SignatureVersion': '1.0',
                      'Timestamp': time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                      'Version': '2019-02-28'}
        # 构造规范化的请求字符串
        query_string = AccessToken._encode_dict(parameters)
        print('规范化的请求字符串: %s' % query_string)
        # 构造待签名字符串
        string_to_sign = 'GET' + '&' + AccessToken._encode_text('/') + '&' + AccessToken._encode_text(query_string)
        print('待签名的字符串: %s' % string_to_sign)
        # 计算签名
        secreted_string = hmac.new(bytes(access_key_secret + '&', encoding='utf-8'),
                                   bytes(string_to_sign, encoding='utf-8'),
                                   hashlib.sha1).digest()
        signature = base64.b64encode(secreted_string)
        print('签名: %s' % signature)
        # 进行URL编码
        signature = AccessToken._encode_text(signature)
        print('URL编码后的签名: %s' % signature)
        # 调用服务
        full_url = 'http://nls-meta.cn-shanghai.aliyuncs.com/?Signature=%s&%s' % (signature, query_string)
        print('url: %s' % full_url)
        # 提交HTTP GET请求
        response = requests.get(full_url)
        if response.ok:
            root_obj = response.json()
            key = 'Token'
            if key in root_obj:
                token = root_obj[key]['Id']
                expire_time = root_obj[key]['ExpireTime']
                return token, expire_time
        print(response.text)
        return None, None
    

def read_yaml():
    with open('config.yaml', 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        return config
    
def get_yaml_token():
    config = read_yaml()
    token = config['token']
    expire_time = config['expire_time']
    # 如果token过期，重新获取
    if time.time() > float(expire_time):
        token, expire_time = get_token()
        config['token'] = token
        config['expire_time'] = expire_time
        with open('config.yaml', 'w') as f:
            yaml.dump(config, f)
    return token, expire_time

def get_yaml_apikey():
    config = read_yaml()
    apikey = config['api_key']
    return apikey

def get_url():
    config = read_yaml()
    url = config['URL']
    return url

def get_AKID():
    config = read_yaml()
    AKID = config['AKID']
    return AKID

def get_AKKEY():
    config = read_yaml()
    AKKEY = config['AKKEY']
    return AKKEY

def get_APPKEY():
    config = read_yaml()
    APPKEY = config['APPKEY']
    return APPKEY
    

def get_token():
    # 用户信息
    access_key_id = 'LTAIT7eDUfcKRP89'
    access_key_secret = 'j0t4x1MpqDdqHmOHhIjkT7c4t2y5Ey'
    token, expire_time = AccessToken.create_token(access_key_id, access_key_secret)
    print('token: %s, expire time(s): %s' % (token, expire_time))
    if expire_time:
        print('token有效期的北京时间：%s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(expire_time))))
        
    return token, expire_time

if __name__ == '__main__':
    get_token()
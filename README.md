本项目使用了阿里云的语音合成功能，需要自己去阿里云申请账号，然后在项目中配置好相关的参数,
目前阿里云是免费的，但是每个月有一定的限制，具体可以去阿里云官网查看。
https://help.aliyun.com/document_detail/374323.html是具体文档地址

# 项目开始
# 1. 安装阿里云语音合成sdk
cd 项目目录
git clone https://github.com/aliyun/alibabacloud-nls-python-sdk.git

cd alibabacloud-nls-python-sdk/ 

python setup.py install
# 2. 安装项目依赖
pip install -r requirements.txt

# 3. 配置阿里云参数
根据需求配置config.yaml文件

# 4. 运行项目
python lu_recognize.py

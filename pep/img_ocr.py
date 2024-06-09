import json
import re
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models
import base64
import os

from secure_config import read_config

config = read_config()

def create_client():
    # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
    # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
    # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
    cred = credential.Credential(config['secret_id'], config['secret_key'])
    # 实例化一个http选项，可选的，没有特殊需求可以跳过
    httpProfile = HttpProfile()
    httpProfile.endpoint = "ocr.tencentcloudapi.com"

    # 实例化一个client选项，可选的，没有特殊需求可以跳过
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    # 实例化要请求产品的client对象,clientProfile是可选的
    client = ocr_client.OcrClient(cred, "ap-beijing", clientProfile)

    # 实例化一个请求对象,每个接口都会对应一个request对象
    req = models.GeneralBasicOCRRequest()
    return req, client

def read_img(req, client, img):
    try:

        # read file from imgs/pepg3s2_07.png, then convert the data to base64 str
        with open(img, 'rb') as file:
            image_data = file.read()
            image_base64 = base64.b64encode(image_data).decode('utf-8')
        print(len(image_base64))
        params = {
            "ImageBase64": image_base64,
            "LanguageType": "zh"
        }
        
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个GeneralBasicOCRResponse的实例，与请求对象对应
        resp = client.GeneralBasicOCR(req)
        # 输出json格式的字符串回包
        return resp.to_json_string()

    except TencentCloudSDKException as err:
        print(err)


directory = 'imgs'
output = 'ocr_res'

req = None
client = None

def read_img_by_index(i):
    global req, client
    if req is None or client is None:
        req, client = create_client()
    img = f'imgs/cropped_{i}.jpg'
    if os.path.exists(img):
        jsonRes = read_img(req, client, img)
        with open(os.path.join(output, f'cropped_{i}.json'), 'w') as file:
            if jsonRes:
                file.write(jsonRes)

if __name__ == '__main__':
    read_img_by_index(130)

    exit(0)

    # for filename in os.listdir(directory):
    #     f = os.path.join(directory, filename)
    #     # checking if it is a file
    #     if os.path.isfile(f) and re.match('^cropped.*.jpg$', filename):
    #         print(f)
    #         res = read_img(req, client, f)
    #         # save res to a json file 'ocr_res/cropped_*.json'
    #         # remove extension of filename
    #         filename = re.sub('.jpg$', '', filename)
    #         with open(os.path.join(output, f'{filename}.json'), 'w') as file:
    #             if res:
    #                 file.write(res)

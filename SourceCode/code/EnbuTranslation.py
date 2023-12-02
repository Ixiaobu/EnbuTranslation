import json
from random import choice

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.tmt.v20180321 import tmt_client, models

def CreateEnbuTranslation(SecretId, SecretKey):
    # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
    # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
    # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
    cred = credential.Credential(SecretId, SecretKey)
    # 实例化一个http选项，可选的，没有特殊需求可以跳过
    httpProfile = HttpProfile()
    httpProfile.endpoint = "tmt.tencentcloudapi.com"

    # 实例化一个client选项，可选的，没有特殊需求可以跳过
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    # 实例化要请求产品的client对象,clientProfile是可选的
    client = tmt_client.TmtClient(cred, "ap-chongqing", clientProfile)
    def fun(intext):
        if not intext:
            return choice(["(⊙o⊙)？", "ಠ_ಠ", "(⌐■_■)", "( ¯(∞)¯ )", "┑(￣Д ￣)┍", "(￢︿̫̿￢☆)", "(￣(工)￣)", "༼ つ ◕_◕ ༽つ", "(lll￢ω￢)", "(+_+)?"])
        try:
            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.TextTranslateRequest()
            params = {
                "SourceText": intext,
                "Source": "auto",
                "Target": "zh",
                "ProjectId": 0
            }
            req.from_json_string(json.dumps(params))

            # 返回的resp是一个TextTranslateResponse的实例，与请求对象对应
            resp = eval(client.TextTranslate(req).to_json_string())
            # 如果输入是汉语则换为汉语
            if resp['Source'] == "zh":
                # 实例化一个请求对象,每个接口都会对应一个request对象
                req = models.TextTranslateRequest()
                params = {
                    "SourceText": intext,
                    "Source": "auto",
                    "Target": "en",
                    "ProjectId": 0
                }
                req.from_json_string(json.dumps(params))

                # 返回的resp是一个TextTranslateResponse的实例，与请求对象对应
                resp = eval(client.TextTranslate(req).to_json_string())
            # 输出
            return resp['TargetText']
        except:
            return "腾讯老大拒接了你的请求"
    return fun


if __name__ == "__main__":
    fun = CreateEnbuTranslation("AKIDtnWcoupjbQ8iDpXK5qY6qebZZP2ZBfy7", "LhQAvcIqLgHcs0weNuERTnuoX6Rn6EH8")
    print(fun("你好"))
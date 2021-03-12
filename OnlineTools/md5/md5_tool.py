from requests import utils
import time
import json
from util.CodeDemo import Code
from util.ini_xpath import HTML
from util import host
import os
import re
import urllib.parse
import urllib.request
import urllib.error
"""
    1、测试过程，cmd5网站输入验证码（验证码正确的情况）请求未成功
    2、如何提高验证码识别成功率
    3、ip被封后，如何反爬未设置
"""
class MD5(object):
    def __init__(self,md5):
        self.Textmd5 = md5
        self.cmd5_repe = 0
        self.pmd5_repe = 0
        self.path = os.path.dirname(__file__)

    def start(self):
        md5_tellyou = self.md5_tellyou()
        if md5_tellyou[0]:
            return md5_tellyou[1]
        md5_cmd5 = self.md5_cmd5()
        if md5_cmd5[0]:
            return md5_cmd5[1]
        md5_pmd5 = self.md5_pmd5()
        if md5_pmd5[0]:
            return md5_pmd5[1]
        myaddr_md5 = self.myaddr_md5()
        if myaddr_md5[0]:
            return myaddr_md5[1]
        return "未查出"
    def md5_tellyou(self):
        request_url = "http://md5.tellyou.top/default.html"
        response = host.get(request_url)
        html = HTML(response.text)
        VIEWSTATE = html.xpath('//*[@id="__VIEWSTATE"]/@value')
        VIEWSTATEGENERATOR = html.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')
        EVENTVALIDATION = html.xpath('//*[@id="__EVENTVALIDATION"]/@value')
        MD5GET="正在处理"
        request_header = {
            "Host": "md5.tellyou.top",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            "Referer": "http://md5.tellyou.top/default.html",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "1512",
            "Origin": "http://md5.tellyou.top",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        request_data = {
            "__VIEWSTATE":VIEWSTATE,
            "__VIEWSTATEGENERATOR":VIEWSTATEGENERATOR,
            "__EVENTVALIDATION":EVENTVALIDATION,
            "Textmd5":self.Textmd5,
            "MD5GET":MD5GET
        }
        response_md5 = host.post(url = request_url, headers=request_header, data=request_data)
        html_md5 = HTML(response_md5.text)
        md5_text = html_md5.xpath('//td[@class="styleh"]/span[2]//text()')
        return 1,md5_text[0]
    def md5_cmd5(self):
        request_url = "https://www.cmd5.com/"
        response = host.get(request_url)
        html = HTML(response.text)
        EVENTTARGET_xpath = html.xpath('//*[@id="__EVENTTARGET"]/@value')
        EVENTTARGET = EVENTTARGET_xpath[0] if EVENTTARGET_xpath else ""

        EVENTARGUMENT_xpath = html.xpath('//*[@id="__EVENTARGUMENT"]/@value')
        EVENTARGUMENT = EVENTARGUMENT_xpath[0] if EVENTARGUMENT_xpath else ""

        VIEWSTATE_xpath = html.xpath('//*[@id="__VIEWSTATE"]/@value')
        VIEWSTATE = VIEWSTATE_xpath[0] if VIEWSTATE_xpath else ""

        VIEWSTATEGENERATOR_xpath = html.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')
        VIEWSTATEGENERATOR = VIEWSTATEGENERATOR_xpath[0] if VIEWSTATEGENERATOR_xpath else ""
        InputHashType = "md5"
        HiddenField1_xpath = html.xpath('//*[@id="ctl00_ContentPlaceHolder1_HiddenField1"]/@value')
        HiddenField1 = HiddenField1_xpath[0] if HiddenField1_xpath else ""

        HiddenField2_xpath = html.xpath('//*[@id="ctl00_ContentPlaceHolder1_HiddenField2"]/@value')
        HiddenField2 = HiddenField2_xpath[0] if HiddenField2_xpath else ""

        request_data = {
            "__EVENTTARGET": EVENTTARGET,
            "__EVENTARGUMENT": EVENTARGUMENT,
            "__VIEWSTATE":VIEWSTATE,
            "__VIEWSTATEGENERATOR": VIEWSTATEGENERATOR,
            "ctl00$ContentPlaceHolder1$TextBoxInput": self.Textmd5,
            "ctl00$ContentPlaceHolder1$InputHashType": InputHashType,
            "ctl00$ContentPlaceHolder1$Button1": "查询",
            "ctl00$ContentPlaceHolder1$HiddenField1": HiddenField1,
            "ctl00$ContentPlaceHolder1$HiddenField2": HiddenField2
        }
        request_header = {
            "Host": "www.cmd5.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "2631",
            "Origin": "https://www.cmd5.com",
            "Connection": "keep-alive",
            "Referer": "https://www.cmd5.com/",
            "Upgrade-Insecure-Requests": "1"
        }
        response_md5 = host.post(url=request_url, headers=request_header, data=request_data)
        html_md5 = HTML(response_md5.text)
        text_md5 = html_md5.xpath('//*[@id="ctl00_ContentPlaceHolder1_table3"]/tr/td/div/span//text()')
        result_md5 = self.cmd5_get_result(request_url,request_header,request_data,text_md5)
        return result_md5

    def cmd5_get_result(self,r_url,r_header,r_data,rps):

        if "验证码错误" in rps:
            request_img_url = "https://www.cmd5.com/checkcode.aspx/0?" + self.cmd5_repe*"?"
            request_img_header = {
                "Host": "www.cmd5.com",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
                "Accept": "image/webp,*/*",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://www.cmd5.com/",
                "Connection": "keep-alive",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
                "TE": "Trailers"
            }
            response_img = host.get(url=request_img_url, headers=request_img_header)
            open(self.path+'/img/cimg.gif', 'wb').write(response_img.content)  # 将内容写入图片
            del response_img
            code_demo = Code(img_path=self.path+"/img/cimg.gif",name="cmd5", code_num=4, search_num=1)
            code_result = code_demo.get_code()
            if self.cmd5_repe > 4:
                return 0, "验证码错误"
            if code_result["code"] == 0:
                self.cmd5_repe += 1
                return self.cmd5_get_result(r_url, r_header, r_data,rps)
            else:
                r_data["ctl00$ContentPlaceHolder1$TextBoxCode"] = code_result["result"]
                response_md5 = host.post(url=r_url, headers=r_header, data=r_data)
                html_md5 = HTML(response_md5.text)
                text_md5 = html_md5.xpath('//*[@id="ctl00_ContentPlaceHolder1_table3"]/tr/td/div/span//text()')
                self.cmd5_repe += 1
                return self.cmd5_get_result(r_url,r_header,r_data,text_md5)
        elif rps[0] == "请":
            return 0, "需要登录"
        else:
            return 1, rps[0]

    def md5_pmd5(self):
        request_img_url = "https://api.pmd5.com/pmd5api/checkcode"
        res = host.get(url=request_img_url)
        if res.status_code == 200:
            if len(res.text)<100:#验证码请求失败
                res_text = json.loads(res.text)
                return 0, res_text["msg"]
            open(self.path+'/img/img.png', 'wb').write(res.content)  # 将内容写入图片
            code_demo = Code(img_path=self.path+"/img/img.png",code_num=4,search_num=3)
            code_result = code_demo.get_code()
            if self.pmd5_repe > 15:
                return 0, "验证码错误"
            if code_result["code"] == 0:
                time.sleep(1)
                self.pmd5_repe += 1
                return (self.md5_pmd5())
            else:
                cookies = res.cookies
                cookie = utils.dict_from_cookiejar(cookies)
                ck = ""
                for k in cookie:
                    ck += k + "=" + cookie[k] + ";"
                del res
                request_img_header = {
                    "accept": "*/*",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "zh-CN,zh;q=0.9",
                    "cookie": ck,
                    "origin": "https://pmd5.com",
                    "referer": "https://pmd5.com/",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-site",
                    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
                }
                request_md5_url = "https://api.pmd5.com/pmd5api/pmd5?checkcode=" + code_result["result"] + "&pwd=" + self.Textmd5
                reponse_md5 = host.get(url=request_md5_url, headers=request_img_header)
                result = json.loads(reponse_md5.text)
                if result["code"] == 403:
                    time.sleep(2)
                    self.pmd5_repe += 1
                    return (self.md5_pmd5())
                else:
                    if result["code"] == 0:
                        return 1,result["result"][self.Textmd5]
                    else:
                        return 0,result
        else:
            return 0, "pmd5_request_error"

    def myaddr_md5(self):
        site = 'http://md5.my-addr.com/'
        rest = 'md5_decrypt-md5_cracker_online/md5_decoder_tool.php'
        para = urllib.parse.urlencode({'md5': self.Textmd5}).encode("utf-8")
        req = urllib.request.Request(site + rest)
        fd = urllib.request.urlopen(req, para)
        data = fd.read().decode("utf-8")
        match = re.search('(Hashed string</span>: )(\w+.\w+)', data)
        if match: return 1,match.group(2)
        else: return 0,"not found in database"

if __name__ == "__main__":
    md5 = "e10adc3949ba59abbe56e057f20f883e"
    # md5 = "8a4f1494b0c2ea89c33f096919c5f1b0"
    md5_class = MD5(md5)
    result = md5_class.start()
    # result = md5_class.myaddr_md5()
    print(result)
    # a = md5_class.md5_cmd5()
    # print(a)

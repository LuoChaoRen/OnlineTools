import time
import re
import demjson
import json
from util.ini_xpath import HTML
from util.filter_cookie import filter_cookie
from util.xpath_filter import xfilter
from util._radom import get_radom
import util.host as host
class PING(object):
    def __init__(self,ip):
        self.ip = ip
        self.set = set()
    def get_ping(self):
        ini_req_url = "http://ping.chinaz.com/"+self.ip
        ini_req_header = {
            "Host": "ping.chinaz.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "129",
            "Origin": "http://ping.chinaz.com",
            "Connection": "keep-alive",
            "Referer": "http://ping.chinaz.com/"+self.ip,
            "Upgrade-Insecure-Requests": "1",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        }
        ini_req_data = {
            "host": self.ip,
            "linetype": "电信,多线,联通,移动,海外"
        }
        ini_res = host.post(url=ini_req_url,data=ini_req_data,headers=ini_req_header)
        ck = filter_cookie(ini_res)
        html = HTML(ini_res.text)
        guid_list = xfilter(html.xpath("//*[@id='speedlist']/div[contains(@class,'listw')]/@id"))
        city_num = len(guid_list)
        encode = xfilter(html.xpath("//*[@id='enkey']/@value"))
        ishost = xfilter(html.xpath("//*[@id='ishost']/@value"))
        isipv6 = xfilter(html.xpath("//*[@id='isipv6']/@value"))
        checktype = xfilter(html.xpath("//*[@id='checktype']/@value"))
        radom_13 = get_radom("0123456789", 13)
        request_url = "http://ping.chinaz.com/iframe.ashx?t=ping&callback=jQuery11130"+radom_13+"_"+str(int(time.time()*1000))
        request_header = {
            "Host": "ping.chinaz.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
            "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            "Referer": "http://ping.chinaz.com/"+self.ip,
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Length": "129",
            "Origin": "http://ping.chinaz.com",
            "Connection": "keep-alive",
            "Cookie": ck,
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
        }
        result_data = {"city_num":city_num}
        cont_num = 0
        for guid in guid_list:
            if guid in self.set:
                result_data["city_num"] = city_num-1
                city_num -= 1
                continue
            self.set.add(guid)
            city = xfilter(html.xpath("//*[@id='speedlist']/div[@id='"+guid+"']/div[@name='city']/text()"))
            if type(city) == list:
                city = city[0]
            request_data = {
                "guid": guid,
                "host": self.ip,
                "ishost": ishost,
                "isipv6": isipv6,
                "encode": encode,
                "checktype":checktype
            }
            response = host.post(url=request_url,data=request_data,headers=request_header)
            data_re = re.findall(".*\((.*)\)", response.text)
            data_0 = data_re[0].replace("'",'"') if data_re else ""
            data_dict = demjson.decode(data_0)
            data_json = json.loads(json.dumps(data_dict))
            cont_num += 1
            print(city_num,cont_num,city,data_json)
            result_data[str(cont_num)] = {"city":city,"result":data_json["result"]} if data_json['state']==1 else "请求超时"

        print(result_data)
        return result_data
if __name__ == "__main__":
    p = PING("106.52.58.53")
    result = p.get_ping()
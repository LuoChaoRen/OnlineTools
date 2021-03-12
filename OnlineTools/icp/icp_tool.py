from util import host
import json
import math
from urllib.parse import quote
from util.ini_xpath import HTML
from util.xpath_filter import xfilter
class ICP(object):
    def __init__(self,url_icp_companyName):
        self.url_icp_companyName = url_icp_companyName.replace("www.","")
        # self.url_icp_companyName_q =self.url_icp_companyName  if "ICP备"  in self.url_icp_companyName  else quote(self.url_icp_companyName)
        self.url_icp_companyName_q = quote(self.url_icp_companyName)
        self.result = {}
    def get_icp(self):
        request_url_1 = "http://icp.chinaz.com/"+self.url_icp_companyName_q
        request_header = {
            "Host": "icp.chinaz.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Referer": "http://icp.chinaz.com/"+self.url_icp_companyName_q,
            "Upgrade-Insecure-Requests": "1",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        }
        response_1 = host.get(url=request_url_1,headers=request_header)
        html = HTML(response_1.text)
        get_first_id = xfilter(html.xpath('//*[@id="first"]'))
        if get_first_id is not None:
            company_name = xfilter(html.xpath('//*[@id="first"]/li[1]/p/a/text()'))
            unit_properties = xfilter(html.xpath('//*[@id="first"]/li[2]/p/strong/text()'))
            icp_id = xfilter(html.xpath('//*[@id="first"]/li[3]/p/font/text()'))
            web_name = xfilter(html.xpath('//*[@id="first"]/li[4]/p/text()'))
            web_home_isture = xfilter(html.xpath('//*[@id="first"]/li[5]/span/text()'))
            if web_home_isture == "网站负责人":
                web_home_url = xfilter(html.xpath('//*[@id="first"]/li[6]/p/text()'))
                verify_time  = xfilter(html.xpath('//*[@id="first"]/li[8]/p/text()'))
            else:
                web_home_url = xfilter(html.xpath('//*[@id="first"]/li[5]/p/text()'))
                verify_time = xfilter(html.xpath('//*[@id="first"]/li[7]/p/text()'))
            self.result["icp_data"] = {
                    "company_name":company_name,
                    "unit_properties": unit_properties,
                    "icp_id": icp_id,
                    "web_name": web_name,
                    "web_home_isture": web_home_isture,
                    "web_home_url": web_home_url,
                    "verify_time": verify_time
            }
        else:
            self.result["icp_data"] = None
        request_header["Accept"]= "application/json, text/javascript, */*; q=0.01"
        request_header["Accept-Encoding"]= "gzip, deflate"
        request_header["Content-Type"]= "application/x-www-form-urlencoded; charset=UTF-8"
        request_header["X-Requested-With"]= "XMLHttpRequest"
        request_header["Content-Length"]= "13"
        request_header["Origin"]= "http://icp.chinaz.com"

        request_qiye_url = "http://icp.chinaz.com/Home/QiYeData"
        request_qiye_data = {
            "Kw" : self.url_icp_companyName
        }
        response_qiye = host.post(url=request_qiye_url,data=request_qiye_data,headers=request_header)
        response_qiye_json = json.loads(response_qiye.text)
        if response_qiye_json["code"] ==200 and response_qiye_json["data"] is not None:
            self.result["company_data"] = response_qiye_json["data"]
            #获取企业的Icp备案
            request_company_icp_url = "http://icp.chinaz.com/Home/PageData"
            request_company_icp_data = {
                "pageNo": "1",
                "pageSize": "10",
                "Kw": response_qiye_json["data"]["companyName"]
            }
            request_header["Content-Length"] = "150"
            response_company_icp = host.post(url=request_company_icp_url,data=request_company_icp_data,headers=request_header)
            response_company_icp_json = json.loads(response_company_icp.text)
            if response_company_icp_json["code"]==200:
                self.result["company_other_icp"] = self.get_page_data(response_company_icp_json["data"],request_company_icp_url,request_company_icp_data,request_header,response_company_icp_json['amount'],response_company_icp_json['pageSize'])
            else:
                self.result["company_other_icp"] = response_company_icp_json["data"]
            #获取企业注销的icp
            company_delicp_result = {}
            request_company_delicp_url = "http://icp.chinaz.com/Home/PageDelData"
            request_company_delicp_data = {
                "pageNo": "1",
                "pageSize": "10",
                "Kw": response_qiye_json["data"]["companyName"]
            }
            response_company_delicp = host.post(url=request_company_delicp_url, data=request_company_delicp_data,headers=request_header)
            response_company_delicp_json = json.loads(response_company_delicp.text)
            if response_company_delicp_json["code"] == 200:
                self.result["company_delicp"] = self.get_page_data(response_company_delicp_json["data"],request_company_delicp_url,request_company_delicp_data,request_header,response_company_delicp_json['amount'],response_company_delicp_json['pageSize'])
            else:
                self.result["company_delicp"] = response_company_delicp_json["data"]
        else:
            self.result["company_data"] = response_qiye_json["data"]
        return self.result
    def get_page_data(self,first_page,req_url,req_data,req_header,amount,pageSize):
        """
        :param first_page: 第一页数据
        :param req_url: 请求地址
        :param req_data: 请求参数
        :param req_header: 请求头
        :param amount: 数据的数量
        :param page_data_num: 每页数量
        :return:
        """
        page_data = {}
        page = math.ceil(amount / pageSize)
        page_data["page_num"] = page
        page_data["page_1"] = first_page
        p_num = 1
        while p_num < page:
            req_data["pageNo"] = str(p_num + 1)
            response_company_page = host.post(url=req_url, data=req_data,
                                              headers=req_header)
            result_icp_data = json.loads(response_company_page.text)
            page_data["page_" + str(p_num + 1)] = result_icp_data["data"]
            p_num += 1
        return page_data

if __name__ == "__main__":
    url1 = "www.chinaz.com"
    url2 = "鲁ICP备2020037903号-1"
    url3 = "sina.com.cn"
    url4 = "百度"
    icp = ICP(url3)
    result = icp.get_icp()
    print(json.dumps(result, sort_keys=True, indent=4, separators=(', ', ': '),ensure_ascii=False))
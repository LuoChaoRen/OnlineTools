from util.ini_xpath import HTML
from util import host
from util.xpath_filter import xfilter

class WS(object):
    def __init__(self,DomainName):
        self.DomainName = DomainName
        pass
    def get_whois(self):
        res_url = "http://whois.chinaz.com/"+self.DomainName
        res_header = {
                "Host": "whois.chinaz.com",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Accept-Encoding": "gzip, deflate",
                "Referer": "http://whois.chinaz.com/"+self.DomainName,
                "Content-Type": "application/x-www-form-urlencoded",
                "Content-Length": "59",
                "Origin": "http://whois.chinaz.com",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache"
        }
        res_data = {
            "DomainName": self.DomainName,
            "ws": "grs-whois.hichina.com",
            "isforceupdate": ""
        }

        response = host.post(url=res_url,data=res_data,headers=res_header)
        html = HTML(response.text)
        Domain_Name_xpath = html.xpath('//*[@id="sh_info"]/li[1]/div[2]/p[1]/a[1]/text()')#域名
        Registrar_xpath = html.xpath('//*[@id="sh_info"]/li[2]/div[2]/div/span/text()')#注册商
        ContactEmail_xpath = html.xpath('//*[@id="sh_info"]/li[3]/div[2]/span/text()')#联系邮箱
        ContactPhone_xpath = html.xpath('//*[@id="sh_info"]/li[4]/div[2]/span/text()')#联系电话
        CreationDate_xpath = html.xpath('//*[@id="sh_info"]/li[5]/div[2]/span/text()')#创建时间
        UpdatedDate_xpath = html.xpath('//*[@id="sh_info"]/li[5]/div[2]/span/text()')#更新时间
        ExpiryDate_xpath = html.xpath('//*[@id="sh_info"]/li[7]/div[2]/span/text()')#到期时间
        RegistrarServer_xpath = html.xpath('//*[@id="sh_info"]/li[8]/div[2]/span/text()')#域名服务器
        DNS = html.xpath('//*[@id="sh_info"]/li[9]/div[2]/text()')#DNS
        DomainStatus_xpath = html.xpath('//*[@id="sh_info"]/li[10]/div[2]/p/span/text()')#状态

        Domain_Name,Registrar,ContactEmail,ContactPhone = xfilter(Domain_Name_xpath,Registrar_xpath,ContactEmail_xpath,ContactPhone_xpath)
        CreationDate,UpdatedDate,ExpiryDate = xfilter(CreationDate_xpath,UpdatedDate_xpath,ExpiryDate_xpath)
        RegistrarServer,DomainStatus = xfilter(RegistrarServer_xpath,DomainStatus_xpath)

        result = {
                "域名":Domain_Name,
                "注册商": Registrar,
                "联系邮箱": ContactEmail,
                "联系电话": ContactPhone,
                "创建时间": CreationDate,
                "更新时间": UpdatedDate,
                "到期时间": ExpiryDate,
                "域名服务器": RegistrarServer,
                "DNS": DNS,
                "状态": DomainStatus,
        }
        return result


if __name__ == "__main__" :
        ws = WS("cmd5.com")
        result = ws.get_whois()
        print(result)
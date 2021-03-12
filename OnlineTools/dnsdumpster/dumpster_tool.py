import requests
from util.filter_cookie import filter_cookie
from util.ini_xpath import HTML
from util.xpath_filter import xfilter
from util.table_2_dic import get_table
class Dumpster(object):
    def __init__(self,targetip):
        self.targetip = targetip
        self.result = {}
    def get_dumpster(self):
        req_url = "https://dnsdumpster.com/"
        get_c_res = requests.get(req_url)
        cookie_dict = filter_cookie(get_c_res,get_type="dict")
        cookie_str = filter_cookie(get_c_res)
        req_data = {
            "csrfmiddlewaretoken": cookie_dict['csrftoken'],
            "targetip": self.targetip
        }
        req_header = {
                "Host": "dnsdumpster.com",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Accept-Encoding": "gzip, deflate, br",
                "Content-Type": "application/x-www-form-urlencoded",
                "Content-Length": "107",
                "Origin": "https://dnsdumpster.com",
                "Connection": "keep-alive",
                "Referer": "https://dnsdumpster.com/",
                "Cookie": cookie_str,
                "Upgrade-Insecure-Requests": "1",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
        }
        res = requests.post(req_url,data=req_data,headers =req_header )
        html = HTML(res.text)
        d_tr_text = '//*[@id="intro"]/div[1]/div[3]/div/div[4]/table/tr'
        DNS_Servers = html.xpath(d_tr_text)
        d_len = len(DNS_Servers)
        d_resu = get_table(d_len,1,None,html,d_tr_text)
        self.result["DNS_Servers"] = d_resu

        mx_tr_text = '//*[@id="intro"]/div[1]/div[3]/div/div[5]/table/tr'
        MX_Records = html.xpath(d_tr_text)
        mx_len = len(MX_Records)
        mx_resu = get_table(mx_len, 1, None, html, mx_tr_text)
        self.result["MX_Records"] = mx_resu

        tx_tr_text = '//*[@id="intro"]/div[1]/div[3]/div/div[6]/table/tr'
        TXT_Records = html.xpath(d_tr_text)
        tx_len = len(TXT_Records)
        tx_resu = get_table(tx_len, 1, None, html, tx_tr_text)
        self.result["TXT_Records"] = tx_resu

        hr_tr_text = '//*[@id="intro"]/div[1]/div[3]/div/div[7]/table/tr'
        Host_Records_A  = html.xpath(d_tr_text)
        hr_len = len(Host_Records_A)
        hr_resu = get_table(hr_len, 1, None, html, hr_tr_text)
        self.result["TXT_Records"] = hr_resu

        return self.result
if __name__ == "__main__":
    url = "imegaware.com"
    d = Dumpster(url)
    result = d.get_dumpster()
    import json
    print(json.dumps(result, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))
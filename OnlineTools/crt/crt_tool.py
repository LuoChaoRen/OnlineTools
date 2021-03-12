from util import host
from util.ini_xpath import HTML
from util.xpath_filter import xfilter
from util.table_2_dic import get_table
from util.table_2_dic import table_xdata

class CRT(object):
    def __init__(self,key):
        self.key = key
        self.result = {}
    def get_crt(self):
        REQ_URL = "https://crt.sh/?q="+self.key
        REQ_HEADER = {
            "Host": "crt.sh",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        }
        res = host.get(REQ_URL,REQ_HEADER)
        html = HTML(res.text)
        crt_shID = xfilter(html.xpath("//table[2]/tr[1]/td/a/text()"))
        Summary = xfilter(html.xpath("//table[2]/tr[2]/td/text()"))

        self.result["crt_shID"] = crt_shID
        self.result["Summary"] = Summary

        if not len(crt_shID)  and  not len(Summary):
            print({"value":None})
            return ({"value": None})
        ct_td_text = "//table[2]/tr[3]/td/div/table/tr/td[1]/table/tr"
        Certificate_Transparency = html.xpath(ct_td_text)
        ct_th = html.xpath(ct_td_text+"/th/text()")
        ct_len = len(Certificate_Transparency)-2
        ct_tr_start_num = 3
        self.result["Certificate_Transparency"] = get_table(ct_len, ct_tr_start_num, ct_th, html, ct_td_text)

        rt_td_text = "//table[2]/tr[4]/td/table/tr"
        Revocation = html.xpath(rt_td_text)
        rt_th = html.xpath(rt_td_text+"/th/text()")
        rt_len = len(Revocation)-1
        rt_tr_start_num = 2
        self.result["Revocation"] = get_table(rt_len,rt_tr_start_num,rt_th,html,rt_td_text)

        rf_td_text = "//table[2]/tr[5]/td/table/tr"
        RevoCertificate_Fingerprints= html.xpath(rf_td_text)
        rf_th = html.xpath(rf_td_text+"/th/text()")
        rf_len = len(RevoCertificate_Fingerprints)
        rf_tr_start_num = 1
        self.result["RevoCertificate_Fingerprints"] = get_table(rf_len, rf_tr_start_num, rf_th, html, rf_td_text,self.table_gdata)

        self.result["Certificate "] = html.xpath("//table[2]/tr[6]/td//text()")
        return self.result

    def table_gdata(self,td_text,tr_line,td_line,xpath_html):
        if td_line == 2:
            td_line +=1
        return table_xdata(td_text,tr_line,td_line,xpath_html)

if __name__ == "__main__":
    key = "fd62089ed7e97c3a3fcc5c17e56ba274e97b26d3"
    c = CRT(key)
    result = c.get_crt()
    import json
    print(json.dumps(result, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))
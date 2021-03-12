import json
import requests
import re

class CenSys(object):
    def __init__(self,key):
        self.key = key
        self.UID = "UID"
        self.SECRET = "SECRET"
        self.BASE_URL = "https://www.censys.io/api/v1/"

    def judge(self):
        ipv4 = re.compile(r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}')
        websites = re.compile(r'(([A-Za-z0-9-~]+)\.)+([A-Za-z0-9-~])+')
        if ipv4.search(self.key):
            return "ipv4"
        elif websites.search(self.key):
            return "websites"
        elif len(self.key)>50:
            return "certificates"
        else:
            return "ipv4"

    def search(self):
        API_URL = self.BASE_URL+"search/"+self.judge()
        data = {
            "query": self.key,  # 搜索的关键字
        }
        res = requests.post(API_URL, data=json.dumps(data), auth=(self.UID, self.SECRET))
        results = res.json()  # 获取json数据
        print(json.dumps(results, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))
        return results

    def view(self):
        API_URL = self.BASE_URL+"view/"+self.judge() +"/"+ self.key
        res = requests.get(API_URL,auth=(self.UID, self.SECRET))
        results = res.json()  # 获取json数据
        print(json.dumps(results, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))
        return results

if __name__ == "__main__":
    key = "baidu.com123"
    key2= "199.26.100.213"
    key3= "9d3b51a6b80daf76e074730f19dc01e643ca0c3127d8f48be64cf3302f6622cc"
    cne = CenSys(key3)
    # cne.search()  #端点返回用户选择字段集的最新信息的分页结果。关于返回的主机、网站和证书的更多信息可以使用view获取。
    cne.view()
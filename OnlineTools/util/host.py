import requests
def get(url,headers = None,cookies = None,**kwargs):
    get_response = requests.get(url=url,headers = headers,cookies = cookies,**kwargs)
    return get_response
def post(url,headers = None,data = None,cookies = None,**kwargs):
    post_response = requests.post(url=url,data=data,headers = headers,cookies = cookies,**kwargs)
    return post_response

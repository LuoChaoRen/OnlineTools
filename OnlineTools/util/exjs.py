import execjs
import os

def get_js(js_url,fun_name,param=None):
    f = open(js_url, 'r', encoding='UTF-8')
    line = f.readline()
    jsstr = ''
    while line:
        jsstr = jsstr + line
        line = f.readline()
    ctx = execjs.compile(jsstr)
    j = ctx.call(fun_name, param)
    return j

if __name__ == "__main__":
    path = os.path.dirname(os.path.dirname(__file__))
    res = get_js(js_url=path+"/ip/generateKey.js",fun_name="gettoken",param="103.205.5.18")
    print(res)

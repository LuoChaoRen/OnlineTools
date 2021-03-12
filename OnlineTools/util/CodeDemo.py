from PIL import Image
import pytesseract
import re

class Code(object):
    def __init__(self,img_path,name="",code_num = 4,search_num = 3):
        self.code_num = code_num #需要返回的验证码数量
        self.search_num = search_num #需要匹配的字符集:1.纯数字/2.纯字母(大小写) /3.数字+大小写字母
        self.img_path = img_path
        self.repe = 0
        self.name = name
    def get_code(self):
        if self.repe >2:#重新尝试次数
            result = {
                "code":0,
                "msg":"识别重试次数过多"
            }
            return result
        img = Image.open(self.img_path)

        if self.name == "cmd5":
            img = img.crop((3, 3, 85, 24))  # (left, upper, right, lower)
        text = pytesseract.image_to_string(img)

        if self.search_num == 1:
            rep = {'O': '0',
                   'I': '1', 'L': '1',
                   'Z': '2',
                   'S': '8'
                   }
            text = text.strip()
            text = text.upper()
            for r in rep:
                text = text.replace(r, rep[r])
            _code = re.sub(r'[^0-9]', "", text)#将非数字部分清除，下同
        elif self.search_num == 2:
            _code = re.sub(r'[^a-zA-Z]', "", text)
        else:
            _code = re.sub(r'[^0-9a-zA-Z]', "", text)
        if len(_code) != self.code_num: #识别到的验证码缺少/过多
            self.repe += 1
            return(self.get_code())
        else:
            return {"code":1,"result":_code}
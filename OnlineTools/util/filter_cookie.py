from requests import utils
def filter_cookie(res,get_type="str"):
    """
    :param res: request response
    :param get_type: 如果需要json数据，get_type="dict",如果需要headers中的str数据，默认即可
    :return:
    """
    cookies = res.cookies
    cookie = utils.dict_from_cookiejar(cookies)
    if get_type=="dict":
        return cookie
    else:
        ck = ""
        for k in cookie:
            ck += k + "=" + cookie[k] + ";"
        return ck
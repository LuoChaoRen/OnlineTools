def table_xdata(tr_text, tr_line, td_line, xpath_html):
    """
    :param tr_text: 提取tr的xpath语法，截止'/tr'不含最后'/text()'部分
    :param tr_line: 第几个tr
    :param td_line: 第几个td  为0时，自动检测td数量
    :param xpath_html:需要xpath解析的数据
    :return:xpath_result or xpath_list
    """
    if td_line>0:
        xpath_text = tr_text + "[" + tr_line + "]/td[" + str(td_line) + "]//text()"
        xpath_result = xpath_html.xpath(xpath_text)
        x_result = xpath_result[0] if len(xpath_result) == 1 else "".join(xpath_result)
        return x_result
    else:
        td_text = tr_text + "[" + tr_line + "]/td"
        td_result = xpath_html.xpath(td_text)
        td_num = len(td_result)
        x_num = 0
        x_list = []
        while td_num>0:
            xpath_text = td_text + "[" + str(x_num+1) + "]//text()"
            xpath_result = xpath_html.xpath(xpath_text)
            x_result = xpath_result[0] if len(xpath_result) == 1 else "".join(xpath_result)
            x_list.append(x_result.replace("\n",""))
            x_num += 1
            td_num -= 1
        return x_list

def get_table(tr_num, tr_start_num, th_data, xpath_html,tr_text,row_name="row", exec_def=table_xdata):
    """
    :param tr_num: 需要提取的tr行的数量（不含th行）
    :param tr_start_num: 需要提取的tr从第几行开始
    :param th_data: th行的xpath text（）数据，返回{th:td,}   没有传None，将返回[td,]
    :param xpath_html: 需要xpath解析的数据
    :param tr_text:  提取tr的xpath语法，截止'/tr'不含最后'/text()'部分
    :param row_name:  返回参数中的行名
    :param exec_def: 提取方法，可自定义
    :return:table -> json
    """
    g_table = {}
    g_num = 0
    t_num = tr_num
    while t_num > 0:
        dic_rt = {}
        if th_data != None:
            for inx, val in enumerate(th_data):
                x_tr_len = str(g_num + tr_start_num)
                x_td_len = inx + 1 #第几个td
                x_result = exec_def(tr_text, x_tr_len, x_td_len, xpath_html)

                dic_rt[val] = x_result
            g_table["row_" + str(g_num + 1)] = dic_rt
            g_num += 1
            t_num -= 1
        else:
            x_tr_len = str(g_num + tr_start_num) #第几个tr 1,2,3,4
            x_td_len = 0 #第几个td  为0时，exec_def检测td数量
            x_result = exec_def(tr_text, x_tr_len, x_td_len, xpath_html) #list
            g_table[row_name+"_" + str(g_num + 1)] = x_result
            g_num += 1
            t_num -= 1
    return g_table



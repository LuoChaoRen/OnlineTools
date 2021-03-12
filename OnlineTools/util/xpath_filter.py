import lxml
def xfilter(*xpath_result_list):
    if len(xpath_result_list) ==1:
        if len(xpath_result_list[0]) ==1:
            return  (xpath_result_list[0][0] if (type(xpath_result_list[0][0]) == lxml.etree._Element) else str(xpath_result_list[0][0])) if xpath_result_list[0]  else ""
        else:
            return [x if x else "" for x in xpath_result_list[0]]
    elif xpath_result_list:
        return [x[0] if x  else "" for x in xpath_result_list]
    else:
        return ""

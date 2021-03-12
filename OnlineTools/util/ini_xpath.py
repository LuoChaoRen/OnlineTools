import lxml.html
etree = lxml.html.etree
def HTML(html_text):
    xhtml = etree.HTML(html_text)
    return xhtml
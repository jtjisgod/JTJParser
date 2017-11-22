#coding:utf-8
"""
    @Author : JTJISGOD ( jtjisgod@gmail.com )
    @Date   : 2017-11-23
    @Usage  : This Script is Usage.
"""
import sys
import JTJParser
import extraction
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')

# It will use to base URL
url = "http://c2djzrn6qx6kupkn.onion/1.html"

# Read HTML Source ( filename is source file path )
filename = "./c2djzrn6qx6kupkn.onion/1.html"

html = open(filename, "r").read()
parser = JTJParser.JTJParser(url, html)
print parser.toJson()

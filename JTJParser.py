#coding:utf-8
"""
    @Author : JTJISGOD ( jtjisgod@gmail.com )
    @Date   : 2017-11-23
    @Usage  : For extract URL, Writer, DetectedUrl(Surface and Dark) and contact information.
              It is simple to parse.
    @Require: pip install idna
              pip install uritools
"""

from bs4 import BeautifulSoup
from urlparse import urlparse
import json
import re

class JTJParser :

    # It is Soup of BeautifulSoup
    soup = None

    data = {
        "url" : "", # Crawled URL
        "writer" : [], # Content writer
        "contact" : {
            "phone" : [],
            "sns" : []
        }, # Parsed Contact in this page
        "detectedUrl" : { # Detected Url ( Parsed )
            "darkWeb" : [], # Drak Web
            "surfaceWeb" : [] # Surface Web
        },
    }

    # This is cutter
    searchData = {
        "telegram" : [
            ["텔레", ":"],
            ["텔래", ":"],
            ["탤래", ":"],
            ["탤레", ":"]
        ],
        "wickr" : [
            ["wickr", ":"],
            ["위커", ":"],
        ],
        "kakaotalk" : [
            ["kakaotalk", ":"],
            ["카톡", ":"],
            ["카카오톡", ":"],
            ["카카오", ":"]
        ],
        "wechat" :[
            ["위챗", ":"],
            ["위쳇", ":"]
        ]
    }

    # Python 생성자
    def __init__(self, url, html) :

        originUrl = urlparse(url)
        self.soup = BeautifulSoup(html, 'lxml')

        # a tags 에서 URL 추출 후 마감처리 이후 처리
        urls = list(set(self.getUrls()))
        for i in range(0, len(urls)) :
            parsed = urlparse(urls[i])
            if not parsed.netloc :
                urls[i] = originUrl.scheme + "://" + originUrl.netloc + "/" + parsed.path
                if parsed.params : urls[i] += "?" + parsed.params
                if parsed.fragment : urls[i] += "#" + parsed.fragment
            if ".onion" in urls[i] : self.data['detectedUrl']['darkWeb'].append(urls[i])
            else : self.data['detectedUrl']['surfaceWeb'].append(urls[i])


        # Phone, Email

        # Phone
        self.data['contact']['phone'] = self.getPhone()

        # Telegram, Kakaotalk, Wechat, Wickr ...
        self.data['contact']['sns'] = self.parseSNSAccount()



    # ================= URL Parsing =================#
    def getURL(self, page):
        start_link = page.find("a href")
        if start_link == -1:
            return None, 0
        start_quote = page.find('"', start_link)
        end_quote = page.find('"', start_quote + 1)
        url = page[start_quote + 1: end_quote]
        return url, end_quote

    def getUrls(self):
        page = str(self.soup)
        urls = []
        while True:
            url, n = self.getURL(page)
            page = page[n:]
            if url:
                urls.append(url)
            else:
                break
        return urls
    # ================= URL Parsing End ==============#


    # ================= StringSearch =======================#
    def stringSearch(self, query) :
        if type(query) != list : return -1
        html = self.soup.prettify().split("\n")
        success = []
        for line in html :
            chk = 0
            for q in query :
                if q in line.replace(" ", "") : chk += 1
            if chk == len(query) :
                success.append(line)
        return success

    def parseSNSAccount(self) :
        lines = {}
        for k, v in self.searchData.items() :
            lines[k] = []
            for vs in v :
                searched = self.stringSearch(vs)
                for i in range(0, len(searched)) :
                    account = searched[i].split(":")[1].split(" ")[0].split("\t")[0].split("\n")[0]
                    if account.encode("utf-8") :
                        lines[k].append(account.encode("utf-8"))
        return lines
    # ================= StringSearch End ===================#

    # Extract phone numbers
    def getPhone(self) :
        html = str(self.soup.prettify)
        if "010-" in html :
            return "010-" + html.split("010-")[1].split(" ")[0].split("\t")[0].split("\n")[0]
        if "010 " in html :
            try :
                return "010 " + html.split("010 ")[1] + "-" + html.split("010 ")[2] + "-" + html.split("010 ")[3]
            except :
                return None
        return None


    # This is return to json
    def toJson(self) :
        return json.dumps(self.data)

# -*-coding:utf-8-*-

import json
import random
import sys
import unittest
import string
import os
import time
import zlib

from poster.encode import multipart_encode
import poster.streaminghttp
import urllib
import urllib2
import cookielib
import traceback

class Browser(object):

    def __init__(self):
        self.cj = cookielib.CookieJar()
        self.handlers = [poster.streaminghttp.StreamingHTTPHandler(),
                         poster.streaminghttp.StreamingHTTPRedirectHandler(),
                         urllib2.HTTPCookieProcessor(self.cj)]
        self.opener = urllib2.build_opener(*self.handlers)
        urllib2.install_opener(self.opener)

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
            'Referer': 'http://www.leleketang.com/lib/list31-0-0-0-0-0-0-1.shtml',
            'Host': 'www.leleketang.com',
            'Proxy-Connection': 'keep-alive',
            'RA-Sid': '7739720A-20150227-233246-a87520-32b248',
            'RA-Ver': '3.0.7',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8,zh;q=0.6,ja;q=0.4,zh-TW;q=0.2,zh-CN;q=0.2,es;q=0.2,fr;q=0.2',
            'Cache-Control': 'max-age=0',
        }
        
    def get(self, url):
        request = urllib2.Request(url, headers=self.headers)
        self.resp = urllib2.urlopen(request)
        text = self.resp.read()
        decompressed_data=zlib.decompress(text, 16+zlib.MAX_WBITS)
        return decompressed_data


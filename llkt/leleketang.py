#!/usr/bin/env python
# -*-coding:utf-8-*-

'''
抓取这个网站http://school.21cnjy.com/中所有的高中和初中名字.
'''

import os
import requests
import bs4  # pip install beautifulsoup4
from bs4 import BeautifulSoup
import os
import re
import json
import time
import zlib

from browser import Browser


http_browser = Browser()

grade_dict = {
    "17": u"初一",
    "18": u"初二",
    "19": u"初三",
    "31": u"高一",
    "32": u"高二",
    "33": u"高三"
}

def get_all_term(content, url):
    '''
    获取一个教材的所有学期
    '''
    main_div = content.find(name="div", attrs={"class": "filter_term"})
    links = main_div.findAll('a')
    res = []
    for i in links:
        href = i.attrs.get('href')
        if href == u'javascript:;':
            href = url
        else:
            href = os.path.join("http://www.leleketang.com/lib", href)
        text = i.get_text()
        res.append({"text": text, "url": href})
    return res


def get_all_version(content, url):
    '''
    获取一个学科的所有教材
    '''
    main_div = content.find(name="div", attrs={"class": "filter_version"})
    links = main_div.findAll('a')
    res = []
    for i in links:
        href = i.attrs.get('href')
        if href == u'javascript:;':
            href = url
        else:
            href = os.path.join("http://www.leleketang.com/lib", href)
        text = i.get_text()
        res.append({"text": text, "url": href})
    return res


def get_all_course(content, url):
    '''
    获取一个年级的所有学科
    '''
    main_div = content.find(name="div", attrs={"class": "filter_course"})
    links = main_div.findAll('a')
    res = []
    for i in links:
        href = i.attrs.get('href')
        if href == u'javascript:;':
            href = url
        else:
            href = os.path.join("http://www.leleketang.com/lib", href)
        text = i.get_text()
        res.append({"text": text, "url": href})
    return res


def get_grade(grade):
    url = "http://www.leleketang.com/lib/list%s-0-0-0-0-0-0-1.shtml" % grade
    r = requests.get(url)
    b = BeautifulSoup(r.content)

    d = {}
    courses = get_all_course(b, url)
    for course in courses:
        # time.sleep(0.3) # 暂停0.3秒，防止被封IP
        r = requests.get(course['url'])
        b = BeautifulSoup(r.content)
        versions = get_all_version(b, course['url'])
        for version in versions:
            # time.sleep(0.3) # 暂停0.3秒，防止被封IP
            r = requests.get(course['url'])
            b = BeautifulSoup(r.content)
            terms = get_all_term(b, course['url'])
            version['terms'] = terms
        course['versions'] = versions
    d = {'grade': grade_dict[grade],
         "courses": courses}
    return d


def get_all_question(term_url):
    print term_url

    text = http_browser.get(term_url)
    b = BeautifulSoup(text)
    
    qids = []
    cc = b.findAll(name="a", attrs={"class": "to_view"})
    for i in cc:
        qids.append(i.attrs.get("href"))
    p_next = b.find(name="a", attrs={"class": "p_next"})
    while p_next:
        url = "http://www.leleketang.com/lib/%s" % p_next.attrs.get("href")
        print url
        text = http_browser.get(url)
        b = BeautifulSoup(text)

        # time.sleep(1)
        # 获取当前页的数据
        cc = b.findAll(name="a", attrs={"class": "to_view"})
        for i in cc:
            qids.append(i.attrs.get("href"))
        p_next = b.find(name="a", attrs={"class": "p_next"})
    return qids


def step_1(grade):
    if not os.path.exists(grade):
        os.mkdir(grade)
    d = get_grade(grade)
    with open("%s/url.json" % grade, "w") as fp:
        fp.write(json.dumps(d))

def step_2(grade):
    d = json.loads(open("%s/url.json" % grade).read())
    if not os.path.exists("%s/term" % grade):
        os.mkdir("%s/term" % grade)
    for course in d['courses']:
        course_text = course['text']
        for version in course['versions']:
            version_text = version['text']
            for term in version['terms']:
                term_text = term['text']
                r = requests.get(term['url'])
                b = BeautifulSoup(r.content)
                main_div = b.find(name="div", attrs={"class": "catalog"})
                links = main_div.findAll('a')
                res = []
                for i in links:
                    href = i.attrs.get('href')
                    text = i.get_text()
                    res.append({'text': text, "url": href})
                with open(u"%s/term/%s_%s_%s.json" % (grade, course_text, version_text, term_text), "w") as fp:
                    fp.write(json.dumps(res))
                    
def step_3(grade):
    d = json.loads(open("%s/url.json" % grade).read())
    if not os.path.exists("%s/qid" % grade):
        os.mkdir("%s/qid" % grade)
    for course in d['courses'][:1]:
        course_text = course['text']
        for version in course['versions'][:1]:
            version_text = version['text']
            for term in version['terms'][:1]:
                term_text = term['text']
                # time.sleep(0.3)

                qids = get_all_question(term['url'])
                
                with open(u"%s/qid/%s_%s_%s.json" % (grade, course_text, version_text, term_text), "w") as fp:
                    fp.write(json.dumps(qids))
       

if __name__ == "__main__":
   # for i in grade_dict:
   #     step_1(i)
   #     step_2(i)
    step_3("32")

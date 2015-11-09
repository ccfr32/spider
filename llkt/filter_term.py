#!/usr/bin/env python

import json

a = json.loads(open("31/url.json").read())
b = json.loads(open("32/url.json").read())
c = json.loads(open("33/url.json").read())


aa = []
for course in a['courses']:
    for version in course['versions']:
        for term in version['terms']:
            aa.append(term['url'])

bb = []
for course in b['courses']:
    for version in course['versions']:
        for term in version['terms']:
            bb.append(term['url'])

cc = []
for course in c['courses']:
    for version in course['versions']:
        for term in version['terms']:
            cc.append(term['url'])

print len(aa), len(bb), len(cc)
print len(list(set(aa + bb + cc)))

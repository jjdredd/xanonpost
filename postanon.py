#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import xmlrpclib
import json
import time
import sys
import httplib2, urllib

data = { "jpost" : "post",
         "amen":"", 
         "subject":"",
         "name" : "",
         "email" : "",
         "pswd" : "",
         "body" : ""}
headers = {'Content-type': 'application/x-www-form-urlencoded', 
           'Referer' : 'http://x.mipt.cc/?xpost=0',
           'User-Agent' : 'BitMessage'}

if len(sys.argv) < 2 or sys.argv[1] != 'newMessage':
    exit()

api = xmlrpclib.ServerProxy("http://user:password@localhost:port/")

inboxMessages = json.loads(api.getAllInboxMessages())

if inboxMessages['inboxMessages'][-1]['toAddress'] == 'BM address that receives posts' :
    data['amen'] = inboxMessages['inboxMessages'][-1]['fromAddress'][:20]
    data['body'] = inboxMessages['inboxMessages'][-1]['message'].decode('base64')
    reply = '0'
    subject_split = inboxMessages['inboxMessages'][-1]['subject'].decode('base64').split()
    for subj_word in subject_split:
        if subj_word[:2] == '/r':
            reply = subj_word[2:]
        elif subj_word[:2] == '/n':
            data['amen'] = subj_word[2:]
        elif subj_word[:2] == '/p':
            data['pswd'] = subj_word[2:]
        else:
            data['subject'] += ' ' + subj_word
    data['subject'] = data['subject'].decode('utf_8').encode('cp1251')
    data['amen'] = data['amen'].decode('utf_8').encode('cp1251')
    data['pswd'] = data['pswd'].decode('utf_8').encode('cp1251')
    data['body'] = data['body'].decode('utf_8').encode('cp1251')
    url = 'http://x.mipt.cc/?xpost=' + reply
    headers['Referer'] = url
    h = httplib2.Http()
    h.request(url, "POST",
                     headers = headers,
                     body = urllib.urlencode(data))

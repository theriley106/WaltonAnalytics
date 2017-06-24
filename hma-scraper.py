#!/usr/bin/env python

from __future__ import print_function
import requests
import re
import sys

def scrape_hma(uri):
    r = requests.get('http://proxylist.hidemyass.com/'+uri)
    bad_class="("
    for line in r.text.splitlines():
        class_name = re.search(r'\.([a-zA-Z0-9_\-]{4})\{display:none\}', line)
        if class_name is not None:
           bad_class += class_name.group(1)+'|'

    bad_class = bad_class.rstrip('|')
    bad_class += ')'

    to_remove = '(<span class\="'+ bad_class + '">[0-9]{1,3}</span>|<span style=\"display:(none|inline)\">[0-9]{1,3}</span>|<div style="display:none">[0-9]{1,3}</div>|<span class="[a-zA-Z0-9_\-]{1,4}">|</?span>|<span style="display: inline">)'

    junk = re.compile(to_remove, flags=re.M)
    junk = junk.sub('', r.text)
    junk = junk.replace("\n", "")

    proxy_src = re.findall('([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\s*</td>\s*<td>\s*([0-9]{2,6}).{100,1200}(socks4/5|HTTPS?)', junk)
    
    list = ''
    for src in proxy_src:
        if src[2] == 'socks4/5':
            proto = 'socks5h'
        else:
            proto = src[2].lower()
        if src:
            list += proto + '://' +src[0] + ':' + src[1] + '\n'
    return(list)

if __name__ == "__main__":
    error = 'Input the number of pages to scrape. Ex:\npython hma-scraper.py 30'
    try:
        if sys.argv[1].isdigit() == True:
            input = int(sys.argv[1])
            for i in range(1,input):
                print(scrape_hma(str(i)), end = '')
        else:
            print(error)
    except:
        print(error)

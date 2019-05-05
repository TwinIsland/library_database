'''

Introduction:

This project was a part of Gargantua Project
and use to build a free and public book resources
database


Fot this program:

It contain some basic manipulation of Database and crawler

'''

from lxml import etree
import requests as rq
import random
import sqlite3
import json


class crawlerComponent:

    def __init__(self):
        '''

        initialize crawler with ipLib
        [ip, type, port]

        '''

        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'}



        ipLib = []
        url = 'https://www.xicidaili.com/nn/'
        r = etree.HTML(rq.get(url, headers=header).content)
        # //*[@id="ip_list"]/tr[2]/td[2]
        # //*[@id="ip_list"]/tr[3]/td[2]
        # //*[@id="ip_list"]/tr[101]/td[2]
        for i in range(2, 101):
            ip = r.xpath('//*[@id="ip_list"]/tr[' + str(i) + ']/td[2]/text()')[0]
            type = r.xpath('//*[@id="ip_list"]/tr[' + str(i) + ']/td[6]/text()')[0]
            port = r.xpath('//*[@id="ip_list"]/tr[' + str(i) + ']/td[3]/text()')[0]
            ipLib.append([ip, type, port])

        self.ipLib = ipLib


    def get_crawel_header(self):
        '''

        :return: header
        :return type: dict

        '''
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'}

        return header


    def get_an_ip(self):
        '''

        :param ipLib:
        :return: an random ip which can directly used by 'proxies'

        '''
        if self.ipLib == []:
            return {}
        choice = random.choice(self.ipLib)
        return {choice[1]: choice[0] + ':' + choice[2]}


class dataBase:

    def __init__(self):
        con = sqlite3.connect('library.db')
        c = con.cursor()

        self.con = con
        self.c = c

    def build_database(self):
        '''

        :return:void

        it will build a book resource database, and initialize the table0

        '''

        self.c.execute('''CREATE TABLE library (
                     book_name TEXT NOT NULL UNIQUE,
                     book_link TEXT NOT NULL UNIQUE ,
                     book_direct_link TEXT UNIQUE,
                     book_introduction TEXT
                     )''')

        self.con.commit()

    def add_book(self,book):
        '''

        :param book:[[book_name,book_link,book_direct_link],[...]]
        :return: void

        if there is no direct link, just neglect it

        '''


        for i in book:

            # if all are null
            if i[3] == '' and i[2] == '':

                print('DB add: ' + str(i[:2]))
                self.c.execute('''INSERT INTO library (book_name,book_link) 
                                  VALUES (?,?)''',i[:2])
                continue

            # if ONLY direct link is null
            if i[2] == '':

                b = i[:2]
                b.append(i[3])
                print('DB add: ' + str(b))

                self.c.execute('''INSERT INTO library (book_name,book_link,book_introduction) 
                                  VALUES (?,?,?)''',b)
                continue

            # if ONLY introduction is null
            if i[3] == '':
                print('DB add: ' + str(i[:3]))

                self.c.execute('''INSERT INTO library (book_name,book_link,book_direct_link)
                                  VALUES (?,?,?)''',i[:3])


        self.con.commit()

    def head(self):
        '''

        :return:void

        it will print the first 10 element in the database

        '''
        book = self.c.execute('''SELECT book_name,book_link,book_direct_link FROM library''')
        counter = 0


        for i in book:
            if counter>=10:
                break

            print(i)

            counter += 1


class tools:
    '''

    some tool that might be useful for developing

    '''
    def remove_database(self):
        '''

        :return: void

        remove the database

        '''
        import os

        try:
            os.remove('library.db')
        except Exception as e:
            print(str(e))



    def solveCtLink(self,originLink, crawlerComponent):

        '''

        solve the ctPan

        '''
        info = originLink.split('/')[-1].split('-')

        begin_code = originLink.split('//')[1].split('.')[0]
        uid = info[0]
        fid = info[1]

        page = etree.HTML(
            rq.get(originLink, proxies=crawlerComponent.get_an_ip(), headers=crawlerComponent.get_crawel_header()).content)

        unTreatedUrl = str(page.xpath('//*[@id="free_down_link"]/@onclick')[0][10:-7])

        chk = unTreatedUrl.split('\'')[3]

        resourceUrl = 'https://' + begin_code + '.pipipan.com/get_file_url.php?' \
                      'uid=' + uid + '' \
                      '&fid=' + fid + '' \
                      '&folder_id=0' \
                      '&fid=' + fid + '' \
                      '&file_chk=' + chk + '' \
                      '&mb=0' \
                      '&app=0'

        #print(resourceUrl)

        link = rq.get(resourceUrl, proxies=crawlerComponent.get_an_ip(),
                    headers=crawlerComponent.get_crawel_header()).content.decode().split('"')[3].replace('\/', '/')

        if link == 'message':
            link = 'error'

        return link

    def shortLink(self,original_link,baidu_short_link_token,crawlerComponent):
        '''

        :param baidu_short_link_token:
        :return: short link

        '''

        host = 'https://dwz.cn'
        path = '/admin/v2/create'
        url = host + path

        content_type = 'application/json'

        token = baidu_short_link_token

        bodys = {'url': original_link}

        headers = {'Content-Type': content_type, 'Token': token}

        response = rq.post(url=url, data=json.dumps(bodys), headers=headers, proxies=crawlerComponent.get_an_ip())


        if json.loads(response.text)['Code'] == 0:
            return json.loads(response.text)['ShortUrl']
        else:
            return original_link


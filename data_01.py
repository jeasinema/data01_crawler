#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# ----------------------------------
# File Name : data_01.py
# Purpose :
# Creation Date : 25-03-2016
# Last Modified : Sat Mar 26 14:30:30 2016
# Created By : Jeasine Ma
# ---------------------------------
import urllib
import re
import json
import datetime
from functools import wraps

class data01_crawler():
    """
    base class, define all the variables and functions
    """
    base_url = "http://data.01caijing.com/p2p"
    kind_of_data_url = (
            "/website/index-data.json?website=",     #成交指标\
            "/website/interest-data.json?website=",  #利率指标\
            "/website/period-data.json?website=",    #期限指标\
            "/borrower/index-data.json?website=",    #借款人数量\
            "/borrower/avg-data.json?website=",      #人均借款数\
            "/investor/index-data.json?website=",    #投资人数量\
            "/investor/avg-data.json?website=",      #人均投资数\
            "/website/balance-data.json?website="    #贷款余额\
                )
    kind_of_data = (
            "cjzb", 
            "lvzb", 
            "qxzb", 
            "jkrsl",
            "rjjks",
            "tzrsl",
            "rjtzs",
            "dkye" 
                )   
    num_of_kind_of_data = {
            "cjzb":2, 
            "lvzb":1, 
            "qxzb":1, 
            "jkrsl":1,
            "rjjks":1,
            "tzrsl":1,
            "rjtzs":1,
            "dkye":2 
                }
    website_url = []  #各借贷站的“website”键
    p2p_name = []

    magic_timestamp = 1427241600000   #2015-3-25
    magic_day = datetime.date(2015, 3, 25)
    """
    data为各借贷站的data，数据分层依次为dic(key=p2p_name)-dic(key=data_kind)-list(time,data)
    """
    data={}
     
    def __init__(self):
        try:
            self.website_list = open('base')
        except IOError:
            print "Please provide the p2p websites you want to crawled."
            del self
            quit()
        

    def read_website_list(self, *args, **kwargs):
        """
        get the p2p's websites on 01data
        """
        """
        insert the name of the website into it
        """
#        for i in re.finditer('[0-9,\u4e00-\u9fff]+[\s]',self.website_list):
#            self.p2p_name.append(i)
        self.website_list = self.website_list.read()
        for i in re.finditer(r'[http][a-z,A-Z,0-9,/:.-]+',self.website_list):
            print (str)(i.group(0))  #TODO:TEST
            self.get_website_url(i.group(0))
    
    def get_website_url(self, *args, **kwargs):
        """
        phrase the pages, and get the p2p's website key.
        """
        url = args[0]
        try:
            page = urllib.urlopen(url)
            page = page.read()
            target = re.search(r'(\?website=)(?P<url>[^\'\&]+)', page)
            if target != None:
                self.website_url.append(target.group('url'))
                print target.group('url')  #TODO:TEST
            else:
                raise IOError
            
            target = re.search(r'(<span class="platform_txt">)(?P<name>.+)', page)
            if target != None:
                self.p2p_name.append(target.group('name'))
                print target.group('name')  #TODO:TEST
            else:
                raise IOError
        except IOError:
            self.website_url.append('')
            self.p2p_name.append('')
    
    def get_data_p2p(self, *args, **kwargs):
        """
        get the json of each p2p(all the data)
        """ 
        data_p2p = {}  # data_p2p is a dict with key from p2p_name and its value is data_kind
        for i in range(len(self.p2p_name)):
            data_kind = {}  #data_kind is a dict with key from kind_of_data and its value is json['data']
            if i != None:
                #for j in range(1):  #TODO:TEST 
                for j in range(len(self.kind_of_data_url)): 
                    print self.base_url + self.kind_of_data_url[j] + self.website_url[i]  #TODO:TEST 
                    try:
                        json_get = urllib.urlopen(self.base_url + self.kind_of_data_url[j] + self.website_url[i]+"&groupBy=day")
                        json_get = json.load(json_get)
                        #print json_get['data']
                        #json['data'] is a list(day) of list([time,data1,data2,......])
                        data_kind[self.kind_of_data[j]] = json_get['data']
                        #data_p2p[self.p2p_name[i]] = data_kind  BUGS
                    except IOError:
                        data_kind[kind_of_data[j]] = []
                        #data_p2p[self.p2p_name[i]] = {}  BUGS
                data_p2p[self.p2p_name[i]] = data_kind
            else:
                data_p2p[self.p2p_name[i]] = {}
            self.data2csv(data_p2p[self.p2p_name[i]], self.p2p_name[i])
        #self.data = data_p2p

    def time2day(self, *args, **kwargs):
        """
        args[0] = timestamp
        return = (year,month,day)
        """
        timestamp = args[0]
        delta = timestamp - self.magic_timestamp
        delta = delta / (1000*3600*24)
        day_now = self.magic_day + datetime.timedelta(delta)
        return (day_now.year, day_now.month, day_now.day)

    def list2dic(self, *args, **kwargs):
        """
        for the day1 = [time,data1,data2.....] in kind_data_list[[day1],[day2]..]
        use time as key
        args[0] = list
        return = dict 
        """
        dic = {}
        for i in args[0]:
            dic[(str)(i[0])] = i[1:]
        return dic

    
    def data2csv(self, *args, **kwargs):
        """
        args(0) = data_p2p(single)
        args(1) = p2p_name(single)
        """
        data_p2p = args[0] 
        data_p2p_name = args[1]
        kind_data = []
        time_timestamp = []
        #for i in range(len(self.data)): #all the p2p
            #print self.p2p_name[i]  #TODO:TEST
        try:
            self.output = open("./result/"+(str)(data_p2p_name)[:-1]+'.csv','w+')
        
            self.output.write('时间,成交量（笔数）,成交额（万元）,利率指标（%）,平均借款期限（天）,借款人数量（人/次）,人均借款额,投资人数量（人）,人均投资额（万元）,还款余额（万元）,待还金额（万元）\n')
        
            self.output.writelines([(str)(data_p2p_name),'\n'])
            #data[self.p2p_name[i]] now is a dict with key from kind of data and value of list[[day1][day2]] day1 = [time,data1,data2....]

            #first step: find all the time from data[p2pname][kindofdata], print it(time is the biggest)
            time_length = 0
            time_length_max = 0
            for j in range(len(self.kind_of_data)):
                if data_p2p[self.kind_of_data[j]] != []:
                    time_length = len(data_p2p[self.kind_of_data[j]])
                    #print time_length   #TODO:TEST
                    #get all the timestamp
                    if time_length > time_length_max:
                        time_timestamp = []
                        for k in range(time_length):
                            time_timestamp.append(data_p2p[self.kind_of_data[j]][k][0])
                        #print time_timestamp   #TODO:TEST
                        time_length_max = time_length
                        

            #transform the data_p2p from dic of list to dic to dic
            data_p2p_all_kind = {}
            for j in range(len(self.kind_of_data)):
                data_p2p_all_kind[self.kind_of_data[j]] = self.list2dic(data_p2p[self.kind_of_data[j]])

            #traverse all the data by time
            for j in range(len(time_timestamp)):
                time_date = self.time2day(time_timestamp[j])
                self.output.write((str)(time_date[0])+'-'+(str)(time_date[1])+'-'+(str)(time_date[2]))
                #find every data with key in kind of data
                for k in range(len(self.kind_of_data)):
                    try:
                        kind_data = data_p2p_all_kind[self.kind_of_data[k]][(str)(time_timestamp[j])]
                    except KeyError:
                        kind_data = []
                        for l in range(self.num_of_kind_of_data[self.kind_of_data[k]]):  #compatible with those has data(first data is timestamp)
                            kind_data.append('no_data_yet')
                    finally:
                        for l in range(len(kind_data)):   #the first data is timestamp
                            self.output.write(',')
                            self.output.write((str)(kind_data[l]))       
                self.output.write('\n')
            self.output.close()
        except IOError:
            print (str)(data_p2p_name)+"data saving failure"
                
"""
TODO:
    1.不能认为kind_data的所有数据的起始时间是相同的.......   FIXED
    2.现在的逻辑默认时间是连续的
    3.excel不支持csv直接分页.....
    4.目前仍对网页列表有要求（必须为index-...）实际上只需要网站id即可
    5.目前为得到整张数据表后再一次性写入，应加以修改
"""


class p2p_list():
    
    base_url = "http://data.01caijing.com/p2p/index.html" 
    """
    this magic_num is the page amount, now is 41
    """
    page_amount = 2
    def __init__(self):
        try:
            self.output = open('./base_list','w+')
        except IOError:
            print "cannot open the p2p_list output files."
            del self
            quit()

    def get_p2p_list(self):
        for i in self.interator_get_p2p():
            if i:
                page = i.read()
                #print page      #TODO:TEST
                for j in re.finditer(r'(<a\sstyle="color:\sblack;"\shref="\/p2p\/website\/)(.+)(">)(.+)(</a>)',page): 
                    self.output.write(j.group(4))
                    print j.group(4)  #TODO:TEST
                    self.output.write('   ')
                    single_url = re.sub(r'platform-details','http://data.01caijing.com/p2p/website/index',j.group(2))
                    print single_url  #TODO:TEST
                    self.output.write(single_url + '\n')
            else:
                pass

    def interator_get_p2p(self, *args, **kwargs):
        for j in range(self.page_amount):
            page_num = j
            try:
                res = urllib.urlopen(self.base_url+'?p='+ (str)(page_num) + "&check_page=" + (str)(page_num))
                yield res
            except IOError:
                yield None
        


if __name__ == "__main__":
   # my_data01 = data01_crawler()	
   # my_data01.read_website_list()
   # print "There will be %d website to crawl"%len(my_data01.p2p_name)
   # print "start crawling"
   # my_data01.get_data_p2p()
    my_url = p2p_list()
    my_url.get_p2p_list()

    

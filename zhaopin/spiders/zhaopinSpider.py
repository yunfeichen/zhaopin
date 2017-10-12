# -*- coding:utf-8 -*-
'''
import sys
import codecs
import chardet
import scrapy
from scrapy import log
from scrapy.selector import Selector

from tutorial.items import DmozItem
'''
import pymongo
import scrapy
import os
from scrapy.http import Request
# import sys
import codecs
import re


# from tutorial.items import DmozItem

class DmozSpider(scrapy.Spider):
    name = "zhaopin"
    allowed_domains = ["zhaopin.com"]
    start_urls = [
        "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%8C%97%E4%BA%AC&kw=%E8%85%BE%E8%AE%AF&p=1&kt=2&isadv=0"]

    def parse(self, response):
        # 获取本页职位链接
        url_data = response.xpath('//div[@id="newlist_list_content_table"]//td[@class="zwmc"]//a/@href').extract()
        #        f = codecs.open(r'F:\test\tutorial\a','a','utf-8')
        #        for company_url in url_data:
        #            f.write(company_url+'\n')
        #        f.close()
        for company_url in url_data:
            yield Request(company_url, callback=self.parse2)
        # 跳转到下一页
        next_page_url = response.xpath(
            '//body/div[@class="main"]/div[@class="search_newlist_main"]/div[@class="newlist_main"]/form[@name="frmMain"]/div[@class="clearfix"]/div[@class="newlist_wrap fl"]/div[@class="pagesDown"]/ul/li[@class="pagesDown-pos"]/a/@href').extract()
        yield Request(next_page_url[0], callback=self.parse)

    def parse2(self, response):
        f = codecs.open(r'D:\zhaopin\zhaopin.json', 'a', 'utf-8')
        # 职位待遇
        try:
            pay_data = response.xpath(
                '//body/div[@class="terminalpage clearfix"]/div[@class="terminalpage-left"]/ul[@class="terminal-ul clearfix"]/li')
            pay = ''
            for sel in pay_data:
                pay_middle_data = sel.xpath('strong').extract()
                pay = pay + re.sub(r'<.*?>', '', pay_middle_data[0]) + ' '
            f.write(pay + '\n')
        except:
            pass
        # 任职要求
        try:
            require_data = response.xpath(
                '//body/div[@class="terminalpage clearfix"]/div[@class="terminalpage-left"]/div[@class="terminalpage-main clearfix"]/div[@class="tab-cont-box"]/div[1]/p').extract()
            require_data_middle = ''
            for i in require_data:
                i_middle = re.sub(r'<.*?>', r'', i, re.S)
                require_data_middle = require_data_middle + re.sub(r'\s*', r'', i_middle, re.S)
            f.write(require_data_middle + '\n')
        except:
            pass
        # 公司地址
        try:
            company_data = response.xpath(
                '//body/div[@class="terminalpage clearfix"]/div[@class="terminalpage-left"]/div[@class="terminalpage-main clearfix"]/div[@class="tab-cont-box"]/div[@class="tab-inner-cont"]/h2').extract()
            company_data = re.search(r'<h2>\s*(.*?)\s*<a', company_data[0], re.S).group(1)
            f.write(company_data + '\n')
        except:
            pass
        # 招聘信息地址
        company_url = str(response)[5:-1]
        f.write(company_url + '\n\n')

        f.close()

        conn = pymongo.MongoClient('127.0.0.1', 27017)
        db = conn.test
        employee = db.employee
        employee.insert(
            {"url": company_url, "pay": pay, "require_data": require_data_middle, "company_data": company_data})

'''
    def parse(self,response):
        f = codecs.open(r'D:\zhaopin\zhaopin.json','a','utf-8')
        #职位待遇        
        pay_data = response.xpath('//body/div[@class="terminalpage clearfix"]/div[@class="terminalpage-left"]/ul[@class="terminal-ul clearfix"]/li')
        pay = ''
        for sel in pay_data:
            try:
                pay_middle_data = sel.xpath('strong').extract()
                pay = pay + re.sub(r'<.*?>','',pay_middle_data[0]) + ' '
            except:
                pass        
        f.write(pay+'\n')
        #任职要求
        require_data = response.xpath('//body/div[@class="terminalpage clearfix"]/div[@class="terminalpage-left"]/div[@class="terminalpage-main clearfix"]/div[@class="tab-cont-box"]/div[1]/p').extract()
        require_data_middle = ''
        for i in require_data:
            i_middle = re.sub(r'<.*?>',r'',i,re.S)
            require_data_middle = require_data_middle + re.sub(r'\s*',r'',i_middle,re.S)
        f.write(require_data_middle+'\n')
        #公司地址        
        company_data = response.xpath('//body/div[@class="terminalpage clearfix"]/div[@class="terminalpage-left"]/div[@class="terminalpage-main clearfix"]/div[@class="tab-cont-box"]/div[@class="tab-inner-cont"]/h2').extract()
        company_data = re.search(r'<h2>\s*(.*?)\s*<a',company_data[0],re.S).group(1)
        f.write(company_data+'\n')
        #招聘信息地址
        company_url = str(response)[5:-1]
        f.write(company_url+'\n\n')
        f.close()
'''
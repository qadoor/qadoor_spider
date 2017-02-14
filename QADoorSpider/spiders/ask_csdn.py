# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from QADoorSpider.items import QuestionItem, AnswerItem
import time, datetime

class AskCsdnSpider(scrapy.Spider):
    name = "ask_csdn"
    allowed_domains = ["ask.csdn.net"]
    start_urls = ['http://ask.csdn.net/?type=resolved']

    #解析CSDN已解决问答URL,下一页
    def parse(self, response):

        is_out_of_date = False;
        for index,time_ele in enumerate(response.xpath("//div[@class='q_time']/span")):
            page_time = time_ele.xpath("text()").extract()[0]
            page_time = page_time.split(" ")[0]
            print("time = ", page_time)
            #对比时间
            if self.timecompare(page_time, 2) == True:
                list = response.xpath("//div[@class='questions_detail_con']/dl/dt/a")[index]
                url = list.xpath("@href").extract()[0]
                title = list.xpath("text()").extract()[0]
                #新建问题
                q_item = QuestionItem()
                q_item['reprint_link'] = url
                q_item['title'] = title
                q_item['user_id'] = 1
                q_item['votes'] = 0

                print("url = ", url)
                print("title = ", title)
                yield scrapy.Request(url, meta={'item': q_item}, callback = self.parse_answer)
            else:
                is_out_of_date = True;
                continue



        # for list in response.xpath("//div[@class='questions_detail_con']/dl/dt/a"):
        #     url = list.xpath("@href").extract()[0]
        #     title = list.xpath("text()").extract()[0]
        #     #新建问题
        #     q_item = QuestionItem()
        #     q_item['reprint_link'] = url
        #     q_item['title'] = title
        #     q_item['user_id'] = 1
        #     q_item['votes'] = 0
        #
        #     print("问题标题:")
        #     print(title)
        #
        #     yield scrapy.Request(url, meta={'item': q_item}, callback = self.parse_answer)

        if is_out_of_date == True:
            return
        else:
            #判断是否还有下一页
            lastpage = response.xpath("//span[@class='page-nav']/a[last()]/text()").extract()[0]
            if (lastpage == unicode('尾页','utf-8')):
                nextpage_url = response.xpath("//span[@class='page-nav']/a[last()-1]/@href").extract()[0]
                inner_url = "http://ask.csdn.net" + nextpage_url;
                yield scrapy.Request(inner_url, callback = self.parse)

    def parse_answer(self, response):
        #接收从上个request发来的item
        q_item = response.meta['item']

        #问题标签
        q_item['tags'] = []
        for list_tag in response.xpath("//div[@class='tags']/a"):
            tag_name = list_tag.xpath("text()").extract()[0]
            q_item['tags'].append(tag_name)

        #问题内容
        question_text = response.xpath("//div[@class='questions_detail_con']/dl/dd").extract_first()
        q_item['content'] = question_text

        #问题回答
        q_item['answers'] = []
        for answer in response.xpath("//div[@class='answer_list']/div[@class='answer_accept']/div[1] | //div[@class='answer_list']/div[@class='answer_detail_con']/div[1]"):
            a_item = AnswerItem()
            a_item['content'] = answer.extract()
            a_item['votes'] = 0
            a_item['user_id'] = 1
            q_item['answers'].append(a_item)

        yield q_item

    def timecompare(self, cmp_time_str, iday):
        #今天时间
        today = datetime.date.today()
        str_today = time.strftime("%Y-%m-%d", today.timetuple())

        # 用今天日期减掉时间差，参数为1天，获得昨天的日期
        yesterday = today - datetime.timedelta(days = iday)
        str_yesterday = time.strftime("%Y-%m-%d", yesterday.timetuple())

        # print("今天是%s, 昨天是%s" % (str_today, str_yesterday))

        yesterdayArray = time.strptime(str_yesterday, "%Y-%m-%d")
        yesterdayTimeStamp = int(time.mktime(yesterdayArray))


        cmp_Time_Array = time.strptime(cmp_time_str, "%Y.%m.%d")
        cmpTimeTimeStamp = int(time.mktime(cmp_Time_Array))

        if (cmpTimeTimeStamp >= yesterdayTimeStamp):
            return True
        else:
            return False
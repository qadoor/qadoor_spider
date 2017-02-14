# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json
import time
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from QADoorSpider.items import QuestionItem, AnswerItem

class StackoverflowSpider(scrapy.Spider):
    name = "stackoverflow"
    allowed_domains = ["stackoverflow.com"]
    start_urls = [
        'https://api.stackexchange.com/2.2/questions?key=U4DMV*8nvpm3EOpvf69Rxw((&page=1&pagesize=100&order=desc&sort=votes&site=stackoverflow'
    ]

    def start_requests(self):
        for page in range(1, 2):
            yield Request('https://api.stackexchange.com/2.2/questions?key=U4DMV*8nvpm3EOpvf69Rxw((&page={}&pagesize=100&order=desc&sort=votes&site=stackoverflow'.format(page), callback=self.parse_api)


    def parse_api(self, response):
        """解析api返回的数据"""
        # print(response.text)
        result = json.loads(response.text)
        questions = result['items']
        for q in questions:
            q_item = QuestionItem()
            q_item['reprint_link'] = q['link']
            q_item['title'] = q['title']
            q_item['user_id'] = 1
            q_item['votes'] = q['score']
            q_item['tags'] = q['tags']

            # q_item['question_id'] = q['question_id']
            # # q_item['user_id'] = q['owner']['user_id']
            # q_item['title'] = q['title']
            # q_item['reprint_link'] = q['link']
            # q_item['tags'] = ' '.join(q['tags'])
            # q_item['view_count'] = q['view_count']
            # q_item['answer_count'] = q['answer_count']
            # q_item['vote_count'] = q['score']
            # q_item['status'] = 1 if q['is_answered'] else 0
            # q_item['content'] = ''
            # q_item['created_date'] = time.strftime('%Y-%m-%d',time.localtime(q['creation_date']))
            # q_item['updated_date'] = time.strftime('%Y-%m-%d',time.localtime(q['last_edit_date']))
            # q_item['source'] = 'so'
            yield Request(url=q_item['reprint_link'], meta={'item': q_item}, callback=self.parse_answer)

    def parse_answer(self, response):
        """解析每个问题的详细内容及答案"""
        q_item = response.meta['item']
        a_item = AnswerItem()
        selector = Selector(response)
        question_text = selector.xpath('//div[@class="question"]//div[@class="post-text"]').extract_first()
        answer_text = selector.xpath('//div[@itemprop="acceptedAnswer"]//div[@class="post-text"]').extract_first()
        answer_votes = selector.xpath('//div[@itemprop="acceptedAnswer"]//span[@itemprop="upvoteCount"]/text()').extract_first()

        q_item['content'] = question_text
        q_item['answers'] = []
        a_item['content'] = answer_text
        a_item['votes'] = answer_votes
        a_item['user_id'] = 1
        q_item['answers'].append(a_item)
        # print(q_item)
        # print a_item
        # print(">>>>Item Answers = ", q_item['answers'])
        yield q_item
# -*- coding:utf-8 -*-
from scrapy import Item, Field

class QuestionItem(Item):
    reprint_link = Field()
    title = Field()
    user_id = Field()
    content = Field()
    votes = Field()
    tags = Field()
    cats = Field()
    answers = Field() #答案列表
    # id = Field()
    # user_id = Field()
    # question_id = Field()
    # status = Field()
    # answer_count = Field()
    # view_count = Field()
    # tags = Field()
    # source = Field()
    # created_date = Field()
    # updated_date = Field()

class AnswerItem(Item):
    # id = Field()
    # question_id = Field()
    content = Field()
    user_id = Field()
    votes = Field()
    # created_date = Field()
    # updated_date = Field()

# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# from mysql import connector
# from MySQLdb import connect
from contextlib import contextmanager
from .items import QuestionItem, AnswerItem
from .config import DB_CONFIG, QUESTION_TABLE, ANSWER_TABLE

#add by lucas
# -*- coding:utf-8 -*-

#import packages
from sqlalchemy import UniqueConstraint, ForeignKey, Column, Integer, Boolean, BigInteger, TIMESTAMP, Text, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.sql import func
from datetime import datetime

#create object base class
Base = declarative_base()

#define Category Object
class Category(Base):

    #table name
    __tablename__ = 'cats'

    #table structure
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    created_at = Column(TIMESTAMP, default = func.now())
    updated_at = Column(TIMESTAMP, default = func.now())
    tags = relationship('Tag', secondary='cat_tag')
    questions = relationship('Question', secondary='cat_question')

#create Tag Object
class Tag(Base):
    #table name
    __tablename__ = 'tags'

    #table structure
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    created_at = Column(TIMESTAMP, default = func.now())
    updated_at = Column(TIMESTAMP, default = func.now())
    cats = relationship('Category', secondary='cat_tag')
    questions = relationship('Question', secondary='tag_question')

#associate table
class CategoryTagLink(Base):
    #table name
    __tablename__ = 'cat_tag'

    #table structure
    id = Column(Integer, primary_key=True)
    cat_id = Column(Integer, ForeignKey('cats.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)

#define Question Object
class Question(Base):

    #table name
    __tablename__ = 'questions'

    #table structure
    id = Column(Integer, primary_key=True)
    reprint_link = Column(String(255))
    title = Column(String(255))
    user_id = Column(Integer)
    content = Column(Text)
    votes = Column(BigInteger)
    clickcount = Column(Integer)
    created_at = Column(TIMESTAMP, default = func.now())
    updated_at = Column(TIMESTAMP, default = func.now())
    tags = relationship('Tag', secondary='tag_question')
    cats = relationship('Category', secondary='cat_question')

class QuestionCategoryLink(Base):
    #table name
    __tablename__ = 'cat_question'

    #table structure
    id = Column(Integer, primary_key=True)
    cat_id = Column(Integer, ForeignKey('cats.id'), primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'), primary_key=True)

class QuestionTagLink(Base):
    #table name
    __tablename__ = 'tag_question'

    #table structure
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)

class Answer(Base):

    #table name
    __tablename__ = 'answers'

    #table structure
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    user_id = Column(Integer)
    isaccept = Column(Boolean)
    votes = Column(BigInteger)
    created_at = Column(TIMESTAMP, default = func.now())
    updated_at = Column(TIMESTAMP, default = func.now())
    question_id = Column(Integer, ForeignKey('questions.id'))
    question = relationship(Question, backref=backref('answers', uselist=True))
    # __table_args__ = (UniqueConstraint('id'))
#add by lucas

#create mysql session
engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/qadoor?charset=utf8", pool_size=20, max_overflow=5)
Session = sessionmaker(bind=engine)
session = Session()

class QadoorspiderPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        if isinstance(item, QuestionItem):
            print(">>>>Item Title = ", item['title'])
            print(">>>>Item Answers = ", item['answers'])

            #查询该问题在数据库是否存在:
            question_res = session.query(Question).filter(Question.reprint_link == item['reprint_link']).all()
            if (len(question_res) != 0):
                print("该问题已经存在!")
                return item

            q_item = Question(user_id=1, reprint_link=item['reprint_link'], title=item['title'], content=item['content'],votes=item['votes'], clickcount=0)

            print "handle Category..."
            #处理分类
            if ('android' in item['content']) or ('android' in item['title']) or ('android' in item['tags']):
                #安卓开发
                cat_one = session.query(Category).all()[0]
                q_item.cats.append(cat_one)

            elif ('javascript' in item['content']) or ('javascript' in item['title']) or ('javascript' in item['tags']):
                #前端开发
                cat_one = session.query(Category).all()[1]
                q_item.cats.append(cat_one)

            elif ('ios' in item['content']) or ('ios' in item['title']) or ('ios' in item['tags']):
                #IOS开发
                cat_one = session.query(Category).all()[2]
                q_item.cats.append(cat_one)
            else:
                #后台开发
                cat_one = session.query(Category).all()[3]
                q_item.cats.append(cat_one)
                #产品开发
                cat_two = session.query(Category).all()[4]
                q_item.cats.append(cat_two)

            print "handle Tag..."
            #处理标签
            tag_name_list = []
            tag_list = session.query(Tag).all()
            for i in tag_list:
                tag_name_list.append(i.name)
            for tag_iter in item['tags']:
                if tag_iter not in tag_name_list:
                    tag_item = Tag(name=tag_iter)
                    session.add(tag_item)
                    q_item.tags.append(tag_item)
                elif tag_iter in tag_name_list:
                    tag_find = session.query(Tag).filter(Tag.name == tag_iter).first()
                    q_item.tags.append(tag_find)

            print "handle Answer..."
            #处理回答
            for one_item in item['answers']:
                print "\n\none_item = ", one_item, "\n\n"
                a_item = Answer()
                a_item.content = one_item['content']
                a_item.votes = int(one_item['votes'])
                a_item.user_id = 1
                a_item.question = q_item
                a_item.isaccept = True
                session.add(a_item)

            print "handle question..."
            session.add(q_item)

            try:
                session.commit()
            except Exception as e:
                print "Error Commit!!!"
                session.rollback()
                session.flush() # for resetting non-commited .add()

            return item
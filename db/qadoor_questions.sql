-- MySQL dump 10.13  Distrib 5.7.9, for osx10.9 (x86_64)
--
-- Host: 192.168.10.10    Database: qadoor
-- ------------------------------------------------------
-- Server version	5.7.12-0ubuntu1.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `questions`
--

DROP TABLE IF EXISTS `questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `questions` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `question_id` bigint(20) NOT NULL UNIQUE COMMENT '问题id',
  `reprint_link` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT '转载地址url',
  `title` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT '问题标题',
  `content` text CHARACTER SET utf8 NOT NULL COMMENT '问题内容',
  `status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '问题是否解决',
  `vote_count` bigint(20) NOT NULL COMMENT '问题投票数',
  `view_count` bigint(20) NOT NULL COMMENT '问题浏览数',
  `answer_count` int(10) NOT NULL COMMENT '问题回答数',
  `created_date` timestamp NULL COMMENT '问题创建时间',
  `updated_date` timestamp NULL COMMENT '问题更新时间',
  `tags` varchar(255) NOT NULL COMMENT '问题标签',
  `source` varchar(255) NOT NULL COMMENT '来源站点',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

CREATE DATABASE  IF NOT EXISTS `biom_website` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci */;
USE `biom_website`;
-- MySQL dump 10.13  Distrib 5.5.43, for debian-linux-gnu (x86_64)
--
-- Host: biom.io    Database: biom_website
-- ------------------------------------------------------
-- Server version	5.5.42-37.1

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
-- Table structure for table `Applications`
--

DROP TABLE IF EXISTS `Applications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Applications` (
  `app_id` varchar(255) NOT NULL,
  `app_type` enum('EXTENSION','PROBE') NOT NULL,
  `public_key` longtext NOT NULL,
  PRIMARY KEY (`app_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Applications`
--

LOCK TABLES `Applications` WRITE;
/*!40000 ALTER TABLE `Applications` DISABLE KEYS */;
INSERT INTO `Applications` VALUES ('0e7655e9b04b982df6addf330d4f7f63','PROBE','-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDL6ylfNI0LQpQzOvElSExRFjsd\nk3OBHMqRn0ztbE+vSMyvb+O7ktRDSn92ZEpzT+yOr1NbglrORoN7sfCpo0aeASXj\na6I//hlkLVL/qUg/yOkdXNtVSapR0R//J9bPLoz4aY+MtsZRmI3EyYAdoCBvWZRM\nvCwBefuJTibWQClAzQIDAQAB\n-----END PUBLIC KEY-----'),('18b863486b7e6cec5016016ef46b0d25','PROBE','-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDDDD/QqibJTgydS8hLMv/WuEhV\nXx96/RtX7ktaGOjLl6OkxKGHWgIcfahdfvvG/xYFlQYcQUsgljZCzfy6Fjr0b4QJ\n1mN/BlN8Etw+qA/j7R0eG7Tqoh/SSIYGwRGBSBNlVz5ETfrArDzGqhmvTZG3yQBh\ndxT4q31ig6hYHBUBOQIDAQAB\n-----END PUBLIC KEY-----'),('31ec8a12d92d79883b0b7b4a9ed479b5','EXTENSION','-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDBbZxFq/DypAtFU1+cSH26n/ZH\nAzMSEi2ImmquLyyMs6LzTRn1ZqAaidfOXb3FfVS9BmgoTbYTkgonoHXl1bqqtZiA\nCOkNc5YziNjJrTnLU1yTcGMnRpc9vX2toULTaFMGAZc8w/JAlzpP7z5ICBCJoWRG\nZP0utn2TbiZZOEDO/wIDAQAB\n-----END PUBLIC KEY-----'),('3a9d3f79ecc2c42b9114b4300a248777','EXTENSION','-----BEGIN PUBLIC KEY----- MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCrD2qbaFzrq5QNwpucqS3+zECb M5tBnG40GkYPPZvgykHeYmtdgkzZH3gJISd8eNfGR4yRMVoP5apuDKeJSnH4lwTF z3IJNFglD95VpleIk8ldRWx08K2EpBi+WodZ5B9CBVpmeSGvrCeaxAICmrh9WcLL 4HDeKR4r6M6mGB+SrwIDAQAB -----END PUBLIC KEY-----'),('7439ef160abe4af57f0b2f567b13b242','PROBE','-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDSLIgmHJyXqmrdHLNSM2m85NBx\npHO5eXYBOliSpGRne3KQaVMX7rG/PmndjpcxNqGVVzNHG5xtDdiTK5P4AtkyOZt6\n/DW+O2UcgTpT9gOUD8fTNQCa5wu4MSwhz9TpMDEqSKQDDBYVWbcUpHLrIfd7/cGP\naP7/n7lYQUhPRG5jawIDAQAB\n-----END PUBLIC KEY-----'),('88b960b1c9805fb586810f270def7378','PROBE','-----BEGIN PUBLIC KEY----- MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCwjyQTMxfiP8a5j3i8RE8bC6hY BmCRP5wDfHofQhGI/NMXXdAiuNzrV7ob7KBkLZdLiayvOxDFsgUbXEZ3pvsh7JfD IrXsAOqflHJdLz+SR9QfZcYW5pL4704wXsXR9TwT4t3hC8m1dRaoIA4/J6aKx+VR xVc3LXHrVziB0gUfiQIDAQAB -----END PUBLIC KEY-----'),('a5140a8cf0041aa5716df93916d6130d','PROBE','-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCieAHNzPWldqznWekV32yHzGM2\nXTzrXR8FIqnoiA9+RtAA+fzrqL3eVc+lQlfjsjqRWPcwAHQMHDI2K33f+eSLSC0Q\nvyPGmyH8Lr+XiOWRHgROYKb2BbOIqxg+TqSEfNYu9BJS8P3HAEGM2oHeT11e/jC8\nc6i91SJDEJTPkOkBpwIDAQAB\n-----END PUBLIC KEY-----'),('a6e91269f71014828f6e9da3755d598f','PROBE','-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCqKvNLt6eC5lxd6BrqV62Q8pAQ\nGCFdmI9z42AeZr+PUoacbbkcG4G3uYPbWp7w1V/jkw+O7AMrE7DzDcHc+hPkMF+9\nua2NSR0QGN1LBj+CQIJRyqxPj4iqNtMheD+Mn1ApQln6hVxvxX5ajnvcn3h3UZms\nVulUV/ykRChz5/kjpQIDAQAB\n-----END PUBLIC KEY-----'),('aa3f5ec46a19943d04fe85416a8218c3','PROBE','-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCFwokPwSckkzh9e6HMRWol8etc\nnbSDAQJWyKf5ABteMjeEZm2ylst1cjK02xKiB8A5tT/4wBISHC2N6PEpiD0Fmw66\nlBzC1/90JdwORhWXP6nkLZS8bDMrBRruOe/8vzLMzqM7BqpU8sC10bVS18ufp3Yi\nBhnv4qbB78d8fKFdswIDAQAB\n-----END PUBLIC KEY-----'),('afc99893dad27c10251f17f5e01a9aee','PROBE','-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDnfHiNQLdsy5dypGepcvzMJzdg\nQcK703Dfo4Lq1407FeARJ8IVclvv1CgyFE+k0e3jh2piYsJ/UexrjUL0nylF0mMx\nGn/nbR5BWvBmmFrLBHB5niswTTa9UT+E9lm/PxlG8mmGq2mpqhf5bTmbHNv9yvm0\n1+/dj1SlLEsh0LV7uwIDAQAB\n-----END PUBLIC KEY-----'),('b65de89efe88e83d25a964e54c26d830','PROBE','-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCkO5BCm/SsTYFVIQnB760AjNeM\nhoEioHVn1kiv/IydJ2HxY57lsq0LfidEhatTPT0P1XTnrbuibKjYEJ1+wA0iA8ci\n8H++Bvp36XoHea2Y8SoyE9PuXziraBmbOWMWf65JkjSXuJLmgm92TKS6gSWtyUEr\nfWo7KCTMf3by4mLIEQIDAQAB\n-----END PUBLIC KEY-----'),('d4bee4618e35f2bf70beec8174bc3867','PROBE','-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQChDUgN7Dkicxfpf4fwLRxXjRyw\nlmqWj5t40HqR+sKJWGi7K1IlMNOJ3m5lW/2LGit2aNaPUQL0yAjMF1hCfJfozhXs\nrYtrGwTUyhdyh/z7Gle0PgOpufIsv9A/r59nX2Xg3TC/n0Z1sIu5+oOR5jjiXgYo\nadg/QBHsLcV675Y+awIDAQAB\n-----END PUBLIC KEY-----'),('d8e8fef022ea2bceacb3aed6c0e13e73','PROBE','-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDkMgy9g48SL4ghdxnflrvwzcX7\n0dJnNNqltDqM5a7QQbqolVh6ju9Y/xdJ8RExD1WcbNY3qBupq+H5TKNulRen97V/\nX2RIyEAz9T4Q9Ttt5lD3x1W1KwgSfELIlLq9gcTsdDiHvK4YqxX2pHlQMuoNEKL1\nGWNLHKz2dX7cK2nb7QIDAQAB\n-----END PUBLIC KEY-----');
/*!40000 ALTER TABLE `Applications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Devices`
--

DROP TABLE IF EXISTS `Devices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Devices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `owner` int(11) NOT NULL,
  `secureLocation` int(11) NOT NULL,
  `name` varchar(100) COLLATE latin1_general_ci NOT NULL,
  `type` enum('lock') CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `serialNumber` varchar(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `mac` varchar(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `lastPing` tinyint(1) NOT NULL,
  `dateCreated` datetime NOT NULL,
  `dateModified` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Devices`
--

LOCK TABLES `Devices` WRITE;
/*!40000 ALTER TABLE `Devices` DISABLE KEYS */;
INSERT INTO `Devices` VALUES (36,18,0,'666','lock','666','',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(37,18,0,'566','lock','777','',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(38,18,0,'666','lock','666','',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(39,18,0,'666','lock','666','',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(40,18,0,'888','lock','888','',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(41,26,0,'qwerty','lock','qwerty','',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(42,26,0,'qewrty','lock','qwerty','',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(43,18,0,'qwerty','lock','ggggg','',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(44,18,0,'qwerty','lock','ggggg','',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(45,18,0,'qwerty','lock','qwerty','',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(47,0,0,'qwerty','lock','qwerty','',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(49,4,13,'Lock4','lock','123456','',0,'0000-00-00 00:00:00','2014-08-26 17:47:54'),(54,4,14,'Lock3','lock','1234567','',0,'0000-00-00 00:00:00','2014-08-26 17:47:59'),(55,4,14,'Lock1','lock','12345','',0,'0000-00-00 00:00:00','2014-08-17 17:23:43'),(56,4,0,'Lock2','lock','123456789','',0,'0000-00-00 00:00:00','2014-09-18 23:55:26'),(57,4,11,'Lock5','lock','1234567899','',0,'0000-00-00 00:00:00','2014-08-26 23:36:39'),(58,1,0,'MyDevice1','lock','qwerty','',0,'0000-00-00 00:00:00','0000-00-00 00:00:00'),(59,4,0,'Lock7','lock','12341324','',0,'2014-07-20 00:17:01','2014-07-20 00:18:19'),(63,4,0,'Lock9','lock','28398293898','',0,'2014-07-24 08:35:48','2014-08-23 04:44:24'),(71,5,34,'qwerty','lock','qwerty','',0,'2014-10-20 18:35:06','2014-10-20 18:42:54'),(72,5,34,'qwerty','lock','qwerty','',0,'2014-10-20 18:35:40','2014-10-20 18:43:58'),(73,5,0,'qwerty','lock','qwerty','',0,'2014-10-20 18:44:34','2014-10-20 18:44:34'),(74,5,0,'qwerty','lock','qwerty','',0,'2014-10-27 14:20:25','2014-10-27 14:20:25'),(75,27,0,'Door1-buildingO, south','lock','081234234234','',0,'2014-12-08 20:37:53','2014-12-08 20:37:53'),(76,27,0,'Door1-buildingO, south','lock','081234234234','',0,'2014-12-08 23:12:03','2014-12-08 23:12:03');
/*!40000 ALTER TABLE `Devices` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`biom`@`localhost`*/ /*!50003 TRIGGER `devices_creation_time` BEFORE INSERT ON `Devices`
 FOR EACH ROW BEGIN
    SET NEW.dateCreated = NOW();
    SET NEW.dateModified = NOW();
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`biom`@`localhost`*/ /*!50003 TRIGGER `devices_modification_time` BEFORE UPDATE ON `Devices`
 FOR EACH ROW BEGIN
    SET NEW.dateModified = NOW();
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `Emails`
--

DROP TABLE IF EXISTS `Emails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Emails` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `profileId` int(11) NOT NULL,
  `email` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `verified` tinyint(1) NOT NULL DEFAULT '0',
  `primary` tinyint(1) NOT NULL DEFAULT '0',
  `extention` tinyint(1) NOT NULL,
  `date_created` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=71 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Emails`
--

LOCK TABLES `Emails` WRITE;
/*!40000 ALTER TABLE `Emails` DISABLE KEYS */;
INSERT INTO `Emails` VALUES (11,4,'ditkis@gmail.com',1,1,0,'0000-00-00 00:00:00'),(12,5,'alex@alex.com',0,1,0,'0000-00-00 00:00:00'),(13,5,'alex2@alex.com',0,0,0,'0000-00-00 00:00:00'),(14,5,'alex3@alex.com',0,0,0,'0000-00-00 00:00:00'),(16,10,'testuser1@gmail.com',0,1,0,'0000-00-00 00:00:00'),(17,11,'guest@biomio.com',0,1,1,'0000-00-00 00:00:00'),(55,11,'qwerty@qwerty.com',0,0,0,'0000-00-00 00:00:00'),(56,11,'qwerty1@qwerty.com',0,0,0,'0000-00-00 00:00:00'),(57,11,'qwerty@gmail.com',0,0,0,'0000-00-00 00:00:00'),(23,101,'test@test.com',0,0,0,'0000-00-00 00:00:00'),(27,14,'test1@gmail.com',0,1,0,'0000-00-00 00:00:00'),(28,14,'test1_1@gmail.com',0,0,0,'0000-00-00 00:00:00'),(54,11,'somenewemail@gmailc.om',1,0,0,'0000-00-00 00:00:00'),(68,11,'andriy.lobashchuk@vakoms.com.ua',0,0,0,'0000-00-00 00:00:00'),(69,22,'orrionandi@gmail.com',0,1,0,'0000-00-00 00:00:00'),(67,11,'alexander.lomov1@gmail.com',0,0,0,'0000-00-00 00:00:00'),(43,19,'test2@gmail.com',0,1,0,'0000-00-00 00:00:00'),(70,23,'test@gmail.com',0,1,0,'0000-00-00 00:00:00'),(47,20,'alex.chmykhalo@vakoms.com.ua',0,1,1,'0000-00-00 00:00:00'),(48,21,'boris.itkis@gmail.com',1,1,1,'0000-00-00 00:00:00');
/*!40000 ALTER TABLE `Emails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `EmailsData`
--

DROP TABLE IF EXISTS `EmailsData`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `EmailsData` (
  `email` varchar(255) NOT NULL,
  `pass_phrase` varchar(255) DEFAULT NULL,
  `public_pgp_key` longtext,
  `private_pgp_key` longtext,
  `user` int(11) NOT NULL,
  PRIMARY KEY (`email`),
  KEY `idx_emailsdata__user` (`user`),
  CONSTRAINT `fk_emailsdata__user` FOREIGN KEY (`user`) REFERENCES `Profiles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `EmailsData`
--

LOCK TABLES `EmailsData` WRITE;
/*!40000 ALTER TABLE `EmailsData` DISABLE KEYS */;
INSERT INTO `EmailsData` VALUES ('alex.chmykhalo@vakoms.com.ua','7lK7kkvCAwFvCcMQ','-----BEGIN PGP PUBLIC KEY BLOCK-----\n\nmI0EVV9kGgEEAPQuSh7X8eRB+qUO4wwP8V6ayPxgjFvp/2tTgNVIYu8a3j61aeaG\nW2u//b2JEyRa8FkpmvJGmA2SHnRHxMIBHXb7E2BQPLQuz4zzEKxt6fHw/XBfoQa8\nE8cWfvcO15K8DFaWW8/8FHowF6sFdyN6GBQqUhRXxGvMFydXoSDAxf+lABEBAAG0\nJUJpb01pbyA8YWxleC5jaG15a2hhbG9AdmFrb21zLmNvbS51YT6IuAQTAQIAIgUC\nVV9kGgIbLwYLCQgHAwIGFQgCCQoLBBYCAwECHgECF4AACgkQ5qSEjxXq+HmC6gQA\n5g1d8wVo9Ig3bfISz9OELA8gS8Js8Ryg7H7S4ZE3i/0hvqPSSX4+qZ2aUFId5zEf\nHNCN8p+vuoaASCXl0fmm6bhcxz6AxvLo7k7LOXEQtLFOh+NDGi9UarrrEWoWJQis\nCm09vRij/uI8C2wsnVekNPQiyslonTGwuIZ09/E91Y8=\n=oa+d\n-----END PGP PUBLIC KEY BLOCK-----\n',NULL,20),('alexander.lomov1@gmail.com','WVQTOaexDNTOVKmM','-----BEGIN PGP PUBLIC KEY BLOCK-----\n\nmI0EVXBdugEEANc9lgw/HdglXmvh77Kb+7dLKbnr9URtvDXcI0SqScWClO5FGOpl\nvDYLxSconmkp4WqhXPXpoaR/TvUnqcWsySybOXMQIPUD+5d0EBzXL7w29XKpsb1d\np4uxdaSt8FGWjv924/fTefdlVPmU6ta/zSVSn/0enWq97gPQDzuB9twPABEBAAG0\nI0Jpb01pbyA8YWxleGFuZGVyLmxvbW92MUBnbWFpbC5jb20+iLgEEwECACIFAlVw\nXboCGy8GCwkIBwMCBhUIAgkKCwQWAgMBAh4BAheAAAoJEOcuZSBHBndbFKsD/jcF\n9iwRob72gYxfZptA3UJWnKyCZaBSLov0EiM5shzRVcvgPDjDShcYOZthJn1kZ6rw\nJqQrFMgI9Qlk57JZhRa2f7/TqO6zNdNUaDHKa6ymR/4ftqtnVyuCbzQSnNFZkvT3\n/mi51YGgB7ZcDnmLJaJ0e668TP1OjnAO9je+ghuM\n=R/eK\n-----END PGP PUBLIC KEY BLOCK-----\n','-----BEGIN PGP PRIVATE KEY BLOCK-----\n\nlQH+BFVwXboBBADXPZYMPx3YJV5r4e+ym/u3Sym56/VEbbw13CNEqknFgpTuRRjq\nZbw2C8UnKJ5pKeFqoVz16aGkf071J6nFrMksmzlzECD1A/uXdBAc1y+8NvVyqbG9\nXaeLsXWkrfBRlo7/duP303n3ZVT5lOrWv80lUp/9Hp1qve4D0A87gfbcDwARAQAB\n/gMDAuKwJU1diqpJYMaBU4haz8vVCXbIqSuc+CMsovMzAM7I82NyXcFXbkWphoDF\nypr1fYyTUJw4XAa2+JUaZuonO9U+jaM6M04na3ybt8Dugk8128aH/JpICo5Gy6ox\n4ZXx5Rgop1HvLkhh5gh8JbfHXMWuMkQ7SxHYmktOBL4LkRM8clS2QhiPTv/bTlMK\n0IHE1Wfl6OiinSM4BnfgjKe9FJ5pPt7O5odYxjK+wSQLGsSEpnXZ407+AjPhDnTf\n/cqIrnNKkB4/DiwP7GiZiQonRqCh/YU4KUaWqwO9PSr4N0mJFiYZrevTe0A0mEqy\nG9J10OIx0fMIiukJ55Us1wrpgogiFeiUzXrqKYIlbUeIIjuouLbT7riJgeZdvcsq\n8mDijRzmcEDPOnAKsoVTg/my0ESPpG37hQWQAY6lXOlnJYScEHLiiT0D5oDSa3BN\nCkPcVDluhL8gvlkDSvtzlb2n2D//KDkcnSqiinXzDLNvtCNCaW9NaW8gPGFsZXhh\nbmRlci5sb21vdjFAZ21haWwuY29tPoi4BBMBAgAiBQJVcF26AhsvBgsJCAcDAgYV\nCAIJCgsEFgIDAQIeAQIXgAAKCRDnLmUgRwZ3WxSrA/43BfYsEaG+9oGMX2abQN1C\nVpysgmWgUi6L9BIjObIc0VXL4Dw4w0oXGDmbYSZ9ZGeq8CakKxTICPUJZOeyWYUW\ntn+/06juszXTVGgxymuspkf+H7arZ1crgm80EpzRWZL09/5oudWBoAe2XA55iyWi\ndHuuvEz9To5wDvY3voIbjA==\n=DhIV\n-----END PGP PRIVATE KEY BLOCK-----\n',11),('andriy.lobashchuk@vakoms.com.ua','GDYNXI4NdFgoWGgZ','-----BEGIN PGP PUBLIC KEY BLOCK-----\n\nmI0EVXBd6gEEANP4dh51YF+gFrS3f9u0FJvaz/IVFVd4tTZ6HuaDA0nUjrX03SZu\nBZzLpme8Zw6f8vdq26sLYR8COf5khI6vKAxNy8/3EXrBNbTrKAG+/bWJYJa8w6Q8\nLb/RhmIaHzAruJ5Rs30oMiRu3Rpt/XCmsUh9UwfPWeR5T3Thay/4oK0fABEBAAG0\nKEJpb01pbyA8YW5kcml5LmxvYmFzaGNodWtAdmFrb21zLmNvbS51YT6IuAQTAQIA\nIgUCVXBd6gIbLwYLCQgHAwIGFQgCCQoLBBYCAwECHgECF4AACgkQg6DF0Ztsi/5+\nBAP9Hr0fnlDcezmyQ68p+9eMK00KQYHJDwZbmv+Bpm2bvO3quOHi+MUha31Nr4X6\ng3pLlmQ3RxqcJWTbGACcKbGrJFPWWgTNtV3901q4kuPLC6DBdQAwCCxQK8Tx7bvp\nSVp0RKRvFWl41NxFM+ydkJ4AEojRWHz3mleEz+8KD76Ux1Y=\n=N80T\n-----END PGP PUBLIC KEY BLOCK-----\n',NULL,11),('orrionandi@gmail.com','V5J7FT8ypM7db8ku','-----BEGIN PGP PUBLIC KEY BLOCK-----\n\nmI0EVXBfIgEEAKA3PJOFyJrygbL+1/VWUw7A6T1/ai8x32evYd45dDH7S3hLjHwl\nsqjgLTyCI+O+jzt761TQQm2Pv7AgP68H4+M90/494uo2JW0k5YjgIz+StkQ5FjRe\nwHSJeqWzX67gGk0XPd+//Ac21jCLq+OU0HwFvvr05xTFFHy+7xxbUxsBABEBAAG0\nHUJpb01pbyA8b3JyaW9uYW5kaUBnbWFpbC5jb20+iLgEEwECACIFAlVwXyICGy8G\nCwkIBwMCBhUIAgkKCwQWAgMBAh4BAheAAAoJEJQKpKMB/fkBH1QD/00jRXxlDXGl\ncK1fM6k191vBCEXa8nyxYqebnITGwnGGLEN3s8R0AIBne0gRakVtXIEbRnfEkDF4\nBSUx6eymUMp5I/SKJwySuZLOzMg8OwA9+h8zDDE+NIdMh1LB28ty0edCNURiyVOu\n2cPjPfjxFlhvKyQIEtg4k1flsUlmvWOz\n=11lp\n-----END PGP PUBLIC KEY BLOCK-----\n','-----BEGIN PGP PRIVATE KEY BLOCK-----\n\nlQH9BFVwXyIBBACgNzyThcia8oGy/tf1VlMOwOk9f2ovMd9nr2HeOXQx+0t4S4x8\nJbKo4C08giPjvo87e+tU0EJtj7+wID+vB+PjPdP+PeLqNiVtJOWI4CM/krZEORY0\nXsB0iXqls1+u4BpNFz3fv/wHNtYwi6vjlNB8Bb769OcUxRR8vu8cW1MbAQARAQAB\n/gMDAhNDJlKkkqloYKgf4u2S3a1Yo68UOLUe7YFkfU+RLQ/9dNrOnOlGJBTqPCnw\n2hdEVD0xulhq96KZKOjjETK/HZPsoghP4cGcEIZixowGwmtxyL+YXS1GzlicFdUo\n2jmz6ZQR2P8njjL8MQYXDl2q6CEm3lT869X/mO+t/qw6GDJHow+Zu+O3pL5+PSyH\nBxd2UdCz3460TFdDRrb76UVpqGGspeuPv8Yruk9ygEWtHb0lPWr0BZXEaLuTiHXO\ngAvLkYu+FXEkPx5aqLIuQD+41ZVql2HapC4v7v/092tYukMEPb8hnb/EKkPxBmY5\n6qC47O+VSViBpsjRlB80myvcE7HRfUGl/QgLplld6IuDqMzWnKKsTwr8nHQWIT/F\neGkXXSD6gz9WZTi3u21XzheuuqVd/+OimZpNa5WyZa0y8/hH7l2HkXpgvPg9LUxO\n3DThS4gjYh++vJ/P3gCUOpegjIN4NzOuM2CRaefZYi+0HUJpb01pbyA8b3JyaW9u\nYW5kaUBnbWFpbC5jb20+iLgEEwECACIFAlVwXyICGy8GCwkIBwMCBhUIAgkKCwQW\nAgMBAh4BAheAAAoJEJQKpKMB/fkBH1QD/00jRXxlDXGlcK1fM6k191vBCEXa8nyx\nYqebnITGwnGGLEN3s8R0AIBne0gRakVtXIEbRnfEkDF4BSUx6eymUMp5I/SKJwyS\nuZLOzMg8OwA9+h8zDDE+NIdMh1LB28ty0edCNURiyVOu2cPjPfjxFlhvKyQIEtg4\nk1flsUlmvWOz\n=cKh/\n-----END PGP PRIVATE KEY BLOCK-----\n',22),('test@gmail.com','hcp7TDfMSMXkj1Fc','-----BEGIN PGP PUBLIC KEY BLOCK-----\n\nmI0EVXjoYQEEAL1Z+zBEKZCDBfaCH/mT4+GinCSu2q0oil5fKtchqQqRSxzSxk77\nvrXmsc278P9EsXhQAzaVj6JQIpefBn9fAHaxH1awx2DRDDmIGpFdwWg7LcPzTr9F\nE5JF7jZ2QoJ6PpH1BiDAmHIAOK8yEFBhA5+E97J+a9C7NsxMgTFeTesHABEBAAG0\nF0Jpb01pbyA8dGVzdEBnbWFpbC5jb20+iLgEEwECACIFAlV46GECGy8GCwkIBwMC\nBhUIAgkKCwQWAgMBAh4BAheAAAoJEEOsD6a2528pKqUEAKFcDRzrsX1IGQkQgmoO\nOZUrnTZ2eQ7+X/B5uGE4MgTsLwhUfATzuXtZ8oQWGTbhRFxHdECNPq652s1tigXR\n/yr4NrQGBdPMdEFlNwO79M0iR3cg1ONnDM+QcQ8oe4+FspQNSTGjUFK+QX6EEQBL\n7U0QGVZ9FjoesExu8S+mVWd9\n=xj+3\n-----END PGP PUBLIC KEY BLOCK-----\n','-----BEGIN PGP PRIVATE KEY BLOCK-----\n\nlQH+BFV46GEBBAC9WfswRCmQgwX2gh/5k+PhopwkrtqtKIpeXyrXIakKkUsc0sZO\n+7615rHNu/D/RLF4UAM2lY+iUCKXnwZ/XwB2sR9WsMdg0Qw5iBqRXcFoOy3D806/\nRROSRe42dkKCej6R9QYgwJhyADivMhBQYQOfhPeyfmvQuzbMTIExXk3rBwARAQAB\n/gMDAuQhDO8+unstYBpsYn0Lc5NRV2uz5r9fB/kay6YiMRL316Ycg5fR3Fvg/Sc3\ndldtgJe8Y6LR4FfBVrk+8L6e+d2Mj2EMCTbxyEOUVkBRcNJEKgHyRPlIJrj/0WGr\n71QX+hqCCdLJcg85NO979ZQk3J/UikkVAVAA0ipIjPNv7kVWjaO8+40eY3Y6jUla\npqKHiXPGQ/2SpfW+IaPZy0Sqleeh56pQqljvsKlsGAUOE0PxZvG7MofCQLyezXHz\nsDh8GolbmO0yX0HTHxpBZyDJhp7Q7rxgLWWdUDntjLaEn/xowh3XG/Sridvl+enl\ngKYbEeqTKHeoZgf8VCNfY9GrhnrQwgk1CV9kDxdoAYpF9oP5O3ILwDS1n235AIyK\ndcBFNMrJInCg25AohkUea2bDhX+yk/gWeFwu/Suqb3yK4QXgTZuLYoFxA1o5jJDw\nnNJhzZoMnQQYz6byFG+GnO6xD5vhz7KlsRi9Y5FFF37YtBdCaW9NaW8gPHRlc3RA\nZ21haWwuY29tPoi4BBMBAgAiBQJVeOhhAhsvBgsJCAcDAgYVCAIJCgsEFgIDAQIe\nAQIXgAAKCRBDrA+mtudvKSqlBAChXA0c67F9SBkJEIJqDjmVK502dnkO/l/webhh\nODIE7C8IVHwE87l7WfKEFhk24URcR3RAjT6uudrNbYoF0f8q+Da0BgXTzHRBZTcD\nu/TNIkd3INTjZwzPkHEPKHuPhbKUDUkxo1BSvkF+hBEAS+1NEBlWfRY6HrBMbvEv\nplVnfQ==\n=glXG\n-----END PGP PRIVATE KEY BLOCK-----\n',23);
/*!40000 ALTER TABLE `EmailsData` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Fingerprints`
--

DROP TABLE IF EXISTS `Fingerprints`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Fingerprints` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fingerPrintString` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `templateHeader` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `hand` enum('RIGHT','LEFT') CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `finger` enum('THUMB','INDEX','MIDDLE','RING','PINKY') CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `captureType` enum('','WEBCAM','FINGERSCAN') CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `dateCreated` datetime NOT NULL,
  `dateModified` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=121 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Fingerprints`
--

LOCK TABLES `Fingerprints` WRITE;
/*!40000 ALTER TABLE `Fingerprints` DISABLE KEYS */;
INSERT INTO `Fingerprints` VALUES (3,'26','','RIGHT','THUMB','WEBCAM','0000-00-00 00:00:00','0000-00-00 00:00:00'),(4,'26','','RIGHT','INDEX','','0000-00-00 00:00:00','0000-00-00 00:00:00'),(5,'26','','LEFT','THUMB','WEBCAM','0000-00-00 00:00:00','0000-00-00 00:00:00'),(6,'26','','LEFT','INDEX','','0000-00-00 00:00:00','0000-00-00 00:00:00'),(7,'8','','RIGHT','THUMB','','0000-00-00 00:00:00','0000-00-00 00:00:00'),(8,'8','','RIGHT','INDEX','','0000-00-00 00:00:00','0000-00-00 00:00:00'),(9,'8','','LEFT','THUMB','','0000-00-00 00:00:00','0000-00-00 00:00:00'),(10,'8','','LEFT','INDEX','','0000-00-00 00:00:00','0000-00-00 00:00:00'),(11,'','','RIGHT','MIDDLE','WEBCAM','0000-00-00 00:00:00','0000-00-00 00:00:00'),(12,'','','RIGHT','RING','WEBCAM','0000-00-00 00:00:00','0000-00-00 00:00:00'),(13,'','','RIGHT','PINKY','WEBCAM','0000-00-00 00:00:00','0000-00-00 00:00:00'),(14,'','','LEFT','MIDDLE','WEBCAM','0000-00-00 00:00:00','0000-00-00 00:00:00'),(15,'','','LEFT','RING','WEBCAM','0000-00-00 00:00:00','0000-00-00 00:00:00'),(16,'','','LEFT','PINKY','WEBCAM','0000-00-00 00:00:00','0000-00-00 00:00:00'),(17,'20','','RIGHT','THUMB','','0000-00-00 00:00:00','0000-00-00 00:00:00'),(18,'20','','RIGHT','INDEX','','0000-00-00 00:00:00','0000-00-00 00:00:00'),(19,'20','','LEFT','THUMB','','0000-00-00 00:00:00','0000-00-00 00:00:00'),(20,'20','','LEFT','INDEX','','0000-00-00 00:00:00','0000-00-00 00:00:00'),(21,'21','','RIGHT','THUMB','','0000-00-00 00:00:00','0000-00-00 00:00:00'),(22,'21','','RIGHT','INDEX','','0000-00-00 00:00:00','0000-00-00 00:00:00'),(23,'21','','LEFT','THUMB','','0000-00-00 00:00:00','0000-00-00 00:00:00'),(24,'21','','LEFT','INDEX','','0000-00-00 00:00:00','0000-00-00 00:00:00'),(25,'22','','RIGHT','THUMB','','0000-00-00 00:00:00','0000-00-00 00:00:00'),(26,'22','','RIGHT','INDEX','','0000-00-00 00:00:00','0000-00-00 00:00:00'),(27,'22','','LEFT','THUMB','','0000-00-00 00:00:00','0000-00-00 00:00:00'),(28,'22','','LEFT','INDEX','','0000-00-00 00:00:00','0000-00-00 00:00:00'),(29,'23','','RIGHT','THUMB','','0000-00-00 00:00:00','0000-00-00 00:00:00'),(30,'23','','RIGHT','INDEX','','0000-00-00 00:00:00','0000-00-00 00:00:00'),(31,'23','','LEFT','THUMB','','0000-00-00 00:00:00','0000-00-00 00:00:00'),(32,'23','','LEFT','INDEX','','0000-00-00 00:00:00','0000-00-00 00:00:00'),(33,'24','','RIGHT','THUMB','','2014-07-24 06:27:15','2014-07-24 06:27:15'),(34,'24','','RIGHT','INDEX','','2014-07-24 06:27:15','2014-07-24 06:27:15'),(35,'24','','LEFT','THUMB','','2014-07-24 06:27:16','2014-07-24 06:27:16'),(36,'24','','LEFT','INDEX','','2014-07-24 06:27:16','2014-07-24 06:27:16'),(37,'25','','RIGHT','THUMB','','2014-07-24 06:27:42','2014-07-24 06:27:42'),(38,'25','','RIGHT','INDEX','','2014-07-24 06:27:42','2014-07-24 06:27:42'),(39,'25','','LEFT','THUMB','','2014-07-24 06:27:42','2014-07-24 06:27:42'),(40,'25','','LEFT','INDEX','','2014-07-24 06:27:42','2014-07-24 06:27:42'),(41,'26','','RIGHT','THUMB','','2014-07-24 13:01:09','2014-07-24 13:01:09'),(42,'26','','RIGHT','INDEX','','2014-07-24 13:01:09','2014-07-24 13:01:09'),(43,'26','','LEFT','THUMB','','2014-07-24 13:01:09','2014-07-24 13:01:09'),(44,'26','','LEFT','INDEX','','2014-07-24 13:01:09','2014-07-24 13:01:09'),(45,'27','','RIGHT','THUMB','','2014-08-04 01:09:46','2014-08-04 01:09:46'),(46,'27','','RIGHT','INDEX','','2014-08-04 01:09:46','2014-08-04 01:09:46'),(47,'27','','LEFT','THUMB','','2014-08-04 01:09:46','2014-08-04 01:09:46'),(48,'27','','LEFT','INDEX','','2014-08-04 01:09:46','2014-08-04 01:09:46'),(49,'28','','RIGHT','THUMB','','2014-08-10 21:30:33','2014-08-10 21:30:33'),(50,'28','','RIGHT','INDEX','','2014-08-10 21:30:33','2014-08-10 21:30:33'),(51,'28','','LEFT','THUMB','','2014-08-10 21:30:33','2014-08-10 21:30:33'),(52,'28','','LEFT','INDEX','','2014-08-10 21:30:33','2014-08-10 21:30:33'),(53,'29','','RIGHT','THUMB','','2014-08-18 14:31:58','2014-08-18 14:31:58'),(54,'29','','RIGHT','INDEX','','2014-08-18 14:31:58','2014-08-18 14:31:58'),(55,'29','','LEFT','THUMB','','2014-08-18 14:31:58','2014-08-18 14:31:58'),(56,'29','','LEFT','INDEX','','2014-08-18 14:31:58','2014-08-18 14:31:58'),(57,'30','','RIGHT','THUMB','','2014-08-31 05:38:24','2014-08-31 05:38:24'),(58,'30','','RIGHT','INDEX','','2014-08-31 05:38:24','2014-08-31 05:38:24'),(59,'30','','LEFT','THUMB','','2014-08-31 05:38:24','2014-08-31 05:38:24'),(60,'30','','LEFT','INDEX','','2014-08-31 05:38:24','2014-08-31 05:38:24'),(61,'31','','RIGHT','THUMB','','2014-08-31 05:40:06','2014-08-31 05:40:06'),(62,'31','','RIGHT','INDEX','','2014-08-31 05:40:06','2014-08-31 05:40:06'),(63,'31','','LEFT','THUMB','','2014-08-31 05:40:06','2014-08-31 05:40:06'),(64,'31','','LEFT','INDEX','','2014-08-31 05:40:06','2014-08-31 05:40:06'),(65,'32','','RIGHT','THUMB','','2014-08-31 16:51:26','2014-08-31 16:51:26'),(66,'32','','RIGHT','INDEX','','2014-08-31 16:51:26','2014-08-31 16:51:26'),(67,'32','','LEFT','THUMB','','2014-08-31 16:51:26','2014-08-31 16:51:26'),(68,'32','','LEFT','INDEX','','2014-08-31 16:51:26','2014-08-31 16:51:26'),(69,'33','','RIGHT','THUMB','','2014-08-31 16:53:07','2014-08-31 16:53:07'),(70,'33','','RIGHT','INDEX','','2014-08-31 16:53:08','2014-08-31 16:53:08'),(71,'33','','LEFT','THUMB','','2014-08-31 16:53:08','2014-08-31 16:53:08'),(72,'33','','LEFT','INDEX','','2014-08-31 16:53:08','2014-08-31 16:53:08'),(73,'34','','RIGHT','THUMB','','2014-08-31 17:05:07','2014-08-31 17:05:07'),(74,'34','','RIGHT','INDEX','','2014-08-31 17:05:07','2014-08-31 17:05:07'),(75,'34','','LEFT','THUMB','','2014-08-31 17:05:07','2014-08-31 17:05:07'),(76,'34','','LEFT','INDEX','','2014-08-31 17:05:07','2014-08-31 17:05:07'),(77,'35','','RIGHT','THUMB','','2014-08-31 17:11:16','2014-08-31 17:11:16'),(78,'35','','RIGHT','INDEX','','2014-08-31 17:11:16','2014-08-31 17:11:16'),(79,'35','','LEFT','THUMB','','2014-08-31 17:11:16','2014-08-31 17:11:16'),(80,'35','','LEFT','INDEX','','2014-08-31 17:11:17','2014-08-31 17:11:17'),(81,'36','','RIGHT','THUMB','','2014-08-31 17:16:25','2014-08-31 17:16:25'),(82,'36','','RIGHT','INDEX','','2014-08-31 17:16:25','2014-08-31 17:16:25'),(83,'36','','LEFT','THUMB','','2014-08-31 17:16:25','2014-08-31 17:16:25'),(84,'36','','LEFT','INDEX','','2014-08-31 17:16:25','2014-08-31 17:16:25'),(85,'37','','RIGHT','THUMB','','2014-08-31 17:17:05','2014-08-31 17:17:05'),(86,'37','','RIGHT','INDEX','','2014-08-31 17:17:05','2014-08-31 17:17:05'),(87,'37','','LEFT','THUMB','','2014-08-31 17:17:05','2014-08-31 17:17:05'),(88,'37','','LEFT','INDEX','','2014-08-31 17:17:05','2014-08-31 17:17:05'),(89,'38','','RIGHT','THUMB','','2014-08-31 17:18:30','2014-08-31 17:18:30'),(90,'38','','RIGHT','INDEX','','2014-08-31 17:18:30','2014-08-31 17:18:30'),(91,'38','','LEFT','THUMB','','2014-08-31 17:18:30','2014-08-31 17:18:30'),(92,'38','','LEFT','INDEX','','2014-08-31 17:18:30','2014-08-31 17:18:30'),(93,'39','','RIGHT','THUMB','','2014-08-31 17:20:24','2014-08-31 17:20:24'),(94,'39','','RIGHT','INDEX','','2014-08-31 17:20:24','2014-08-31 17:20:24'),(95,'39','','LEFT','THUMB','','2014-08-31 17:20:24','2014-08-31 17:20:24'),(96,'39','','LEFT','INDEX','','2014-08-31 17:20:24','2014-08-31 17:20:24'),(97,'40','','RIGHT','THUMB','','2014-08-31 17:25:51','2014-08-31 17:25:51'),(98,'40','','RIGHT','INDEX','','2014-08-31 17:25:51','2014-08-31 17:25:51'),(99,'40','','LEFT','THUMB','','2014-08-31 17:25:51','2014-08-31 17:25:51'),(100,'40','','LEFT','INDEX','','2014-08-31 17:25:51','2014-08-31 17:25:51'),(101,'41','','RIGHT','THUMB','','2014-08-31 18:25:12','2014-08-31 18:25:12'),(102,'41','','RIGHT','INDEX','','2014-08-31 18:25:12','2014-08-31 18:25:12'),(103,'41','','LEFT','THUMB','','2014-08-31 18:25:12','2014-08-31 18:25:12'),(104,'41','','LEFT','INDEX','','2014-08-31 18:25:12','2014-08-31 18:25:12'),(105,'42','','RIGHT','THUMB','','2014-08-31 18:38:09','2014-08-31 18:38:09'),(106,'42','','RIGHT','INDEX','','2014-08-31 18:38:09','2014-08-31 18:38:09'),(107,'42','','LEFT','THUMB','','2014-08-31 18:38:09','2014-08-31 18:38:09'),(108,'42','','LEFT','INDEX','','2014-08-31 18:38:09','2014-08-31 18:38:09'),(109,'43','','RIGHT','THUMB','','2014-09-06 03:50:16','2014-09-06 03:50:16'),(110,'43','','RIGHT','INDEX','','2014-09-06 03:50:16','2014-09-06 03:50:16'),(111,'43','','LEFT','THUMB','','2014-09-06 03:50:16','2014-09-06 03:50:16'),(112,'43','','LEFT','INDEX','','2014-09-06 03:50:16','2014-09-06 03:50:16'),(113,'44','','RIGHT','THUMB','','2014-09-06 17:31:44','2014-09-06 17:31:44'),(114,'44','','RIGHT','INDEX','','2014-09-06 17:31:44','2014-09-06 17:31:44'),(115,'44','','LEFT','THUMB','','2014-09-06 17:31:44','2014-09-06 17:31:44'),(116,'44','','LEFT','INDEX','','2014-09-06 17:31:44','2014-09-06 17:31:44'),(117,'45','','RIGHT','THUMB','','2014-09-11 22:55:45','2014-09-11 22:55:45'),(118,'45','','RIGHT','INDEX','','2014-09-11 22:55:45','2014-09-11 22:55:45'),(119,'45','','LEFT','THUMB','','2014-09-11 22:55:45','2014-09-11 22:55:45'),(120,'45','','LEFT','INDEX','','2014-09-11 22:55:45','2014-09-11 22:55:45');
/*!40000 ALTER TABLE `Fingerprints` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`biom`@`localhost`*/ /*!50003 TRIGGER `fingerprints_creation_time` BEFORE INSERT ON `Fingerprints`
 FOR EACH ROW BEGIN
    SET NEW.dateCreated = NOW();
    SET NEW.dateModified = NOW();
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`biom`@`localhost`*/ /*!50003 TRIGGER `fingerprints_modification_time` BEFORE UPDATE ON `Fingerprints`
 FOR EACH ROW BEGIN
    SET NEW.dateModified = NOW();
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `Phones`
--

DROP TABLE IF EXISTS `Phones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Phones` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `profileId` int(11) NOT NULL,
  `phone` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `date_created` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Phones`
--

LOCK TABLES `Phones` WRITE;
/*!40000 ALTER TABLE `Phones` DISABLE KEYS */;
INSERT INTO `Phones` VALUES (1,120,'15039840867','0000-00-00 00:00:00'),(2,120,'11111111111','0000-00-00 00:00:00'),(7,11,'15039840867','0000-00-00 00:00:00');
/*!40000 ALTER TABLE `Phones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Policies`
--

DROP TABLE IF EXISTS `Policies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Policies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `owner` int(11) NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `bioAuth` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `minAuth` int(11) NOT NULL,
  `maxAuth` int(11) NOT NULL,
  `matchCertainty` int(11) NOT NULL,
  `geoRestriction` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `timeRestriction` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `dateCreated` datetime NOT NULL,
  `dateModified` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Policies`
--

LOCK TABLES `Policies` WRITE;
/*!40000 ALTER TABLE `Policies` DISABLE KEYS */;
INSERT INTO `Policies` VALUES (1,18,'qwerty','',1,2,0,'','','0000-00-00 00:00:00','0000-00-00 00:00:00'),(13,18,'qwerty2','',1,2,90,'','','0000-00-00 00:00:00','0000-00-00 00:00:00'),(14,6,'test','bioAuth',1,2,90,'','','0000-00-00 00:00:00','0000-00-00 00:00:00'),(15,4,'Main','',1,2,95,'orldwide','Anytime','0000-00-00 00:00:00','0000-00-00 00:00:00'),(16,4,'Policy2','',0,0,0,'','','0000-00-00 00:00:00','0000-00-00 00:00:00'),(18,4,'Policy3','Dedicated fingerprint scanner',6,66,666,'orldwide','Anytime','0000-00-00 00:00:00','0000-00-00 00:00:00'),(19,4,'Office','',1,2,90,'','','0000-00-00 00:00:00','0000-00-00 00:00:00'),(20,3,'test_policy','',1,2,90,'','','0000-00-00 00:00:00','0000-00-00 00:00:00'),(21,22,'test','',1,2,90,'','','0000-00-00 00:00:00','0000-00-00 00:00:00'),(22,4,'Policy4','',1,2,90,'','','2014-07-24 10:03:33','2014-07-24 10:03:33'),(24,65,'Daytime access','',1,2,90,'','','2014-10-10 17:26:13','2014-10-10 17:26:13'),(25,5,'qwerty','',1,2,90,'','','2014-10-13 16:58:27','2014-10-13 16:58:27'),(26,5,'qwerty','',1,2,90,'','','2014-10-13 16:58:33','2014-10-13 16:58:33'),(27,5,'qwerty','',1,2,90,'','','2014-10-20 16:33:19','2014-10-20 16:33:19'),(28,5,'qwerty','',1,2,90,'','','2014-10-20 18:30:55','2014-10-20 18:30:55'),(29,5,'qwerty','',1,2,90,'','','2014-10-20 18:33:45','2014-10-20 18:33:45'),(30,5,'qwerty','',1,2,90,'','','2014-10-20 18:34:08','2014-10-20 18:34:08'),(31,27,'Daily 7am-5pm','',1,2,90,'','','2014-12-08 20:30:34','2014-12-08 20:30:34'),(32,106,'Physical','',1,2,90,'','','2015-03-26 14:25:23','2015-03-26 14:25:23'),(33,0,'','',0,0,0,'','','2015-04-10 14:45:08','2015-04-10 14:45:08'),(34,0,'','',0,0,0,'','','2015-04-10 14:45:58','2015-04-10 14:45:58'),(35,0,'','',0,0,0,'','','2015-04-10 14:47:53','2015-04-10 14:47:53');
/*!40000 ALTER TABLE `Policies` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`biom`@`localhost`*/ /*!50003 TRIGGER `policies_creation_time` BEFORE INSERT ON `Policies`
 FOR EACH ROW BEGIN
    SET NEW.dateCreated = NOW();
    SET NEW.dateModified = NOW();
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`biom`@`localhost`*/ /*!50003 TRIGGER `policies_modification_time` BEFORE UPDATE ON `Policies`
 FOR EACH ROW BEGIN
    SET NEW.dateModified = NOW();
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `Profiles`
--

DROP TABLE IF EXISTS `Profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Profiles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `api_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `emails` varchar(255) NOT NULL DEFAULT '[]',
  `phones` varchar(255) NOT NULL,
  `password` varchar(50) NOT NULL,
  `temp_pass` varchar(50) NOT NULL,
  `type` enum('ADMIN','USER','PROVIDER','PARTNER') NOT NULL,
  `acc_type` tinyint(1) NOT NULL,
  `creation_time` datetime NOT NULL,
  `last_login_time` datetime NOT NULL,
  `last_ip` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Profiles`
--

LOCK TABLES `Profiles` WRITE;
/*!40000 ALTER TABLE `Profiles` DISABLE KEYS */;
INSERT INTO `Profiles` VALUES (4,11,'danit','[\"dan@biom.io\"]','[\'11111111111\']','alink1a','','USER',0,'0000-00-00 00:00:00','0000-00-00 00:00:00','24.21.108.35'),(6,1,'admin','[\"admin@admin.com\"]','','qwerty1234','','USER',0,'0000-00-00 00:00:00','0000-00-00 00:00:00','50.43.34.130'),(8,16,'ditkis','[\"ditkis@gmail.com\"]','','qwerty1234','','USER',0,'0000-00-00 00:00:00','0000-00-00 00:00:00','50.43.34.130'),(9,0,'','[]','','','','USER',0,'0000-00-00 00:00:00','0000-00-00 00:00:00','50.43.34.130'),(10,0,'','[]','','','','USER',0,'0000-00-00 00:00:00','0000-00-00 00:00:00','50.43.34.130'),(11,0,'','[]','','','','USER',0,'0000-00-00 00:00:00','0000-00-00 00:00:00','67.136.129.196'),(14,0,'','[]','','','','USER',0,'0000-00-00 00:00:00','0000-00-00 00:00:00','50.43.34.130'),(18,0,'','[]','','','','USER',0,'0000-00-00 00:00:00','0000-00-00 00:00:00','91.237.240.1'),(19,0,'','[]','','','','USER',0,'0000-00-00 00:00:00','0000-00-00 00:00:00','50.43.34.130'),(20,0,'','[]','','','','USER',0,'0000-00-00 00:00:00','0000-00-00 00:00:00','91.237.240.1'),(21,0,'','[]','','','','USER',0,'0000-00-00 00:00:00','0000-00-00 00:00:00','99.185.41.175'),(22,0,'','[]','','','','USER',0,'0000-00-00 00:00:00','0000-00-00 00:00:00','91.237.240.1'),(23,0,'','[]','','','','USER',0,'0000-00-00 00:00:00','0000-00-00 00:00:00','50.43.34.130');
/*!40000 ALTER TABLE `Profiles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ProviderInfo`
--

DROP TABLE IF EXISTS `ProviderInfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ProviderInfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `profileId` int(11) NOT NULL,
  `title` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `description` text COLLATE utf8_unicode_ci NOT NULL,
  `mission` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `address` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '{"street1":"", "street2":"", "continent": "", "country": "", "province": "", "region": "", "city": "","postcode": ""}',
  `founded` year(4) NOT NULL,
  `socialBar` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT '{"facebook":"", "twitter":"", "linkedin": "", "google": ""}',
  `products` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `size` enum('1-2','<15','<200','<1000','>1000') COLLATE utf8_unicode_ci NOT NULL,
  `notifications` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '[0, 0, 0]',
  `dateCreated` datetime NOT NULL,
  `dateModified` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=127 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ProviderInfo`
--

LOCK TABLES `ProviderInfo` WRITE;
/*!40000 ALTER TABLE `ProviderInfo` DISABLE KEYS */;
INSERT INTO `ProviderInfo` VALUES (107,4,'','','','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}',0000,'{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','','1-2','[0, 0, 0]','2015-04-15 18:49:39','2015-04-15 18:49:39'),(108,5,'','','','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}',0000,'{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','','1-2','[0, 0, 0]','2015-04-15 18:50:02','2015-04-15 18:50:02'),(109,6,'','','','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}',0000,'{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','','1-2','[0, 0, 0]','2015-04-20 08:16:30','2015-04-20 08:16:30'),(110,7,'','','','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}',0000,'{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','','1-2','[0, 0, 0]','2015-04-20 08:23:13','2015-04-20 08:23:13'),(111,8,'','','','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}',0000,'{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','','1-2','[0, 0, 0]','2015-04-20 08:27:19','2015-04-20 08:27:19'),(112,9,'','','','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}',0000,'{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','','1-2','[0, 0, 0]','2015-04-22 01:40:01','2015-04-22 01:40:01'),(113,10,'','','','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}',0000,'{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','','1-2','[0, 0, 0]','2015-04-22 01:47:38','2015-04-22 01:47:38'),(114,11,'','','','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}',0000,'{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','','1-2','[0, 0, 0]','2015-04-24 12:35:26','2015-04-24 12:35:26'),(115,12,'','','','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}',0000,'{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','','1-2','[0, 0, 0]','2015-05-15 03:56:23','2015-05-15 03:56:23'),(116,13,'','','','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}',0000,'{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','','1-2','[0, 0, 0]','2015-05-15 03:57:40','2015-05-15 03:57:40'),(117,14,'','','','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}',0000,'{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','','1-2','[0, 0, 0]','2015-05-15 10:11:55','2015-05-15 10:11:55'),(118,15,'','','','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}',0000,'{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','','1-2','[0, 0, 0]','2015-05-15 10:52:22','2015-05-15 10:52:22'),(119,16,'','','','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}',0000,'{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','','1-2','[0, 0, 0]','2015-05-20 06:38:08','2015-05-20 06:38:08'),(120,17,'','','','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}',0000,'{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','','1-2','[0, 0, 0]','2015-05-20 06:54:15','2015-05-20 06:54:15'),(121,18,'','','','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}',0000,'{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','','1-2','[0, 0, 0]','2015-05-20 08:17:51','2015-05-20 08:17:51'),(122,19,'','','','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}',0000,'{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','','1-2','[0, 0, 0]','2015-05-21 02:39:48','2015-05-21 02:39:48'),(123,20,'','','','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}',0000,'{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','','1-2','[0, 0, 0]','2015-05-22 12:12:22','2015-05-22 12:12:22'),(124,21,'','','','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}',0000,'{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','','1-2','[0, 0, 0]','2015-05-25 00:28:22','2015-05-25 00:28:22'),(125,22,'','','','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}',0000,'{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','','1-2','[0, 0, 0]','2015-06-04 09:22:26','2015-06-04 09:22:26'),(126,23,'','','','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}',0000,'{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','','1-2','[0, 0, 0]','2015-06-10 20:46:10','2015-06-10 20:46:10');
/*!40000 ALTER TABLE `ProviderInfo` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`biom`@`localhost`*/ /*!50003 TRIGGER `provider_info_creation_time` BEFORE INSERT ON `ProviderInfo`
 FOR EACH ROW BEGIN
    SET NEW.dateCreated = NOW();
    SET NEW.dateModified = NOW();
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`biom`@`localhost`*/ /*!50003 TRIGGER `provider_info_modification_time` BEFORE UPDATE ON `ProviderInfo`
 FOR EACH ROW BEGIN
    SET NEW.dateModified = NOW();
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `Reports`
--

DROP TABLE IF EXISTS `Reports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Reports` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `profileId` int(11) NOT NULL,
  `type` enum('incoming','outgoing') COLLATE utf8_unicode_ci NOT NULL,
  `description` varchar(250) COLLATE utf8_unicode_ci NOT NULL,
  `dateCreated` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=200 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Reports`
--

LOCK TABLES `Reports` WRITE;
/*!40000 ALTER TABLE `Reports` DISABLE KEYS */;
INSERT INTO `Reports` VALUES (1,4,'outgoing','Lock 1 added to My Home','2014-07-20 16:45:05'),(2,4,'incoming','Alex applied to My Home','2014-07-20 16:45:05'),(3,4,'outgoing','You accepted Alex to My Home','2014-07-20 16:45:05'),(4,4,'outgoing','Lock 2 added to My Home','2014-07-20 16:45:05'),(5,4,'outgoing','Den invited to My Home','2014-07-20 16:45:05'),(6,4,'incoming','Den accepted invitation to My Home','2014-07-20 16:45:05'),(7,4,'outgoing','<span class=\"glyphicon glyphicon-cog\"></span> New lock Lock8 added','2014-07-20 18:42:01'),(8,4,'outgoing','<span class=\"glyphicon glyphicon-cog\"></span> New lock <strong>Lock8</strong> added','2014-07-20 18:46:17'),(9,4,'outgoing','<span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock10</strong> updated','2014-07-20 18:50:30'),(10,4,'outgoing','<span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock10</strong> deleted','2014-07-20 18:50:34'),(11,4,'outgoing','<span class=\"glyphicon glyphicon-list-alt\"></span> Policy <strong>Policy 4</strong> deleted','2014-07-20 20:30:34'),(12,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> <span class=\"glyphicon glyphicon-cog\"></span> undefined <strong>undefined</strong> added to <strong></strong>','2014-07-20 20:59:05'),(13,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> <span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock1</strong> added to <strong>undefined</strong>','2014-07-20 21:07:08'),(14,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> <span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock1</strong> removed from <strong>undefined</strong>','2014-07-20 21:07:37'),(15,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> <span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock1</strong> added to <strong>undefined</strong>','2014-07-20 21:08:55'),(16,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> <span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock1</strong> removed from <strong>undefined</strong>','2014-07-20 21:09:00'),(17,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> <span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock1</strong> added to <strong>undefined</strong>','2014-07-20 21:10:40'),(18,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> <span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock1</strong> removed from <strong>undefined</strong>','2014-07-20 21:10:47'),(19,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> <span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock1</strong> added to <strong>undefined</strong>','2014-07-20 21:11:08'),(20,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> <span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock1</strong> added to <strong>undefined</strong>','2014-07-20 21:11:09'),(21,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> <span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock1</strong> removed from <strong>undefined</strong>','2014-07-20 21:11:13'),(22,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> <span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock1</strong> added to <strong>some device</strong>','2014-07-20 21:12:08'),(23,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> <span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock1</strong> removed from <strong>some device</strong>','2014-07-20 21:12:14'),(24,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> New location <strong>some device</strong> deleted','2014-07-20 21:20:31'),(25,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> New location <strong>My Office</strong> added','2014-07-20 21:20:59'),(26,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> <span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock1</strong> added to <strong>My Office</strong>','2014-07-20 21:21:08'),(27,4,'outgoing','<span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock1</strong> updated','2014-07-20 21:21:14'),(28,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> <span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock1</strong> removed from <strong>My Office</strong>','2014-07-20 21:21:18'),(29,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> New location <strong>My Office</strong> deleted','2014-07-20 21:21:36'),(30,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Pool</strong> updated','2014-07-20 21:24:55'),(31,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> <span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock2</strong> removed from <strong>undefined</strong>','2014-07-20 21:36:01'),(32,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> <span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock1</strong> added to <strong>My Home</strong>','2014-07-20 21:36:56'),(33,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> <span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock1</strong> removed from <strong>My Home</strong>','2014-07-20 21:37:03'),(34,4,'outgoing','<span class=\"glyphicon glyphicon-user\"></span> You invited <strong>hulk</strong> to <strong>\n\n		    My HomeMy StoreMy Dog\'s HouseMy Pool</strong>','2014-07-20 22:02:13'),(35,17,'incoming','<span class=\"glyphicon glyphicon-user\"></span> You are invited by <strong>charles</strong> to <strong>\n\n		    My HomeMy StoreMy Dog\'s HouseMy Pool</strong>','2014-07-20 22:02:13'),(36,4,'outgoing','<span class=\"glyphicon glyphicon-user\"></span> You invited <strong>spiderman</strong> to <strong>My Home</strong>','2014-07-20 22:04:21'),(37,16,'incoming','<span class=\"glyphicon glyphicon-user\"></span> You are invited by <strong>charles</strong> to <strong>My Home</strong>','2014-07-20 22:04:21'),(38,23,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> New resource <strong>Bart\'s House</strong> added','2014-07-20 22:09:24'),(39,23,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> New resource <strong>Bart\'s Room</strong> added','2014-07-20 22:09:42'),(40,23,'outgoing','<span class=\"glyphicon glyphicon-user\"></span> You invited <strong>charles</strong> to <strong>Bart\'s House</strong>','2014-07-20 22:10:15'),(41,4,'incoming','<span class=\"glyphicon glyphicon-user\"></span> You are invited by <strong>bart</strong> to <strong>Bart\'s House</strong>','2014-07-20 22:10:15'),(42,4,'outgoing','<span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock8</strong> deleted','2014-07-24 08:13:22'),(43,4,'outgoing','<span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock6</strong> deleted','2014-07-24 08:13:26'),(44,4,'outgoing','<span class=\"glyphicon glyphicon-cog\"></span> New lock <strong>Lock8</strong> added','2014-07-24 08:35:49'),(45,4,'outgoing','<span class=\"glyphicon glyphicon-list-alt\"></span> New policy <strong>Policy4</strong> added','2014-07-24 10:03:34'),(46,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> New resource <strong>My Room</strong> added','2014-07-24 12:14:13'),(47,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Rooms</strong> updated','2014-07-24 12:14:21'),(48,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Rooms</strong> updated','2014-07-25 17:58:34'),(49,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Rooms</strong> updated','2014-07-25 18:35:00'),(50,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Rooms</strong> updated','2014-07-25 18:36:16'),(51,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Rooms</strong> updated','2014-07-25 18:37:09'),(52,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Rooms</strong> updated','2014-07-25 18:38:14'),(53,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Home</strong> updated','2014-07-25 18:40:07'),(54,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Store</strong> updated','2014-07-25 18:40:20'),(55,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Home</strong> updated','2014-07-25 18:45:55'),(56,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Store</strong> updated','2014-07-25 18:46:00'),(57,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Home</strong> updated','2014-07-25 18:46:16'),(58,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Store</strong> updated','2014-07-25 18:46:21'),(59,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Dog\'s House</strong> updated','2014-07-25 18:46:30'),(60,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Home</strong> updated','2014-07-25 18:50:35'),(61,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Store</strong> updated','2014-07-25 18:51:06'),(62,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Home</strong> updated','2014-07-25 18:54:55'),(63,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Home</strong> updated','2014-07-25 18:55:20'),(64,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Store</strong> updated','2014-07-25 18:55:27'),(65,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Home</strong> updated','2014-07-25 18:56:15'),(66,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Home</strong> updated','2014-07-25 18:56:40'),(67,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Store</strong> updated','2014-07-25 18:56:45'),(68,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Home</strong> updated','2014-07-25 18:58:03'),(69,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Home</strong> updated','2014-07-25 19:03:27'),(70,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Home</strong> updated','2014-07-25 19:03:58'),(71,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Home</strong> updated','2014-07-25 19:07:01'),(72,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Store</strong> updated','2014-07-25 19:07:12'),(73,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Home</strong> updated','2014-07-25 19:10:32'),(74,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Home</strong> updated','2014-07-25 19:10:36'),(75,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Home</strong> updated','2014-07-25 19:10:40'),(76,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Home</strong> updated','2014-07-25 19:10:44'),(77,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Rooms</strong> updated','2014-07-25 19:10:58'),(78,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Store</strong> updated','2014-07-25 19:11:25'),(79,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Store</strong> updated','2014-07-25 19:11:30'),(80,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Dog\'s House</strong> updated','2014-07-25 19:11:31'),(81,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Home</strong> updated','2014-07-26 03:08:19'),(82,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Home</strong> updated','2014-07-26 03:08:31'),(83,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Home</strong> updated','2014-07-26 03:08:37'),(84,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Store</strong> updated','2014-07-26 03:08:43'),(85,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Home</strong> updated','2014-07-26 03:08:53'),(86,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Home</strong> updated','2014-07-26 03:09:11'),(87,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Home</strong> updated','2014-07-26 03:09:20'),(88,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Home</strong> updated','2014-07-26 03:10:10'),(89,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Home</strong> updated','2014-07-26 03:10:18'),(90,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Home</strong> updated','2014-07-26 03:11:51'),(91,27,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> New resource <strong>test</strong> added','2014-08-04 01:10:02'),(92,27,'outgoing','<span class=\"glyphicon glyphicon-list-alt\"></span> New policy <strong>test</strong> added','2014-08-04 01:10:07'),(93,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> New resource <strong>11111</strong> added','2014-08-17 07:11:20'),(94,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>11111</strong> deleted','2014-08-17 07:11:38'),(95,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> New resource <strong>My Secure Location</strong> added','2014-08-17 07:20:58'),(96,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> New resource <strong>My Loco</strong> added','2014-08-17 07:44:27'),(97,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> New resource <strong>My Loco2</strong> added','2014-08-17 07:46:06'),(98,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Loco2</strong> deleted','2014-08-17 15:10:25'),(99,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Loco</strong> deleted','2014-08-17 15:10:29'),(100,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> New resource <strong>New Home</strong> added','2014-08-17 15:33:22'),(101,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> <span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock1</strong> added to <strong>My Pool</strong>','2014-08-17 17:23:44'),(102,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> <span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock1</strong> added to <strong>My Pool</strong>','2014-08-17 17:23:44'),(103,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> <span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock1</strong> added to <strong>My Pool</strong>','2014-08-17 17:23:44'),(104,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> <span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock3</strong> removed from <strong>My Home</strong>','2014-08-17 17:34:00'),(105,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> <span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock2</strong> added to <strong>My Home</strong>','2014-08-17 17:34:08'),(106,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Home</strong> updated','2014-08-18 05:27:21'),(107,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> New resource <strong>New Location</strong> added','2014-08-18 06:11:08'),(108,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>New Location</strong> deleted','2014-08-18 06:11:16'),(109,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>New Home</strong> deleted','2014-08-18 06:13:27'),(110,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Resource <strong>My Secure Location</strong> deleted','2014-08-18 06:13:39'),(111,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> New resource <strong>New Location</strong> added','2014-08-18 06:13:59'),(112,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Home</strong> updated','2014-08-22 05:16:55'),(113,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> New location <strong>Some Location</strong> added','2014-08-22 05:17:07'),(114,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Home</strong> updated','2014-08-22 05:20:12'),(115,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Home</strong> updated','2014-08-22 07:25:47'),(116,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Home</strong> updated','2014-08-22 07:25:54'),(117,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Home</strong> updated','2014-08-22 07:28:58'),(118,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Home</strong> updated','2014-08-22 07:29:11'),(119,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Home</strong> updated','2014-08-22 07:33:47'),(120,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Home</strong> updated','2014-08-22 08:09:29'),(121,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Home</strong> updated','2014-08-22 08:09:45'),(122,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> New location <strong>New Location</strong> added','2014-08-23 03:51:58'),(123,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> New location <strong>My Location</strong> added','2014-08-23 03:52:54'),(124,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> New location <strong>My Location</strong> added','2014-08-23 03:55:11'),(125,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> New location <strong>My Location</strong> added','2014-08-23 03:57:57'),(126,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> New location <strong>My Location</strong> added','2014-08-23 03:59:24'),(127,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> New location <strong>qwerty</strong> added','2014-08-23 04:06:27'),(128,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> New location <strong>qwerty</strong> added','2014-08-23 04:10:16'),(129,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>qwerty</strong> deleted','2014-08-23 04:11:24'),(130,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Room</strong> updated','2014-08-23 04:15:26'),(131,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Room</strong> updated','2014-08-23 04:31:28'),(132,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Room</strong> updated','2014-08-23 04:32:45'),(133,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Room</strong> updated','2014-08-23 04:33:59'),(134,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Rooms</strong> updated','2014-08-23 04:41:14'),(135,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Room</strong> updated','2014-08-23 04:43:14'),(136,4,'outgoing','<span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock9</strong> updated','2014-08-23 04:44:25'),(137,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Rooms</strong> updated','2014-08-23 04:45:06'),(138,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Room</strong> updated','2014-08-23 04:48:38'),(139,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Dog\'s House</strong> updated','2014-08-23 06:02:26'),(140,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Room</strong> updated','2014-08-23 06:02:36'),(141,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Pool</strong> updated','2014-08-23 06:04:38'),(142,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Dog\'s House</strong> updated','2014-08-23 06:05:32'),(143,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Pool</strong> updated','2014-08-23 06:08:20'),(144,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Store</strong> updated','2014-08-26 04:40:27'),(145,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Pool</strong> updated','2014-08-26 04:40:36'),(146,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Dog\'s House</strong> updated','2014-08-26 04:46:27'),(147,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Room</strong> updated','2014-08-26 04:46:38'),(148,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Dog\'s House</strong> updated','2014-08-26 04:46:42'),(149,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Pool</strong> updated','2014-08-26 04:46:50'),(150,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> New location <strong>Some Location</strong> added','2014-08-26 04:47:13'),(151,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>Some Location</strong> updated','2014-08-26 04:47:32'),(152,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Home</strong> updated','2014-08-26 04:50:28'),(153,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Home</strong> updated','2014-08-26 04:50:34'),(154,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Home</strong> updated','2014-08-26 04:50:44'),(155,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>Some Location</strong> updated','2014-08-26 04:51:03'),(156,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>Some Location</strong> updated','2014-08-26 04:51:59'),(157,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Home</strong> updated','2014-08-26 04:52:05'),(158,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Store</strong> updated','2014-08-26 04:52:18'),(159,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Pool</strong> updated','2014-08-26 05:02:33'),(160,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Home</strong> updated','2014-08-26 05:05:23'),(161,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Store</strong> updated','2014-08-26 05:05:33'),(162,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Home</strong> updated','2014-08-26 05:06:18'),(163,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Room</strong> updated','2014-08-26 05:10:37'),(164,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Pool</strong> updated','2014-08-26 05:10:42'),(165,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Home</strong> updated','2014-08-26 05:10:49'),(166,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Home</strong> updated','2014-08-26 05:10:52'),(167,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Home</strong> updated','2014-08-26 05:13:22'),(168,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Home</strong> updated','2014-08-26 05:13:26'),(169,4,'outgoing','<span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock4</strong> updated','2014-08-26 17:47:55'),(170,4,'outgoing','<span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock3</strong> updated','2014-08-26 17:47:59'),(171,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>My Home</strong> updated','2014-08-26 22:55:59'),(172,4,'outgoing','<span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock5</strong> updated','2014-08-26 23:36:39'),(173,4,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> <span class=\"glyphicon glyphicon-cog\"></span> lock <strong>Lock2</strong> removed from <strong>My Home</strong>','2014-09-18 23:55:27'),(174,65,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> New location <strong>123 Main Street</strong> added','2014-10-10 17:25:09'),(175,65,'incoming','<span class=\"glyphicon glyphicon-user\"></span> You are invited by <strong>danit</strong> to <strong></strong>','2014-10-10 17:25:50'),(176,65,'outgoing','<span class=\"glyphicon glyphicon-user\"></span> You invited <strong>danit</strong> to <strong></strong>','2014-10-10 17:25:50'),(177,65,'outgoing','<span class=\"glyphicon glyphicon-list-alt\"></span> New policy <strong>Daytime access</strong> added','2014-10-10 17:26:13'),(178,65,'outgoing','<span class=\"glyphicon glyphicon-list-alt\"></span> Policy <strong>Daytime access</strong> added','2014-10-10 17:26:59'),(179,65,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> Location <strong>123 Main Street</strong> updated','2014-10-10 17:31:06'),(180,5,'outgoing','<span class=\"glyphicon glyphicon-list-alt\"></span> New policy <strong>qwerty</strong> added','2014-10-13 16:58:28'),(181,5,'outgoing','<span class=\"glyphicon glyphicon-list-alt\"></span> New policy <strong>qwerty</strong> added','2014-10-13 16:58:34'),(182,5,'outgoing','<span class=\"glyphicon glyphicon-list-alt\"></span> New policy <strong>qwerty</strong> added','2014-10-20 16:33:19'),(183,5,'outgoing','<span class=\"glyphicon glyphicon-list-alt\"></span> New policy <strong>qwerty</strong> added','2014-10-20 18:30:55'),(184,5,'outgoing','<span class=\"glyphicon glyphicon-list-alt\"></span> New policy <strong>qwerty</strong> added','2014-10-20 18:33:45'),(185,5,'outgoing','<span class=\"glyphicon glyphicon-list-alt\"></span> New policy <strong>qwerty</strong> added','2014-10-20 18:34:08'),(186,5,'outgoing','<span class=\"glyphicon glyphicon-cog\"></span> lock <strong>some name</strong> deleted','2014-10-20 18:41:54'),(187,5,'outgoing','<span class=\"glyphicon glyphicon-cog\"></span> lock <strong>some name</strong> deleted','2014-10-20 18:41:58'),(188,5,'outgoing','<span class=\"glyphicon glyphicon-cog\"></span> lock <strong>some name</strong> deleted','2014-10-20 18:42:01'),(189,5,'outgoing','<span class=\"glyphicon glyphicon-cog\"></span> lock <strong>qwerty</strong> deleted','2014-10-20 18:42:04'),(190,5,'outgoing','<span class=\"glyphicon glyphicon-cog\"></span> lock <strong>qwerty</strong> deleted','2014-10-20 18:42:09'),(191,5,'outgoing','<span class=\"glyphicon glyphicon-cog\"></span> lock <strong>qwerty</strong> deleted','2014-10-20 18:42:12'),(192,5,'outgoing','<span class=\"glyphicon glyphicon-cog\"></span> lock <strong>qwerty</strong> deleted','2014-10-20 18:42:16'),(193,5,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> New location <strong>qwerty</strong> added','2014-10-20 18:42:35'),(194,5,'outgoing','<span class=\"glyphicon glyphicon-cog\"></span> lock <strong>qwerty</strong> updated','2014-10-20 18:42:54'),(195,5,'outgoing','<span class=\"glyphicon glyphicon-cog\"></span> lock <strong>qwerty</strong> updated','2014-10-20 18:43:59'),(196,5,'outgoing','<span class=\"glyphicon glyphicon-home\"></span> New location <strong>Location</strong> added','2014-10-27 14:58:08'),(197,27,'outgoing','<span class=\"glyphicon glyphicon-list-alt\"></span> New policy <strong>Daily 7am-5pm</strong> added','2014-12-08 20:30:34'),(198,27,'outgoing','<span class=\"glyphicon glyphicon-list-alt\"></span> Policy <strong>test</strong> deleted','2014-12-08 20:30:45'),(199,106,'outgoing','<span class=\"glyphicon glyphicon-list-alt\"></span> New policy <strong>Physical</strong> added','2015-03-26 14:25:24');
/*!40000 ALTER TABLE `Reports` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`biom`@`localhost`*/ /*!50003 TRIGGER `reports_creation_time` BEFORE INSERT ON `Reports`
 FOR EACH ROW BEGIN
    SET NEW.dateCreated = NOW();
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `ResourceUsers`
--

DROP TABLE IF EXISTS `ResourceUsers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ResourceUsers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `locationId` int(11) NOT NULL,
  `ownerId` int(11) NOT NULL,
  `userId` int(11) NOT NULL,
  `type` enum('application','invitation') CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `status` enum('pending','accepted','refused') CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT 'pending',
  `timeRestriction` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `dateCreated` datetime NOT NULL,
  `dateModified` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ResourceUsers`
--

LOCK TABLES `ResourceUsers` WRITE;
/*!40000 ALTER TABLE `ResourceUsers` DISABLE KEYS */;
INSERT INTO `ResourceUsers` VALUES (1,8,4,1,'invitation','pending','02:59 / 14:00','0000-00-00 00:00:00','2014-07-20 19:27:38'),(2,8,4,2,'application','accepted','days/5','0000-00-00 00:00:00','0000-00-00 00:00:00'),(3,8,4,3,'application','pending','24/7','0000-00-00 00:00:00','0000-00-00 00:00:00'),(19,8,4,5,'invitation','pending','11:00 / 14:00','0000-00-00 00:00:00','2014-07-20 20:11:23'),(20,8,4,8,'invitation','refused','24/7','0000-00-00 00:00:00','0000-00-00 00:00:00'),(21,15,1,4,'application','accepted','24/7','0000-00-00 00:00:00','0000-00-00 00:00:00'),(22,16,1,4,'invitation','accepted','24/7','0000-00-00 00:00:00','2014-10-18 00:29:27'),(24,8,4,15,'invitation','refused','24/7','0000-00-00 00:00:00','0000-00-00 00:00:00'),(41,8,4,17,'invitation','pending',' - ','2014-07-20 22:02:12','2014-07-20 22:02:12'),(42,8,4,16,'invitation','pending',' - ','2014-07-20 22:04:19','2014-07-20 22:04:19'),(43,22,23,4,'invitation','accepted',' - ','2014-07-20 22:10:14','2014-10-18 00:29:29'),(44,23,23,4,'invitation','accepted',' - ','2014-07-20 22:10:39','2014-10-18 00:29:30');
/*!40000 ALTER TABLE `ResourceUsers` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`biom`@`localhost`*/ /*!50003 TRIGGER `resource_users_creation_time` BEFORE INSERT ON `ResourceUsers`
 FOR EACH ROW BEGIN
    SET NEW.dateCreated = NOW();
    SET NEW.dateModified = NOW();
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`biom`@`localhost`*/ /*!50003 TRIGGER `resource_users_modification_time` BEFORE UPDATE ON `ResourceUsers`
 FOR EACH ROW BEGIN
    SET NEW.dateModified = NOW();
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `SecureLocations`
--

DROP TABLE IF EXISTS `SecureLocations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SecureLocations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE latin1_general_ci NOT NULL,
  `address` varchar(1000) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `owner` int(11) NOT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `deviceIds` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `policy` int(11) NOT NULL,
  `map` text COLLATE latin1_general_ci NOT NULL,
  `dateCreated` datetime NOT NULL,
  `dateModified` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SecureLocations`
--

LOCK TABLES `SecureLocations` WRITE;
/*!40000 ALTER TABLE `SecureLocations` DISABLE KEYS */;
INSERT INTO `SecureLocations` VALUES (1,'qwerty','{\"street1\":\"2323, Green Road\",\"street2\":\"\",\"continent\":\"Antarctica\",\"country\":\"Antarctica\",\"province\":\"\",\"region\":\"\",\"city\":\"\",\"postcode\":\"939343\"}',26,'','',0,'','0000-00-00 00:00:00','2014-08-18 05:17:01'),(2,'qwerty','{\"street1\":\"2323, Green Road\",\"street2\":\"\",\"continent\":\"Antarctica\",\"country\":\"Antarctica\",\"province\":\"\",\"region\":\"\",\"city\":\"\",\"postcode\":\"939343\"}',26,'','',1,'','0000-00-00 00:00:00','2014-08-18 05:17:01'),(3,'qwerty','{\"street1\":\"2323, Green Road\",\"street2\":\"\",\"continent\":\"Antarctica\",\"country\":\"Antarctica\",\"province\":\"\",\"region\":\"\",\"city\":\"\",\"postcode\":\"939343\"}',26,'','',0,'','0000-00-00 00:00:00','2014-08-18 05:17:01'),(4,'qwerty','{\"street1\":\"2323, Green Road\",\"street2\":\"\",\"continent\":\"Antarctica\",\"country\":\"Antarctica\",\"province\":\"\",\"region\":\"\",\"city\":\"\",\"postcode\":\"939343\"}',18,'','',0,'','0000-00-00 00:00:00','2014-08-18 05:17:01'),(5,'qwerty2','{\"street1\":\"2323, Green Road\",\"street2\":\"\",\"continent\":\"Antarctica\",\"country\":\"Antarctica\",\"province\":\"\",\"region\":\"\",\"city\":\"\",\"postcode\":\"939343\"}',18,'','',1,'','0000-00-00 00:00:00','2014-08-18 05:17:01'),(6,'qwerty','{\"street1\":\"2323, Green Road\",\"street2\":\"\",\"continent\":\"Antarctica\",\"country\":\"Antarctica\",\"province\":\"\",\"region\":\"\",\"city\":\"\",\"postcode\":\"939343\"}',18,'','',0,'','0000-00-00 00:00:00','2014-08-18 05:17:01'),(8,'My Home','{\"street1\":\"2323, Green Road\",\"street2\":\"\",\"continent\":\"Asia\",\"country\":\"Azerbaijan\",\"province\":\"\",\"region\":\"\",\"city\":\"\",\"postcode\":\"939343\"}',4,'Some very very cool place','My Home',19,'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1397.427492043511!2d-122.93404450000004!3d45.53312370000001!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x54950560dd2a65d3%3A0xfcbb3d6c56622033!2s4600+NE+Cornell+Rd%2C+Hillsboro%2C+OR+97124!5e0!3m2!1sen!2sus!4v1407712856234','0000-00-00 00:00:00','2014-08-26 22:55:58'),(11,'My Store','{\"street1\":\"2323, Green Road\",\"street2\":\"\",\"continent\":\"Antarctica\",\"country\":\"Antarctica\",\"province\":\"\",\"region\":\"\",\"city\":\"\",\"postcode\":\"939343\"}',4,'','My Store',16,'','0000-00-00 00:00:00','2014-08-26 05:05:32'),(13,'My Dog\'s House','{\"street1\":\"2323, Green Road\",\"street2\":\"\",\"continent\":\"Antarctica\",\"country\":\"Antarctica\",\"province\":\"\",\"region\":\"\",\"city\":\"\",\"postcode\":\"939343\"}',4,'','',15,'','0000-00-00 00:00:00','2014-08-26 04:46:42'),(14,'My Pool','{\"street1\":\"2323, Green Road\",\"street2\":\"\",\"continent\":\"Antarctica\",\"country\":\"Antarctica\",\"province\":\"\",\"region\":\"\",\"city\":\"\",\"postcode\":\"939343\"}',4,'','',16,'','0000-00-00 00:00:00','2014-08-26 05:10:41'),(15,'Alex\'s Home','{\"street1\":\"2323, Green Road\",\"street2\":\"\",\"continent\":\"Antarctica\",\"country\":\"Antarctica\",\"province\":\"\",\"region\":\"\",\"city\":\"\",\"postcode\":\"939343\"}',1,'','',0,'','0000-00-00 00:00:00','2014-08-18 05:17:01'),(16,'Alex\'s Garage','{\"street1\":\"2323, Green Road\",\"street2\":\"\",\"continent\":\"Antarctica\",\"country\":\"Antarctica\",\"province\":\"\",\"region\":\"\",\"city\":\"\",\"postcode\":\"939343\"}',1,'','',0,'','0000-00-00 00:00:00','2014-08-18 05:17:01'),(17,'Alex\'s Gym','{\"street1\":\"2323, Green Road\",\"street2\":\"\",\"continent\":\"Antarctica\",\"country\":\"Antarctica\",\"province\":\"\",\"region\":\"\",\"city\":\"\",\"postcode\":\"939343\"}',1,'','',0,'','0000-00-00 00:00:00','2014-08-18 05:17:01'),(18,'ABC','{\"street1\":\"2323, Green Road\",\"street2\":\"\",\"continent\":\"Antarctica\",\"country\":\"Antarctica\",\"province\":\"\",\"region\":\"\",\"city\":\"\",\"postcode\":\"939343\"}',22,'','',21,'','0000-00-00 00:00:00','2014-08-18 05:17:01'),(19,'test','{\"street1\":\"2323, Green Road\",\"street2\":\"\",\"continent\":\"Antarctica\",\"country\":\"Antarctica\",\"province\":\"\",\"region\":\"\",\"city\":\"\",\"postcode\":\"939343\"}',3,'','',20,'','0000-00-00 00:00:00','2014-08-18 05:17:01'),(22,'Bart\'s House','{\"street1\":\"2323, Green Road\",\"street2\":\"\",\"continent\":\"Antarctica\",\"country\":\"Antarctica\",\"province\":\"\",\"region\":\"\",\"city\":\"\",\"postcode\":\"939343\"}',23,'','',0,'','2014-07-20 22:09:24','2014-08-18 05:17:01'),(23,'Bart\'s Room','{\"street1\":\"2323, Green Road\",\"street2\":\"\",\"continent\":\"Antarctica\",\"country\":\"Antarctica\",\"province\":\"\",\"region\":\"\",\"city\":\"\",\"postcode\":\"939343\"}',23,'','',0,'','2014-07-20 22:09:41','2014-08-18 05:17:01'),(24,'My Room','{\"street1\":\"2323, Green Road\",\"street2\":\"\",\"continent\":\"Antarctica\",\"country\":\"Antarctica\",\"province\":\"\",\"region\":\"\",\"city\":\"\",\"postcode\":\"939343\"}',4,'','',15,'','2014-07-24 12:14:13','2014-08-26 05:10:37'),(25,'test','{\"street1\":\"2323, Green Road\",\"street2\":\"\",\"continent\":\"Antarctica\",\"country\":\"Antarctica\",\"province\":\"\",\"region\":\"\",\"city\":\"\",\"postcode\":\"939343\"}',27,'','',0,'','2014-08-04 01:10:01','2014-08-18 05:17:01'),(32,'Some Location','{\"street1\":\"Some street\",\"street2\":\"\",\"continent\":\"\",\"country\":\"\",\"province\":\"\",\"region\":\"\",\"city\":\"\",\"postcode\":\"\"}',4,'','',15,'','2014-08-26 04:47:13','2014-08-26 04:51:59'),(33,'123 Main Street','{\"street1\":\"address\",\"street2\":\"\",\"continent\":\"\",\"country\":\"\",\"province\":\"\",\"region\":\"\",\"city\":\"\",\"postcode\":\"\"}',65,'description','',24,'','2014-10-10 17:25:06','2014-10-10 17:31:05'),(34,'qwerty','{\"street1\":\"\",\"street2\":\"\",\"continent\":\"\",\"country\":\"\",\"province\":\"\",\"region\":\"\",\"city\":\"\",\"postcode\":\"\"}',5,'','',0,'','2014-10-20 18:42:34','2014-10-20 18:42:34'),(35,'Location','{\"street1\":\"\",\"street2\":\"\",\"continent\":\"\",\"country\":\"\",\"province\":\"\",\"region\":\"\",\"city\":\"\",\"postcode\":\"\"}',5,'','',0,'','2014-10-27 14:58:07','2014-10-27 14:58:07');
/*!40000 ALTER TABLE `SecureLocations` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`biom`@`localhost`*/ /*!50003 TRIGGER `secure_locations_creation_time` BEFORE INSERT ON `SecureLocations`
 FOR EACH ROW BEGIN
    SET NEW.dateCreated = NOW();
    SET NEW.dateModified = NOW();
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`biom`@`localhost`*/ /*!50003 TRIGGER `secure_locations_modification_time` BEFORE UPDATE ON `SecureLocations`
 FOR EACH ROW BEGIN
    SET NEW.dateModified = NOW();
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `Services`
--

DROP TABLE IF EXISTS `Services`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Services` (
  `id` int(2) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `date_created` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Services`
--

LOCK TABLES `Services` WRITE;
/*!40000 ALTER TABLE `Services` DISABLE KEYS */;
INSERT INTO `Services` VALUES (1,'mobile_application','2015-04-06 19:45:52'),(2,'chrome_extention','2015-04-06 19:45:52');
/*!40000 ALTER TABLE `Services` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Splash`
--

DROP TABLE IF EXISTS `Splash`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Splash` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `type` enum('Developer','Provider','Press','Investor','User','') COLLATE utf8_unicode_ci NOT NULL,
  `code` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `invitation` enum('yes','no') COLLATE utf8_unicode_ci NOT NULL DEFAULT 'no',
  `date_created` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Splash`
--

LOCK TABLES `Splash` WRITE;
/*!40000 ALTER TABLE `Splash` DISABLE KEYS */;
INSERT INTO `Splash` VALUES (1,'admin','admin@biomio.admin','Developer','biomioadmin7777','no','2015-04-15 18:35:32'),(2,'Joshua Sams','joshuasams@gmail.com','Developer','4ZewyOZjDmvHQB','no','0000-00-00 00:00:00'),(3,'Andre Mon Belle','andre@monbelle.com','Investor','qkIBVhqrYaP0cJB','yes','0000-00-00 00:00:00'),(4,'isaac durotoye Jnrjose','idurotoye@jnrjose.org','Developer','0DCZfL7R0veaS0j','no','0000-00-00 00:00:00'),(5,'Philip Kolba','philip.kolba@hayesabrams.com','Developer','QE20vhtJaCfMuFO','no','0000-00-00 00:00:00'),(6,'Andriy Lobashchuk','orrionandi@gmail.com','Developer','ITpTt2BcvIUG5D','no','0000-00-00 00:00:00'),(7,'Alex Chmykhalo','alex.chmykhalo@vakoms.com.ua','Developer','arfAGn85rJN0pO','yes','0000-00-00 00:00:00'),(8,'morty eisen','mortyeisen@gmail.com','Provider','OZlBthNpa7PEJgT','no','0000-00-00 00:00:00'),(9,'Alex Ramskov ','alex@biometricsolutions.dk','Provider','UUywTFvdV07WuL','no','0000-00-00 00:00:00'),(10,'jiri sklenar','sklenarj@ohsu.edu','Developer','T6vy5ce9tDC36L','no','0000-00-00 00:00:00');
/*!40000 ALTER TABLE `Splash` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TempEmailCodes`
--

DROP TABLE IF EXISTS `TempEmailCodes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TempEmailCodes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `profileId` int(11) NOT NULL,
  `code` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `email` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '1',
  `date_created` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=46 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TempEmailCodes`
--

LOCK TABLES `TempEmailCodes` WRITE;
/*!40000 ALTER TABLE `TempEmailCodes` DISABLE KEYS */;
INSERT INTO `TempEmailCodes` VALUES (7,11,'otyQTNvzmr','qwerty@qwerty.com',0,'2015-04-27 10:12:40'),(8,11,'rdVIycUlGj','qwerty@qwerty.com',0,'2015-04-27 10:24:50'),(9,11,'1mPEJ3DlCo','qwerty@qwerty.com',0,'2015-04-27 10:24:54'),(10,11,'7YqfJnNcAh','qwerty@qwerty.com',0,'2015-04-27 10:40:15'),(11,11,'03x9fSZ1Jv','qwerty@qwerty.com',0,'2015-04-28 13:25:39'),(12,11,'vha07l8yrR','qwerty2@qwerty.com',0,'2015-04-28 13:25:42'),(13,11,'UFIixftCBA','qwerty@qwerty.com',0,'2015-04-28 13:30:59'),(14,11,'O65fxz3ILm','qewrty3@qwerty.com',0,'2015-04-28 13:59:01'),(15,11,'WJU2nsLCzy','qwerty4@qwerty.com',0,'2015-04-28 13:59:31'),(19,15,'5qIDeCu1fE','orrionandi@gmail.com',1,'2015-05-15 10:53:28'),(18,15,'Cb4JkfQK0h','orrionandi@gmail.com',0,'2015-05-15 10:53:11'),(20,11,'SHyXsnl7zr','andriy.lobashchuk@vakoms.com.ua',0,'2015-05-19 06:29:29'),(21,11,'HiTPOzhFEK','andriy.lobashchuk@vakoms.com.ua',0,'2015-05-19 06:29:38'),(22,11,'A84gbkTYXI','alexander.lomov1@gmail.com',0,'2015-05-19 20:43:20'),(23,11,'v5yH4DnSwA','alexander.lomov1@gmail.com',0,'2015-05-19 20:48:54'),(24,11,'98vLhsEa6j','alexander.lomov1@gmail.com',0,'2015-05-19 20:50:07'),(25,11,'WVoOp5vKGJ','alexander.lomov1@gmail.com',0,'2015-05-19 20:54:25'),(26,11,'AFR8Zag9DU','test@test.com',0,'2015-05-21 02:38:40'),(27,11,'WHGIUQJuZc','test3@gmail.com',0,'2015-05-21 02:46:46'),(28,11,'GQ86rOdYIN','test4@gmail.com',0,'2015-05-21 02:48:01'),(29,11,'CGRZhTiQA5','test5@gmail.com',0,'2015-05-21 02:49:33'),(30,11,'3caXikUtdo','orrionandi@gmail.com',0,'2015-05-25 11:19:29'),(31,11,'SZrXL5daVp','qwerty1234@gmail.com',0,'2015-05-25 11:19:46'),(32,11,'UwzR8k4IS1','test5@gmail.com',0,'2015-05-25 11:30:29'),(33,11,'O5vXfD3k6u','qwerty1234@gmail.com',0,'2015-05-25 11:32:14'),(34,11,'40eGSwugBh','alexander.lomov1@gmail.com',0,'2015-05-26 13:18:13'),(35,11,'W3jizIJT2m','alexander.lomov1@gmail.com',0,'2015-05-26 13:18:36'),(36,11,'ahbgimR0Jr','alexander.lomov1@gmail.com',0,'2015-05-26 13:24:41'),(37,11,'2EWn8grOZ5','alexander.lomov1@gmail.com',0,'2015-05-26 13:29:48'),(38,11,'f4vmgGi3P7','alexander.lomov1@gmail.com',2,'2015-05-26 13:43:49'),(39,11,'rEnaL1XiPN','somenewemail@gmailc.om',3,'2015-05-26 17:29:46'),(40,11,'oapgBiMWR5','qwerty@qwerty.com',0,'2015-05-26 19:32:02'),(41,11,'3iGpDeEsMd','qwerty1@qwerty.com',0,'2015-05-26 19:33:47'),(42,21,'oCbpYJthsl','boris.itkis@gmail.com',3,'2015-06-03 15:18:04'),(43,11,'UBymZqRvpd','alexander.lomov1@gmail.com',3,'2015-06-03 15:58:45'),(44,4,'tlkBTAexUI','ditkis@gmail.com',0,'2015-06-03 17:04:08'),(45,4,'jStEhVwlpy','ditkis@gmail.com',3,'2015-06-03 17:04:09');
/*!40000 ALTER TABLE `TempEmailCodes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TempLoginCodes`
--

DROP TABLE IF EXISTS `TempLoginCodes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TempLoginCodes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `profileId` int(11) NOT NULL,
  `code` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '1',
  `date_created` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=121 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TempLoginCodes`
--

LOCK TABLES `TempLoginCodes` WRITE;
/*!40000 ALTER TABLE `TempLoginCodes` DISABLE KEYS */;
INSERT INTO `TempLoginCodes` VALUES (88,5,'LF7TjOzcmI',0,'2015-04-20 08:39:53'),(89,5,'LNcytagSjm',0,'2015-04-20 08:40:25'),(90,5,'j60LXuwiMp',0,'2015-04-20 08:41:32'),(91,5,'dEJtHucCTG',0,'2015-04-20 08:57:14'),(92,5,'J9RVCQUved',0,'2015-04-20 09:00:09'),(93,15,'inclHrT5IS',1,'2015-05-19 06:28:09'),(94,4,'6APpuOWTJg',0,'2015-06-02 17:59:55'),(95,4,'lRoSC1H0Zb',0,'2015-06-02 18:01:24'),(96,11,'BlbyN1rsGA',0,'2015-06-02 18:20:55'),(97,4,'9fmwxVLkWO',0,'2015-06-02 18:31:00'),(98,11,'RxJowkItAu',0,'2015-06-02 18:33:03'),(99,11,'ktHeI8ib1g',0,'2015-06-02 18:33:50'),(100,4,'D4JskQiOto',0,'2015-06-02 18:35:50'),(101,4,'j2mn0CvtOu',0,'2015-06-02 18:39:55'),(102,11,'m1zQgBMy6V',0,'2015-06-02 18:41:33'),(103,11,'tk37YayKIR',0,'2015-06-02 18:41:48'),(104,4,'Uu9FRp7Gjl',0,'2015-06-02 18:42:24'),(105,11,'KSRc9oCDAq',0,'2015-06-02 18:45:04'),(106,4,'UFiaCLQlx4',0,'2015-06-02 18:45:18'),(107,4,'6fQq3GluTo',0,'2015-06-02 18:47:49'),(108,4,'APIy7KDhSd',0,'2015-06-02 18:48:39'),(109,4,'rjPOgLz8CE',0,'2015-06-02 18:54:35'),(110,21,'Jnv26dMCQY',0,'2015-06-03 01:08:27'),(111,21,'KLPMTmew2W',0,'2015-06-03 01:09:50'),(112,21,'JBW5zTQXUv',0,'2015-06-03 10:50:57'),(113,21,'k4A5YtIpPX',0,'2015-06-03 13:25:06'),(114,21,'4G9p2QAaw8',0,'2015-06-03 15:15:20'),(115,21,'GBTWXbuO9A',0,'2015-06-03 15:16:16'),(116,22,'okfIuQpNyB',0,'2015-06-04 09:25:13'),(117,22,'dL9RuqyKFD',0,'2015-06-04 09:25:30'),(118,4,'y6wzMFhsb4',0,'2015-06-04 23:20:55'),(119,21,'kOrJKep3zd',1,'2015-06-05 00:25:03'),(120,4,'nAvXVwM8Zr',0,'2015-06-05 11:04:21');
/*!40000 ALTER TABLE `TempLoginCodes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TempPhoneCodes`
--

DROP TABLE IF EXISTS `TempPhoneCodes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TempPhoneCodes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `profileId` int(11) NOT NULL,
  `code` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `phone` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '1',
  `date_created` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=64 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TempPhoneCodes`
--

LOCK TABLES `TempPhoneCodes` WRITE;
/*!40000 ALTER TABLE `TempPhoneCodes` DISABLE KEYS */;
INSERT INTO `TempPhoneCodes` VALUES (53,11,'G6PdYCs27x','1',0,'2015-04-24 14:21:31'),(54,11,'TclFsdgwEJ','15039840867',0,'2015-04-24 14:23:52'),(55,11,'T5lBcohGtr','15039840867',0,'2015-04-24 14:26:52'),(56,11,'s7SzW6ewbM','15039840867',0,'2015-04-24 14:30:19'),(57,11,'KidRGBsxCJ','15039840867',0,'2015-04-24 14:31:14'),(58,11,'u9UOgQsiKc','15039840867',0,'2015-04-24 14:32:45'),(59,11,'uGfy2DIQc9','15039840867',0,'2015-04-24 14:36:08'),(60,11,'5r4pRDLAJX','15039840867',0,'2015-04-24 16:18:57'),(61,11,'ub5EHvJG7S','15039840867',0,'2015-04-27 10:14:09'),(62,11,'bFAfhzH3Z5','15039840867',0,'2015-05-26 17:38:26'),(63,11,'hdk1NQ3Mm4','15039840867',0,'2015-06-02 18:32:14');
/*!40000 ALTER TABLE `TempPhoneCodes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TempWebsiteCodes`
--

DROP TABLE IF EXISTS `TempWebsiteCodes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TempWebsiteCodes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `filename` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `domain` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `dateCreated` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=53 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TempWebsiteCodes`
--

LOCK TABLES `TempWebsiteCodes` WRITE;
/*!40000 ALTER TABLE `TempWebsiteCodes` DISABLE KEYS */;
INSERT INTO `TempWebsiteCodes` VALUES (40,'9Z3fpZVH3LUhV6h','BIOMIO_ux6CVEO2w8L4w77.txt','charles','0000-00-00 00:00:00'),(39,'xtKY8Q67V8ZqmcG','BIOMIO_n5DX0KkjXuLJQyI.txt','sdfjlsjdf.kjslkdfj','0000-00-00 00:00:00'),(38,'ztan3KM6QEgdLJO','BIOMIO_BG6kIrG8PWK40h.txt','chadf.com','0000-00-00 00:00:00'),(37,'o2pPnd8EJ38plQp','BIOMIO_Li4UdHTdXfBJxC.txt','chadf','0000-00-00 00:00:00'),(36,'ps0kFkLVRmhtF0I','BIOMIO_RbdsLIJ5hQQvGmK.txt','vhbjnkm.com','0000-00-00 00:00:00'),(35,'xo7eOSW64wzqY','BIOMIO_zMgXxlmVi7D8llV.txt','jkjkjkj.com','0000-00-00 00:00:00'),(34,'p7hoBB2aZuPIGM','BIOMIO_yXkai5g8bFL35ij.txt','jkjlkj.com','0000-00-00 00:00:00'),(33,'CQBCicM06mtjBIg','BIOMIO_hkayEHOzku3zROV.txt','jlskajdlfkjsdf.com','0000-00-00 00:00:00'),(32,'Fh495uMbCWZAIHU','BIOMIO_HzFJ7OKbWQFezuL.txt','fgfhjkl;.com','0000-00-00 00:00:00'),(31,'88XNGz2KUMO7Qke','BIOMIO_i8Ck8oz0uinlR4e.html','fghjkl;.com','0000-00-00 00:00:00'),(30,'WpvCH8PvLuKi8i7','BIOMIO_RrskiCYxeygWZMT.html','hjkl.com','0000-00-00 00:00:00'),(29,'okx3c6DSlJBnsoV','BIOMIO_gPCakt8Zh69lARx.html','lkjljkdsf.com','0000-00-00 00:00:00'),(28,'sjqjw4pca37uGFA','BIOMIO_EYGb5TpaFr7rqHf.txt','something.com','0000-00-00 00:00:00'),(27,'RYaSDNJCaSHSpU5','BIOMIO_2kxYdqLBIbNYPsF.html','asdfsdf.com','0000-00-00 00:00:00'),(25,'5IPj4vHqBzSBezk','BIOMIO_vZdFEtCIe0AsBHU.html','asdfasdf.com','0000-00-00 00:00:00'),(26,'sOwITnPGZxMzplp','BIOMIO_Sfu8zqeJYSLCsBg.html','asdfasdff.com','0000-00-00 00:00:00'),(41,'0ofgEL76vhDVWGr','BIOMIO_Ph3yACWIjvwG0VN.txt','charles.com','0000-00-00 00:00:00'),(42,'RXdT5OePzbnnZ7W','BIOMIO_k3RdNV9H6aL97wj.txt','sdfsdf','0000-00-00 00:00:00'),(43,'6nOKSIABsy5BBmw','BIOMIO_88ARQeqAzNfEKPz.txt','sdfsdf.com','0000-00-00 00:00:00'),(44,'ApYP8JJczKOPpSN','BIOMIO_zOlPHoe7SRN5oE.txt','alexanderlomov.com','0000-00-00 00:00:00'),(45,'8dHxioeK3cV6b0a','BIOMIO_F3G5xD62Dtyc5tk.txt','a','0000-00-00 00:00:00'),(46,'nJ0YnPbwFm7flDy','BIOMIO_EvH9Ddzftp9g3XD.txt','alexanderlomov.co','0000-00-00 00:00:00'),(47,'bdq7tU8WAqXWP3','BIOMIO_qDwTfZei4GtlckM.txt','alexanderlomov.c','0000-00-00 00:00:00'),(48,'EwAfN6jKSFdx0Hi','BIOMIO_ubYj3nSH0L3r7k.txt','','0000-00-00 00:00:00'),(49,'wRLQxFDQ4OTw5ZL','BIOMIO_bmKysjvrZLzak.txt','beastyvsbeaute.com','0000-00-00 00:00:00'),(50,'bHa2YsAJgTgnsD7','BIOMIO_NczL5LillFaSO.txt','google.com','0000-00-00 00:00:00'),(51,'koTpkDqOSRbeeF6','BIOMIO_HKXmFsPj4MBOExj.txt','biom.io','0000-00-00 00:00:00'),(52,'digQ82Dwj3Lmjgp','BIOMIO_Intu7NB3P9oWfLB.txt','target.com','0000-00-00 00:00:00');
/*!40000 ALTER TABLE `TempWebsiteCodes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TrainingData`
--

DROP TABLE IF EXISTS `TrainingData`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TrainingData` (
  `probe_id` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `data` longblob NOT NULL,
  PRIMARY KEY (`probe_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TrainingData`
--

LOCK TABLES `TrainingData` WRITE;
/*!40000 ALTER TABLE `TrainingData` DISABLE KEYS */;
/*!40000 ALTER TABLE `TrainingData` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `UILog`
--

DROP TABLE IF EXISTS `UILog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `UILog` (
  `id` int(21) NOT NULL AUTO_INCREMENT,
  `table_name` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `record_id` int(20) NOT NULL,
  `change_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UILog`
--

LOCK TABLES `UILog` WRITE;
/*!40000 ALTER TABLE `UILog` DISABLE KEYS */;
/*!40000 ALTER TABLE `UILog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `UserInfo`
--

DROP TABLE IF EXISTS `UserInfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `UserInfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `profileId` int(11) NOT NULL,
  `firstName` varchar(30) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `lastName` varchar(30) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `fingerprints` varchar(30) COLLATE latin1_general_ci NOT NULL DEFAULT '[0,0,0,0,0,0,0,0,0,0]',
  `face` tinyint(1) NOT NULL DEFAULT '0',
  `voice` tinyint(1) NOT NULL,
  `motto` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `address` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '{"street1":"", "street2":"", "continent": "", "country": "", "province": "", "region": "", "city": "","postcode": ""}',
  `bday` date NOT NULL,
  `occupation` varchar(255) COLLATE latin1_general_ci NOT NULL,
  `education` enum('Doctoral or professional degree','Master degree','Bachelor degree','Associate degree','Some college','High school','Less than high school') COLLATE latin1_general_ci NOT NULL,
  `socialBar` varchar(100) COLLATE latin1_general_ci NOT NULL DEFAULT '{"facebook":"", "twitter":"", "linkedin": "", "google": ""}',
  `notifications` varchar(50) COLLATE latin1_general_ci NOT NULL DEFAULT '[0, 0, 0]',
  `dateCreated` datetime NOT NULL,
  `dateModified` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=140 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UserInfo`
--

LOCK TABLES `UserInfo` WRITE;
/*!40000 ALTER TABLE `UserInfo` DISABLE KEYS */;
INSERT INTO `UserInfo` VALUES (121,1,'alex','lomov','[0,0,0,0,0,0,0,0,0,0]',0,0,'','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}','0000-00-00','','Doctoral or professional degree','{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','[0, 0, 0]','2015-04-15 18:50:02','2015-06-02 18:51:59'),(122,6,'admin','admin','[0,0,0,0,0,0,0,0,0,0]',0,0,'','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}','0000-00-00','','Doctoral or professional degree','{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','[0, 0, 0]','2015-04-20 08:16:30','2015-04-20 08:16:30'),(123,4,'Dan','Itkis','[0,0,0,0,0,0,\"2\",0,0,0]',0,0,'','{\"street1\":\"\",\"street2\":\"\",\"continent\":\"\",\"country\":\"\",\"province\":\"\",\"region\":\"\",\"city\":\"\",\"postcode\":\"\"}','0000-00-00','','Doctoral or professional degree','{\"facebook\":\"\",\"twitter\":\"\",\"linkedin\":\"\",\"google\":\"\"}','[0,0,0]','2015-04-20 08:23:13','2015-06-02 18:52:06'),(124,8,'Dan','Itkis','[0,0,0,0,0,0,0,0,0,0]',0,0,'','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}','0000-00-00','','Doctoral or professional degree','{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','[0, 0, 0]','2015-04-20 08:27:19','2015-04-20 08:27:19'),(125,9,'Alexander','Lomov','[0,0,0,0,0,0,0,0,0,0]',0,0,'','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}','0000-00-00','','Doctoral or professional degree','{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','[0, 0, 0]','2015-04-22 01:40:01','2015-04-22 01:40:01'),(126,10,'Test','Account','[0,0,0,0,0,0,0,0,0,0]',0,0,'','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}','0000-00-00','','Doctoral or professional degree','{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','[0, 0, 0]','2015-04-22 01:47:38','2015-04-22 01:47:38'),(127,11,'Guest','User','[\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"',1,0,'','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}','0000-00-00','','Doctoral or professional degree','{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','[0, 0, 0]','2015-04-24 12:35:26','2015-06-08 10:14:12'),(128,12,'Andriy','Lobashchuk','[0,0,0,0,0,0,0,0,0,0]',0,0,'','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}','0000-00-00','','Doctoral or professional degree','{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','[0, 0, 0]','2015-05-15 03:56:23','2015-05-15 03:56:23'),(129,13,'Andriy','Lobashchuk','[0,0,0,0,0,0,0,0,0,0]',0,0,'','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}','0000-00-00','','Doctoral or professional degree','{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','[0, 0, 0]','2015-05-15 03:57:40','2015-05-15 03:57:40'),(130,14,'test1','test1','[0,0,0,0,0,0,0,0,0,0]',0,0,'','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}','0000-00-00','','Doctoral or professional degree','{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','[0, 0, 0]','2015-05-15 10:11:55','2015-05-15 10:11:55'),(132,16,'','','[0,0,0,0,0,0,0,0,0,0]',0,0,'','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}','0000-00-00','','Doctoral or professional degree','{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','[0, 0, 0]','2015-05-20 06:38:08','2015-05-20 06:38:08'),(133,17,'','','[0,0,0,0,0,0,0,0,0,0]',0,0,'','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}','0000-00-00','','Doctoral or professional degree','{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','[0, 0, 0]','2015-05-20 06:54:14','2015-05-20 06:54:14'),(134,18,'','','[0,0,0,0,0,0,0,0,0,0]',0,0,'','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}','0000-00-00','','Doctoral or professional degree','{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','[0, 0, 0]','2015-05-20 08:17:51','2015-05-20 08:17:51'),(135,19,'test2','test2','[0,0,0,0,0,0,0,0,0,0]',0,0,'','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}','0000-00-00','','Doctoral or professional degree','{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','[0, 0, 0]','2015-05-21 02:39:48','2015-05-21 02:39:48'),(136,20,'Alex','Chmykhalo','[0,0,0,0,0,0,0,0,0,0]',0,0,'','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}','0000-00-00','','Doctoral or professional degree','{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','[0, 0, 0]','2015-05-22 12:12:22','2015-05-22 12:12:22'),(137,21,'boris','test1','[\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"',1,0,'','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}','0000-00-00','','Doctoral or professional degree','{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','[0, 0, 0]','2015-05-25 00:28:22','2015-06-05 01:57:34'),(138,22,'','','[0,0,0,0,0,0,0,0,0,0]',0,0,'','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}','0000-00-00','','Doctoral or professional degree','{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','[0, 0, 0]','2015-06-04 09:22:26','2015-06-04 09:22:26'),(139,23,'Test','Acc','[0,0,0,0,0,0,0,0,0,0]',0,0,'','{\"street1\":\"\", \"street2\":\"\", \"continent\": \"\", \"country\": \"\", \"province\": \"\", \"region\": \"\", \"city\": \"\",\"postcode\": \"\"}','0000-00-00','','Doctoral or professional degree','{\"facebook\":\"\", \"twitter\":\"\", \"linkedin\": \"\", \"google\": \"\"}','[0, 0, 0]','2015-06-10 20:46:10','2015-06-10 20:46:10');
/*!40000 ALTER TABLE `UserInfo` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`biom`@`localhost`*/ /*!50003 TRIGGER `user_info_creation_time` BEFORE INSERT ON `UserInfo`
 FOR EACH ROW BEGIN
    SET NEW.dateCreated = NOW();
    SET NEW.dateModified = NOW();
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`biom`@`localhost`*/ /*!50003 TRIGGER `user_info_modification_time` BEFORE UPDATE ON `UserInfo`
 FOR EACH ROW BEGIN
    SET NEW.dateModified = NOW();
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `UserServices`
--

DROP TABLE IF EXISTS `UserServices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `UserServices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `profileId` int(11) NOT NULL,
  `serviceId` int(2) NOT NULL,
  `title` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '0',
  `device_token` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `date_created` datetime NOT NULL,
  `date_modified` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=154 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UserServices`
--

LOCK TABLES `UserServices` WRITE;
/*!40000 ALTER TABLE `UserServices` DISABLE KEYS */;
INSERT INTO `UserServices` VALUES (1,121,1,'device',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(8,121,1,'dfghj',0,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(9,121,1,'device6',0,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(5,121,1,'device4',0,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(7,121,1,'device5',0,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(10,121,1,'device7',0,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(11,121,1,'device8',0,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(12,121,1,'device9',0,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(13,121,1,'device10',0,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(91,4,1,'iphone',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(15,5,1,'my iphone',0,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(16,10,1,'myphone',0,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(17,10,1,'myipad',0,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(130,23,2,'',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(125,11,2,'',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(21,14,2,'',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(23,11,2,'',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(24,11,2,'',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(25,11,2,'',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(26,11,2,'',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(27,11,2,'',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(28,11,2,'',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(29,11,2,'',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(30,11,2,'',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(134,11,1,'VAkoms6Plus',1,'7439ef160abe4af57f0b2f567b13b242','0000-00-00 00:00:00','0000-00-00 00:00:00'),(85,4,2,'',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(34,11,2,'',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(35,11,2,'',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(36,11,2,'',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(37,11,2,'',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(38,11,2,'',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(40,11,2,'',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(51,11,2,'',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(42,11,2,'',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(77,11,2,'',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(62,20,2,'',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(63,20,1,'device',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(102,21,1,'i23',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(65,21,2,'',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(139,11,1,'vk_i5',1,'18b863486b7e6cec5016016ef46b0d25','0000-00-00 00:00:00','0000-00-00 00:00:00'),(68,11,2,'',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(69,11,2,'',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(70,11,2,'',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(71,11,2,'',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(79,11,2,'',1,'','0000-00-00 00:00:00','0000-00-00 00:00:00'),(136,23,1,'Magic Device',1,'88b960b1c9805fb586810f270def7378','0000-00-00 00:00:00','0000-00-00 00:00:00'),(137,23,1,'Verify Device Test',0,'','0000-00-00 00:00:00','0000-00-00 00:00:00');
/*!40000 ALTER TABLE `UserServices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `VerificationCodes`
--

DROP TABLE IF EXISTS `VerificationCodes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `VerificationCodes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `application` tinyint(1) NOT NULL COMMENT '1 for application, 2 for extention',
  `device_id` int(11) NOT NULL DEFAULT '0',
  `status` tinyint(1) NOT NULL,
  `profileId` int(11) NOT NULL,
  `date_created` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=569 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `VerificationCodes`
--

LOCK TABLES `VerificationCodes` WRITE;
/*!40000 ALTER TABLE `VerificationCodes` DISABLE KEYS */;
INSERT INTO `VerificationCodes` VALUES (1,'krAhY9Ba',1,0,3,110,'2015-03-30 07:51:18'),(2,'G6IiuqY0',1,0,0,110,'2015-03-30 07:51:20'),(3,'uieo7QqB',1,0,0,110,'2015-03-30 07:51:23'),(4,'VONJqbw1',1,0,0,110,'2015-03-30 07:51:24'),(5,'g9sHhCfn',1,0,0,110,'2015-03-30 07:53:27'),(6,'gjFKyYXz',2,0,0,110,'2015-03-30 07:55:03'),(7,'IfvLwH27',2,0,0,110,'2015-03-30 07:55:04'),(8,'0EaUgjKW',2,0,3,110,'2015-03-30 07:55:46'),(9,'GpDW0ev7',1,0,0,110,'2015-03-30 07:56:24'),(10,'SMRmwVHn',1,0,0,110,'2015-03-30 07:56:26'),(11,'XrBz4nck',1,0,0,110,'2015-03-30 07:56:28'),(12,'0kZaESe6',1,0,0,110,'2015-03-30 11:20:11'),(13,'oL7gOeq3',1,0,0,110,'2015-03-30 11:20:13'),(14,'TOXdL2PF',1,0,0,110,'2015-03-30 11:20:15'),(15,'6nLthbax',1,0,0,110,'2015-03-30 11:20:16'),(16,'zaZCeqPL',1,0,0,110,'2015-03-30 11:20:17'),(17,'UZ2X8jbL',1,0,0,110,'2015-03-30 11:21:07'),(18,'kw1MYvjx',1,0,0,110,'2015-03-30 11:21:09'),(19,'3PZIUdfA',1,0,0,110,'2015-03-30 11:21:11'),(20,'b39GDPge',1,0,0,110,'2015-03-30 11:21:13'),(21,'m9e6M4aO',1,0,0,110,'2015-03-30 11:21:14'),(22,'cU4Z7GOf',1,0,0,110,'2015-03-30 11:21:57'),(23,'g7FMR18N',1,0,0,110,'2015-03-30 11:21:59'),(24,'IqczZ4Ba',1,0,0,110,'2015-03-30 11:22:00'),(25,'4Qjcu0hw',1,0,0,110,'2015-03-30 11:22:01'),(26,'jbsCg7VU',1,0,0,110,'2015-03-30 11:22:03'),(27,'AaWupEek',1,0,0,110,'2015-03-30 11:22:05'),(28,'V1xjsazK',1,0,0,110,'2015-03-30 11:22:05'),(29,'NS9pDrhV',1,0,0,110,'2015-03-30 11:22:09'),(30,'0JlgqZSd',1,0,0,110,'2015-03-30 11:22:11'),(31,'c7tK5Tvh',1,0,0,110,'2015-03-30 11:22:12'),(32,'nwlALIBr',1,0,0,110,'2015-03-30 11:24:17'),(33,'dsfx7uRD',1,0,0,110,'2015-03-30 11:24:19'),(34,'587XgwTJ',1,0,0,110,'2015-03-30 11:24:21'),(35,'cEZ35C1R',1,0,0,110,'2015-03-30 11:24:21'),(36,'bV1jk28z',1,0,0,110,'2015-03-30 11:24:21'),(37,'g9i7oYRT',1,0,0,110,'2015-03-30 11:24:22'),(38,'rJiEPtdo',1,0,0,110,'2015-03-30 11:24:22'),(39,'aAWN5861',1,0,0,110,'2015-03-30 11:24:22'),(40,'SbGRlaKX',1,0,0,110,'2015-03-30 11:24:22'),(41,'KNyxAgl1',1,0,0,110,'2015-03-30 11:24:22'),(42,'6pUHBPb1',1,0,0,110,'2015-03-30 11:24:23'),(43,'0KWw5NlO',1,0,0,110,'2015-03-30 11:24:23'),(44,'qzM6LgfI',1,0,0,110,'2015-03-30 11:24:23'),(45,'2nYKiCvw',1,0,0,110,'2015-03-30 11:24:23'),(46,'V9rOpYel',1,0,0,110,'2015-03-30 11:24:24'),(47,'wWfRd2UK',1,0,0,110,'2015-03-30 11:24:24'),(48,'3kpLeTF4',1,0,0,110,'2015-03-30 11:24:24'),(49,'8IBUP36c',1,0,0,110,'2015-03-30 11:24:36'),(50,'Mt5WjNgG',1,0,0,110,'2015-03-30 11:24:39'),(51,'EqRzOm5d',1,0,0,110,'2015-03-30 11:24:40'),(52,'iIpPy4bl',1,0,0,110,'2015-03-30 11:24:42'),(53,'GTk9syCl',1,0,0,110,'2015-03-30 11:24:45'),(54,'D8GpSWuk',1,0,0,110,'2015-03-30 11:24:46'),(55,'XbQsfuIR',1,0,0,110,'2015-03-30 11:24:48'),(56,'MwBPuAX3',1,0,0,110,'2015-03-30 11:24:49'),(57,'AILdN9rK',1,0,0,110,'2015-03-30 11:24:50'),(58,'zToC31ID',1,0,0,110,'2015-03-30 11:24:51'),(59,'j8zXtwEm',1,0,0,110,'2015-03-30 11:24:51'),(60,'ZXo70HKj',1,0,0,110,'2015-03-30 11:25:32'),(61,'2Zxkwun4',1,0,0,110,'2015-03-30 11:25:33'),(62,'uB8J9Urg',1,0,0,110,'2015-03-30 11:25:34'),(63,'MyQVxilp',1,0,0,110,'2015-03-30 11:25:34'),(64,'0fA2YzQO',1,0,0,110,'2015-03-30 11:25:36'),(65,'j4HNG3yg',1,0,0,110,'2015-03-30 11:25:36'),(66,'t5vJYg0p',1,0,0,110,'2015-03-30 11:25:37'),(67,'1YBtku26',1,0,0,110,'2015-03-30 11:25:38'),(68,'aUt4P17j',1,0,0,110,'2015-03-30 11:25:38'),(69,'YmK9vdk8',1,0,1,110,'2015-03-30 11:25:42'),(70,'hp4j1UoY',1,0,1,106,'2015-03-31 15:51:06'),(71,'YaXCWIt3',1,0,0,121,'2015-04-06 15:13:03'),(72,'FkCr8VRy',1,0,0,121,'2015-04-06 15:13:06'),(73,'BfMAp26Y',1,0,0,121,'2015-04-06 16:07:44'),(74,'vpMUbeLa',1,0,0,121,'2015-04-06 16:11:46'),(75,'bMlUeIA8',1,0,0,121,'2015-04-06 16:12:25'),(76,'t1Vj64C3',1,0,0,121,'2015-04-06 16:13:07'),(77,'SqfncXIg',1,0,0,121,'2015-04-06 16:14:05'),(78,'d8XjOqQb',1,0,0,121,'2015-04-06 16:14:39'),(79,'YtisBzO0',1,0,0,121,'2015-04-06 16:15:01'),(80,'N5KwuZ3L',1,0,0,121,'2015-04-06 16:15:52'),(81,'eP6ZStGJ',1,0,0,121,'2015-04-06 16:16:33'),(82,'tmwhLU7W',1,0,0,121,'2015-04-06 16:17:20'),(83,'u9ex7rSJ',1,0,0,121,'2015-04-06 16:33:13'),(84,'M1fLorPd',1,0,0,121,'2015-04-06 16:33:15'),(85,'Wb5K90Xa',1,0,0,121,'2015-04-06 16:33:16'),(86,'afUO4qzd',1,0,0,121,'2015-04-06 16:33:17'),(87,'cD6SCoNg',1,0,0,121,'2015-04-06 16:33:48'),(88,'4Fr7nWpk',1,0,0,121,'2015-04-06 16:33:50'),(89,'EVq4UN32',1,0,0,121,'2015-04-06 16:33:52'),(90,'wNdvrgW9',1,0,0,121,'2015-04-06 16:33:53'),(91,'7acLrgoE',1,0,0,121,'2015-04-06 16:33:54'),(92,'iGVxKwuM',1,0,0,121,'2015-04-06 16:33:55'),(93,'hlE3QXfo',1,0,0,121,'2015-04-06 16:34:30'),(94,'JTfhqzjr',1,0,0,121,'2015-04-06 16:34:32'),(95,'oWGBjQYF',1,0,0,121,'2015-04-06 16:34:57'),(96,'U875uyMQ',1,0,0,121,'2015-04-06 16:35:27'),(97,'U3GW2ZHM',1,0,0,121,'2015-04-06 16:36:26'),(98,'mH5lYKZA',1,0,0,121,'2015-04-06 16:36:57'),(99,'4mnudxwA',1,0,0,121,'2015-04-06 16:38:03'),(100,'RxtLJjXT',1,0,0,121,'2015-04-06 16:38:22'),(101,'nuNxT8Iy',1,0,0,121,'2015-04-06 16:38:24'),(102,'1xytQmne',1,0,0,121,'2015-04-06 16:38:49'),(103,'ckJLbize',1,0,0,121,'2015-04-06 16:38:53'),(104,'NUZmk0V8',1,0,0,121,'2015-04-06 16:39:38'),(105,'Aq8wnXmf',1,0,0,121,'2015-04-06 16:45:31'),(106,'nmEw4LYG',1,0,0,121,'2015-04-06 16:46:19'),(107,'lbp9WxJ6',1,0,0,121,'2015-04-06 16:46:47'),(108,'SoZCOh3V',1,0,0,121,'2015-04-06 16:53:00'),(109,'f2pV1Itz',1,5,0,121,'2015-04-07 12:58:13'),(110,'eQrvW8V9',1,6,0,121,'2015-04-07 12:59:50'),(111,'pBzRWhbd',1,6,0,121,'2015-04-07 13:00:27'),(112,'xLvAfUIG',1,6,0,121,'2015-04-07 13:00:33'),(113,'d5hsLyTB',1,7,0,121,'2015-04-07 13:42:34'),(114,'lqRoG9C1',1,1,0,121,'2015-04-07 13:58:44'),(115,'8GclY6OI',1,4,0,121,'2015-04-07 13:58:46'),(116,'EhyF36bp',1,5,0,121,'2015-04-07 13:58:48'),(117,'0eKAMgyt',1,7,0,121,'2015-04-07 13:58:50'),(118,'6oAw3BbX',1,5,0,121,'2015-04-07 13:58:57'),(119,'MCr85cX2',1,7,0,121,'2015-04-07 14:42:45'),(120,'HUlDo1TI',1,1,0,121,'2015-04-07 14:59:22'),(121,'xuzMKWUj',1,4,0,121,'2015-04-07 14:59:39'),(122,'g6dT8NRa',1,8,0,121,'2015-04-07 14:59:43'),(123,'IKLxzpd1',1,4,0,121,'2015-04-07 14:59:55'),(124,'aUN0hlIg',1,4,0,121,'2015-04-07 14:59:57'),(125,'XIRCur0P',2,0,0,121,'2015-04-08 11:11:37'),(126,'RerGCNqy',1,7,0,121,'2015-04-08 13:47:44'),(127,'Ywt2rfQe',1,5,0,121,'2015-04-08 13:48:05'),(128,'iqslM28L',1,8,0,121,'2015-04-08 13:48:06'),(129,'Woi0FK7w',1,1,0,121,'2015-04-08 13:48:07'),(130,'avDiLUze',1,8,0,121,'2015-04-08 16:41:05'),(131,'ozb4HqjO',1,9,0,121,'2015-04-08 16:41:14'),(132,'k4J95TED',1,10,0,121,'2015-04-08 16:41:16'),(133,'O3iWZhMN',1,11,0,121,'2015-04-08 16:41:19'),(134,'yN36itah',1,12,0,121,'2015-04-08 16:41:21'),(135,'6iXHrRVU',1,13,1,121,'2015-04-08 16:41:25'),(136,'t2a386Wh',2,0,0,121,'2015-04-08 17:22:25'),(137,'eZWFU391',2,0,0,121,'2015-04-08 17:23:11'),(138,'9WOpVXbD',2,0,0,121,'2015-04-08 17:24:25'),(139,'vbSK3JFQ',2,0,0,121,'2015-04-08 17:24:28'),(140,'UPQy36Xa',2,0,0,121,'2015-04-08 17:25:08'),(141,'f0DHT6JE',2,0,0,121,'2015-04-08 17:25:44'),(142,'RLwvIbe2',2,0,0,121,'2015-04-08 17:26:03'),(143,'OAiT8RD1',2,0,0,121,'2015-04-08 17:26:19'),(144,'tDUyVR12',2,0,0,121,'2015-04-08 17:26:22'),(145,'FBD2fA8n',2,0,0,121,'2015-04-08 17:26:47'),(146,'VcY9xXdT',2,0,0,121,'2015-04-08 17:27:02'),(147,'4PlvenKh',2,0,0,121,'2015-04-08 17:28:23'),(148,'clKGtLba',2,0,0,121,'2015-04-08 17:28:25'),(149,'tuGJcsLM',2,0,1,121,'2015-04-08 17:29:11'),(150,'QTOkinXr',1,14,0,4,'2015-04-15 18:52:25'),(151,'Y7HCNhi2',1,15,0,5,'2015-04-15 18:52:41'),(152,'Bx4LO1XU',1,15,0,5,'2015-04-15 18:52:54'),(153,'cvzEZIPw',1,0,0,4,'2015-04-15 18:53:20'),(154,'XBQw5nTL',1,15,0,5,'2015-04-15 18:53:52'),(155,'NZu9PGgE',1,15,0,5,'2015-04-15 18:53:54'),(156,'9ny8SBrN',1,15,0,5,'2015-04-15 18:53:55'),(157,'2JdZxbl5',1,15,0,5,'2015-04-15 18:53:56'),(158,'aTshf3b0',1,15,0,5,'2015-04-15 18:53:57'),(159,'B6Nsb2UG',1,15,1,5,'2015-04-15 18:53:58'),(160,'JfqI3aLs',1,16,0,10,'2015-04-22 02:51:41'),(161,'eGg1K2sO',1,16,0,10,'2015-04-22 02:51:47'),(162,'Yun7h5oF',1,17,1,10,'2015-04-22 02:51:58'),(163,'z3d71Qiy',1,18,0,11,'2015-04-24 12:57:28'),(164,'IvbEjKJD',1,18,0,11,'2015-04-28 14:33:04'),(165,'xGAD5dkX',2,0,0,11,'2015-04-28 14:35:21'),(166,'diCFAesU',2,0,0,11,'2015-04-28 14:35:24'),(167,'0uHKOj7k',2,0,0,11,'2015-04-28 14:35:31'),(168,'u60EtpGg',2,0,0,11,'2015-04-28 14:35:40'),(169,'dFwuIqNY',2,0,0,11,'2015-04-29 09:59:48'),(170,'hj5Lpav1',1,18,0,11,'2015-04-29 10:51:00'),(171,'ToEvpaOY',1,19,0,11,'2015-04-29 11:10:33'),(172,'oebEuY8F',1,20,0,11,'2015-04-29 13:23:01'),(186,'pfS1dsV2',2,0,0,14,'2015-05-18 08:36:45'),(198,'kf7qNHgB',2,0,0,11,'2015-05-19 07:39:31'),(197,'PfIRpF4T',2,0,0,11,'2015-05-19 07:33:44'),(196,'NHUjpmGf',2,0,0,11,'2015-05-19 07:23:02'),(195,'CcIPGXxq',2,0,0,11,'2015-05-19 07:21:19'),(194,'dSzeyOXt',2,0,0,11,'2015-05-19 06:34:43'),(179,'6ZJ8DHd2',2,0,0,14,'2015-05-15 10:17:01'),(180,'HlbYSyWh',2,0,0,14,'2015-05-15 10:28:12'),(187,'qpWiERBd',2,0,0,14,'2015-05-18 08:37:49'),(188,'Aq01izYV',2,0,0,14,'2015-05-18 08:39:16'),(189,'qpkfNXz0',2,0,0,14,'2015-05-18 08:58:33'),(190,'rs2oFGJq',2,0,0,14,'2015-05-18 09:00:28'),(191,'y6wAjadM',2,0,0,14,'2015-05-18 09:01:36'),(192,'jrLJpVSG',2,0,0,14,'2015-05-18 09:03:45'),(193,'RFZifczE',2,0,1,14,'2015-05-18 09:06:25'),(199,'7Py9qUmQ',2,0,0,11,'2015-05-19 07:42:21'),(200,'OEAhFGDj',2,0,0,11,'2015-05-19 19:00:40'),(201,'W2hRGcpF',2,0,0,11,'2015-05-19 20:07:41'),(202,'NezSrYcQ',1,18,0,11,'2015-05-19 20:21:48'),(203,'qK48Pj5m',1,18,0,11,'2015-05-19 20:23:36'),(204,'R84rjovk',1,20,0,11,'2015-05-19 20:24:23'),(205,'sf1bIoQx',1,20,0,11,'2015-05-19 20:24:59'),(206,'QfJbVF5D',1,18,0,11,'2015-05-19 20:25:58'),(207,'SRQAqNaX',1,18,0,11,'2015-05-19 20:29:07'),(208,'fRJbETMg',2,0,0,11,'2015-05-19 20:30:44'),(209,'I2FkPzoB',2,0,0,11,'2015-05-19 20:32:05'),(210,'YyZVnOKq',2,0,0,11,'2015-05-19 20:33:07'),(211,'yTWKLY40',1,20,0,11,'2015-05-19 20:33:46'),(212,'fqdH3F8G',1,20,0,11,'2015-05-19 20:34:22'),(213,'RaCeoz4A',1,31,0,11,'2015-05-19 20:37:32'),(214,'WLuwZ0Xt',1,32,0,11,'2015-05-19 20:38:06'),(215,'XVfZQIJq',1,33,0,11,'2015-05-19 20:39:27'),(216,'OgrRvAxq',2,0,0,11,'2015-05-19 20:48:19'),(217,'EV6L0m3a',0,0,0,11,'2015-05-20 03:26:22'),(218,'UJrKieH4',2,0,0,11,'2015-05-20 06:21:40'),(219,'PjH3UeNE',2,0,0,11,'2015-05-20 06:23:46'),(220,'T7r6pfDV',2,0,0,11,'2015-05-20 06:24:41'),(221,'fNIcDQGJ',2,0,0,11,'2015-05-20 06:30:40'),(222,'fKON9uPd',2,0,0,11,'2015-05-21 11:38:00'),(223,'Ic5tTsyu',1,39,0,11,'2015-05-21 11:50:35'),(224,'BgC41UQx',2,0,0,11,'2015-05-21 12:17:07'),(225,'VQDKhzE7',2,0,0,11,'2015-05-21 12:24:06'),(226,'w7AP3FHC',1,41,0,11,'2015-05-21 12:25:38'),(227,'ymDcoGWp',2,0,0,11,'2015-05-21 12:29:14'),(228,'B3iAsaZO',1,43,0,11,'2015-05-21 12:33:22'),(229,'0pgXIr4P',1,44,0,11,'2015-05-21 12:42:48'),(230,'egrbXxGP',0,0,0,11,'2015-05-21 12:46:53'),(231,'OCVw3Dtx',1,45,0,11,'2015-05-21 13:50:33'),(232,'ZK2n9PR7',1,46,0,11,'2015-05-21 13:53:06'),(233,'ifSAjMZU',1,47,0,11,'2015-05-21 13:54:29'),(234,'ZYUrEHaL',1,48,0,11,'2015-05-21 13:56:23'),(235,'0TuxhN1b',1,49,0,11,'2015-05-21 14:00:22'),(236,'aMWerqNL',1,50,0,11,'2015-05-21 14:04:26'),(237,'mGdWVPbM',0,0,0,11,'2015-05-21 14:40:16'),(238,'9wkDKPLr',0,18,0,11,'2015-05-21 14:53:55'),(239,'CKl6NA39',0,18,0,11,'2015-05-21 14:54:28'),(240,'wryO396C',0,18,0,11,'2015-05-21 14:56:33'),(241,'WPXJ36Dv',0,18,0,11,'2015-05-21 14:57:36'),(242,'DspNaYnh',2,0,0,11,'2015-05-22 02:50:11'),(243,'zdJIYBV5',1,52,0,11,'2015-05-22 02:59:27'),(244,'0DLZnHjK',1,53,0,11,'2015-05-22 03:02:35'),(245,'f8Vun09m',1,54,0,11,'2015-05-22 03:10:51'),(246,'gMPCHB40',0,54,0,11,'2015-05-22 03:12:09'),(247,'qdcRFw35',1,55,0,11,'2015-05-22 03:49:30'),(248,'knalN78d',1,56,0,11,'2015-05-22 03:51:57'),(249,'G17dB9C6',1,57,0,11,'2015-05-22 08:04:38'),(250,'wyHlJXQS',0,57,0,11,'2015-05-22 08:05:57'),(251,'xpCcvSwN',1,58,0,11,'2015-05-22 09:17:08'),(252,'EGF8pV5g',0,58,0,11,'2015-05-22 09:17:53'),(253,'DTgzuZNl',1,59,0,11,'2015-05-22 09:30:06'),(254,'7Ttq8LN4',0,59,0,11,'2015-05-22 09:30:37'),(255,'HwKyGBkA',0,59,0,11,'2015-05-22 09:31:51'),(256,'3JjLTbZv',1,60,0,11,'2015-05-22 11:08:43'),(257,'TlOQhsYH',1,61,0,11,'2015-05-22 11:26:15'),(258,'o2CdsW6T',2,0,3,20,'2015-05-22 12:20:26'),(259,'03amk1oZ',1,63,3,20,'2015-05-22 12:31:40'),(260,'ml9gjoqt',1,64,0,21,'2015-05-25 00:29:42'),(261,'yCGpE4Nh',2,0,3,21,'2015-05-25 00:32:30'),(262,'Y5aGWf4B',0,64,0,21,'2015-05-25 01:21:04'),(263,'8Jz7NlhR',1,66,0,21,'2015-05-25 01:22:37'),(264,'iGeExyaC',0,66,0,21,'2015-05-25 01:26:08'),(265,'zKcfBSNs',0,66,0,21,'2015-05-25 01:26:18'),(266,'5zDwLNaO',0,66,0,21,'2015-05-25 01:26:27'),(267,'EDlCFh2p',0,66,0,21,'2015-05-25 01:28:26'),(268,'f9TuPnYL',0,66,0,21,'2015-05-25 01:30:12'),(269,'9xYIlfBW',0,66,0,21,'2015-05-25 01:31:54'),(270,'lyHvLOTb',0,61,0,11,'2015-05-25 03:30:11'),(271,'SoTcxnPp',0,61,0,11,'2015-05-25 05:13:27'),(272,'OWGZxQtr',1,32,0,11,'2015-05-25 05:14:16'),(273,'hCvgaosH',0,61,0,11,'2015-05-25 05:14:26'),(274,'PoLyONm8',0,18,0,11,'2015-05-25 09:53:15'),(275,'OVhWk2DE',0,61,0,11,'2015-05-25 09:56:43'),(276,'2tEvN0Jm',0,18,0,11,'2015-05-25 09:58:47'),(277,'6abgc0Rk',0,18,0,11,'2015-05-25 10:01:07'),(278,'xXdanMGU',0,18,0,11,'2015-05-25 10:04:52'),(279,'WPaJK7tM',0,18,0,11,'2015-05-25 10:05:48'),(280,'RPn1UDCt',0,18,0,11,'2015-05-25 10:07:25'),(281,'FHVq1j8h',0,18,0,11,'2015-05-25 10:08:02'),(282,'VOu57QcU',1,67,0,11,'2015-05-25 10:15:03'),(283,'JEpoAfc6',0,18,0,11,'2015-05-25 10:29:13'),(284,'ycKo5Cv6',0,18,0,11,'2015-05-25 10:40:24'),(285,'cu2rig1I',0,18,0,11,'2015-05-25 10:41:18'),(286,'Z7qBxW56',0,61,0,11,'2015-05-25 10:50:45'),(287,'V64pOcl1',0,61,0,11,'2015-05-25 11:13:24'),(288,'WEF0o5Am',2,0,0,11,'2015-05-26 14:56:49'),(289,'f4pJaeK5',2,0,0,11,'2015-05-26 15:02:39'),(290,'ADUSh2yz',2,0,0,11,'2015-05-26 15:04:50'),(291,'46RwmUEG',2,0,0,11,'2015-05-26 15:05:38'),(292,'cqepIiyO',2,0,0,11,'2015-05-26 15:06:45'),(293,'7Qv1LXKt',0,18,0,11,'2015-05-26 20:02:18'),(294,'9XDAdkvH',0,18,0,11,'2015-05-26 20:03:32'),(295,'iTZF9mIf',0,18,0,11,'2015-05-26 20:06:32'),(296,'FAZbPJEe',0,18,0,11,'2015-05-26 20:08:22'),(297,'FwZX0OHC',0,18,0,11,'2015-05-26 20:10:36'),(298,'wkgCcjvW',0,18,0,11,'2015-05-26 20:12:32'),(299,'rkQU9lpx',1,67,0,11,'2015-05-26 20:15:08'),(300,'SVie1uTk',1,32,0,11,'2015-05-26 20:15:51'),(301,'CIO6tjok',1,72,0,11,'2015-05-26 20:19:05'),(302,'nVHx7bKC',1,72,0,11,'2015-05-27 06:42:00'),(303,'Crv5PYnb',1,73,0,11,'2015-05-27 06:43:44'),(304,'Ioj3J0pr',0,73,0,11,'2015-05-27 06:44:50'),(305,'ebRT874Z',0,73,0,11,'2015-05-27 06:50:45'),(306,'irM49zA6',0,73,0,11,'2015-05-27 06:54:40'),(307,'5puqPEAL',0,73,0,11,'2015-05-27 06:57:36'),(308,'E6CTMnuR',0,73,0,11,'2015-05-27 07:04:35'),(309,'W8k3KndN',1,74,0,11,'2015-05-27 10:05:42'),(310,'jk76gxPF',0,74,0,11,'2015-05-27 10:09:04'),(311,'tJIB5jQF',0,74,0,11,'2015-05-27 10:11:13'),(312,'L8JgqNfu',0,74,0,11,'2015-05-27 10:11:20'),(313,'x8m3TMio',0,18,0,11,'2015-05-27 10:54:25'),(314,'1mKT4lUe',0,19,0,11,'2015-05-27 10:54:27'),(315,'OFARYny7',0,20,0,11,'2015-05-27 10:54:29'),(316,'dp24vCs3',0,31,0,11,'2015-05-27 10:54:31'),(317,'c6TI5ndP',0,18,0,11,'2015-05-27 10:57:20'),(318,'payGroUA',0,19,0,11,'2015-05-27 10:57:21'),(319,'EtRnpwSL',0,20,0,11,'2015-05-27 10:57:23'),(320,'sg8MS7Oa',0,31,0,11,'2015-05-27 10:57:23'),(321,'UmrlfpRh',0,18,0,11,'2015-05-27 10:57:42'),(322,'cFzNhI89',0,18,0,11,'2015-05-27 11:21:56'),(323,'NteDbO5J',0,19,0,11,'2015-05-27 11:21:57'),(324,'MFnIQ6ir',0,20,0,11,'2015-05-27 11:21:59'),(325,'iofSMbyT',0,31,0,11,'2015-05-27 11:22:01'),(326,'fKPr9gk3',0,18,0,11,'2015-05-27 11:24:27'),(327,'awqE9vjb',0,18,0,11,'2015-05-27 11:27:45'),(328,'jV1H6fK8',0,19,0,11,'2015-05-27 11:27:46'),(329,'aUORwB2v',0,18,0,11,'2015-05-27 11:28:33'),(330,'rJbmGayz',0,19,0,11,'2015-05-27 11:28:35'),(331,'ts4hHjvP',0,18,0,11,'2015-05-27 11:30:36'),(332,'Xo61eBip',0,19,0,11,'2015-05-27 11:30:42'),(333,'jn5BgWo6',0,18,0,11,'2015-05-27 11:32:54'),(334,'kisMPExG',0,19,0,11,'2015-05-27 11:32:55'),(335,'G2FH0Ddt',0,20,0,11,'2015-05-27 11:32:56'),(336,'wTxujhKn',0,31,0,11,'2015-05-27 11:32:57'),(337,'2qKjJ8zH',0,18,0,11,'2015-05-27 11:36:46'),(338,'xpSJmag6',0,19,0,11,'2015-05-27 11:36:47'),(339,'8Pf46EGN',0,20,0,11,'2015-05-27 11:36:49'),(340,'PJ8OwjDW',0,18,0,11,'2015-05-27 11:37:49'),(341,'EcWyfYS6',0,19,0,11,'2015-05-27 11:37:50'),(342,'BKtC2nYE',0,20,0,11,'2015-05-27 11:37:51'),(343,'ZlAm2y19',0,18,0,11,'2015-05-27 11:44:15'),(344,'9tLOEHSD',0,19,0,11,'2015-05-27 11:44:16'),(345,'B0D1eJXz',0,20,0,11,'2015-05-27 11:44:17'),(346,'GcmK84AP',0,31,0,11,'2015-05-27 11:44:18'),(347,'eYlGZ0FU',0,74,0,11,'2015-05-27 13:19:09'),(348,'QVUeBT4f',0,18,0,11,'2015-05-27 18:34:17'),(349,'poj0aGtO',1,14,0,4,'2015-06-02 18:55:49'),(350,'iCxvYGcP',2,0,0,4,'2015-06-02 18:57:56'),(351,'wHq62ofO',2,0,0,4,'2015-06-02 18:58:24'),(352,'RDzEZaHL',2,0,0,4,'2015-06-02 19:02:34'),(353,'VWpL2PX3',2,0,0,4,'2015-06-02 19:14:43'),(354,'Kbf7l5G3',1,75,0,11,'2015-06-03 01:19:05'),(355,'Gr2YdQE4',1,75,0,11,'2015-06-03 01:22:50'),(356,'wPI4iVGr',1,75,0,11,'2015-06-03 01:33:24'),(357,'SmPCEqOG',2,0,0,11,'2015-06-03 01:39:04'),(358,'zIjVnTAS',2,0,0,11,'2015-06-03 01:56:32'),(359,'xvo3eMjW',2,0,0,11,'2015-06-03 08:59:09'),(360,'OA3mv0pl',2,0,0,11,'2015-06-03 09:05:08'),(361,'kK7dsGao',1,76,0,11,'2015-06-03 09:17:29'),(362,'yhjp2ZNR',2,0,0,11,'2015-06-03 10:28:26'),(363,'1wlXiuVZ',1,75,0,11,'2015-06-03 10:35:30'),(364,'p8IngTb6',1,78,0,11,'2015-06-03 10:38:04'),(365,'DagbWCr1',2,0,0,11,'2015-06-03 10:39:12'),(366,'mP7v5R2a',1,80,0,11,'2015-06-03 10:40:28'),(367,'veWcaCb4',1,81,0,11,'2015-06-03 10:41:09'),(368,'iFqDelYV',0,81,0,11,'2015-06-03 10:42:29'),(369,'7cCFwsSh',0,81,0,11,'2015-06-03 10:44:14'),(370,'DWSsBL70',0,32,0,11,'2015-06-03 11:18:36'),(371,'a3KlGBi9',1,82,0,11,'2015-06-03 11:20:19'),(372,'G8vhIqbt',0,32,0,11,'2015-06-03 11:43:42'),(373,'1ABfRsrI',1,83,0,21,'2015-06-03 15:19:39'),(374,'0trOiGag',0,32,0,11,'2015-06-03 15:21:24'),(375,'2tcUkAIV',0,83,0,21,'2015-06-03 15:22:16'),(376,'gVhEKcq0',0,83,0,21,'2015-06-03 15:22:22'),(377,'e18bXTuC',0,83,0,21,'2015-06-03 15:22:35'),(378,'IgPZDNLi',0,83,0,21,'2015-06-03 15:22:38'),(379,'ijJxGdSI',0,83,0,21,'2015-06-03 15:22:53'),(380,'v3bHkD7G',0,83,0,21,'2015-06-03 15:23:01'),(381,'T6oDuP10',0,82,0,11,'2015-06-03 15:26:51'),(382,'6zsmBa93',0,19,0,11,'2015-06-03 15:26:53'),(383,'4BKWjUNk',0,32,0,11,'2015-06-03 15:26:55'),(384,'w8pZGEQ9',0,32,0,11,'2015-06-03 15:27:07'),(385,'tlzYBwUV',0,32,0,11,'2015-06-03 15:27:13'),(386,'xyNqGviY',1,84,0,11,'2015-06-03 16:13:28'),(387,'JsLEwrSi',1,14,0,4,'2015-06-03 17:04:50'),(388,'3PpaXhYF',2,0,0,4,'2015-06-03 17:06:07'),(389,'yd3MI590',1,14,0,4,'2015-06-03 17:16:08'),(390,'rAYjgnq3',1,86,0,4,'2015-06-03 17:19:47'),(391,'bRL4wYgI',0,86,0,4,'2015-06-03 17:20:10'),(392,'7c234WOh',0,82,0,11,'2015-06-04 06:31:06'),(393,'CzmA1FL0',1,87,0,11,'2015-06-04 09:07:25'),(394,'FfxTr7Pl',1,88,0,11,'2015-06-04 09:29:30'),(395,'sYbVTRA3',1,89,0,11,'2015-06-04 09:49:46'),(396,'56VpQh8B',1,90,0,11,'2015-06-04 09:53:00'),(397,'MN3el4G5',0,90,0,11,'2015-06-04 09:54:14'),(398,'0Ag3946b',0,87,0,11,'2015-06-04 09:54:18'),(399,'SAGqez1E',0,90,0,11,'2015-06-04 10:09:51'),(400,'G6j7sYxk',0,90,0,11,'2015-06-04 10:10:13'),(401,'em6ByUp3',0,90,0,11,'2015-06-04 10:11:27'),(402,'1tuEL3mN',0,90,0,11,'2015-06-04 10:19:02'),(403,'XFrcMHuv',0,90,0,11,'2015-06-04 10:19:15'),(404,'UdoIrbcv',0,88,0,11,'2015-06-04 10:24:55'),(405,'jw6V1kHY',0,88,0,11,'2015-06-04 10:30:45'),(406,'bosEWdX5',0,90,0,11,'2015-06-04 10:34:02'),(407,'ToXGRC5J',2,0,1,4,'2015-06-04 23:23:30'),(408,'WOpE7Hre',1,91,0,4,'2015-06-04 23:29:06'),(409,'LJcChWvB',1,91,3,4,'2015-06-04 23:29:45'),(410,'qEtWayhB',0,91,1,4,'2015-06-04 23:32:11'),(411,'hQX4ORBr',0,83,0,21,'2015-06-05 00:26:41'),(412,'HmtBPYsu',0,83,0,21,'2015-06-05 00:27:58'),(413,'BcOEjtqS',0,83,0,21,'2015-06-05 00:28:08'),(414,'8mGCpdI5',1,92,0,21,'2015-06-05 00:31:15'),(415,'ro5yCSQk',0,92,0,21,'2015-06-05 00:31:57'),(416,'NBuOnqtG',1,93,0,21,'2015-06-05 00:40:09'),(417,'IBNpQa8f',0,93,0,21,'2015-06-05 00:41:04'),(418,'xWwKrlyq',0,88,0,11,'2015-06-05 00:45:09'),(419,'IZb9c2JQ',0,93,0,21,'2015-06-05 00:48:30'),(420,'cbJxOEqr',1,94,0,21,'2015-06-05 00:56:43'),(421,'w5lcaU7A',0,94,0,21,'2015-06-05 00:57:45'),(422,'viOtF1r4',0,94,0,21,'2015-06-05 01:00:15'),(423,'uByVMZ05',0,94,0,21,'2015-06-05 01:07:56'),(424,'sJLNCGzO',1,95,0,21,'2015-06-05 01:15:56'),(425,'z6W2kXsG',0,95,0,21,'2015-06-05 01:16:59'),(426,'SXfJPIhO',0,95,0,21,'2015-06-05 01:17:13'),(427,'VpXj159O',0,95,0,21,'2015-06-05 01:18:32'),(428,'5SjwKq4x',1,96,0,21,'2015-06-05 01:20:10'),(429,'vgNZH9JA',1,96,0,21,'2015-06-05 01:20:20'),(430,'qT0W8VBG',0,96,0,21,'2015-06-05 01:21:20'),(431,'n0z37B4c',1,97,0,21,'2015-06-05 01:26:30'),(432,'iMcVdzkJ',0,97,0,21,'2015-06-05 01:27:13'),(433,'H2kdWhaN',0,97,0,21,'2015-06-05 01:29:38'),(434,'cX57TIRk',1,98,0,21,'2015-06-05 01:31:14'),(435,'Bq08Qkvs',0,98,0,21,'2015-06-05 01:32:07'),(436,'hWyiBbKr',1,99,0,21,'2015-06-05 01:38:15'),(437,'BTmLJdXU',0,99,0,21,'2015-06-05 01:39:11'),(438,'5EuqbTZn',1,100,0,21,'2015-06-05 01:41:15'),(439,'cbR6Uzwf',0,100,0,21,'2015-06-05 01:42:07'),(440,'rX1xPN4o',0,100,0,21,'2015-06-05 01:51:25'),(441,'cpSWD8Kn',0,100,0,21,'2015-06-05 01:51:41'),(442,'2roE84cT',1,101,0,21,'2015-06-05 01:54:06'),(443,'yuTzSVDA',0,101,0,21,'2015-06-05 01:54:47'),(444,'eKNtPumg',0,101,0,21,'2015-06-05 01:58:56'),(445,'dJHozGIV',1,102,3,21,'2015-06-05 02:01:39'),(446,'LXewrZ2H',0,102,1,21,'2015-06-05 02:02:16'),(447,'FPYBcu9t',1,103,0,11,'2015-06-05 04:25:54'),(448,'j1zDRHMB',1,103,0,11,'2015-06-05 04:29:18'),(449,'c6brwyen',1,104,0,11,'2015-06-05 04:29:29'),(450,'kGx8nvca',1,105,0,11,'2015-06-05 04:37:52'),(451,'xfnuNY8o',1,105,0,11,'2015-06-05 04:39:53'),(452,'GoO8apim',1,105,0,11,'2015-06-05 04:41:27'),(453,'nSOhKT8N',1,106,0,11,'2015-06-05 04:41:31'),(454,'vWKlr0LD',1,107,0,11,'2015-06-05 04:44:18'),(455,'ZBF0Nt5G',1,108,0,11,'2015-06-05 04:46:52'),(456,'D2mbieon',1,109,0,11,'2015-06-05 06:02:00'),(457,'rJe5bOmh',1,110,0,11,'2015-06-05 06:03:38'),(458,'0RqSQp9o',1,111,0,11,'2015-06-05 06:04:43'),(459,'v45xaPgz',1,112,0,11,'2015-06-05 06:12:51'),(460,'W1l0Znc8',1,113,0,11,'2015-06-05 06:18:12'),(461,'9kLGz1Qe',1,114,0,11,'2015-06-05 06:19:56'),(462,'1OxZ90lL',1,115,0,11,'2015-06-05 06:24:52'),(463,'ka4XOBDE',1,116,0,11,'2015-06-05 06:33:18'),(464,'xlC98KvR',1,117,0,11,'2015-06-05 06:37:36'),(465,'0z8ebkwC',1,118,0,11,'2015-06-05 06:47:01'),(466,'P7BaHfJL',1,119,0,11,'2015-06-05 07:42:48'),(467,'XEzku3IK',1,120,0,11,'2015-06-05 07:45:09'),(468,'irpfwPc4',1,121,0,11,'2015-06-05 07:55:48'),(469,'js1NQphW',0,121,0,11,'2015-06-05 07:56:17'),(470,'qjXMn52K',1,122,0,11,'2015-06-05 07:59:53'),(471,'HhSNgfGJ',0,122,0,11,'2015-06-05 08:00:34'),(472,'IRC9S2BQ',0,122,0,11,'2015-06-05 08:03:22'),(473,'9SiHB4hP',1,123,0,11,'2015-06-05 08:29:39'),(474,'jeZ9LFEQ',1,124,0,11,'2015-06-05 08:45:23'),(475,'2GNh3ZEU',2,0,0,11,'2015-06-05 08:53:59'),(476,'Uv2kK4pX',1,126,0,11,'2015-06-05 09:03:16'),(477,'QYRmurk7',0,126,0,11,'2015-06-05 09:03:51'),(478,'wL41UdVo',1,127,0,11,'2015-06-05 09:07:20'),(479,'AbokF9Qi',0,127,0,11,'2015-06-05 09:08:23'),(480,'A3a6XkBs',0,127,0,11,'2015-06-05 09:30:03'),(481,'u0SKBYV1',0,127,0,11,'2015-06-05 09:30:53'),(482,'SldUYvpA',0,127,0,11,'2015-06-05 09:32:31'),(483,'uLkWJjT8',0,127,0,11,'2015-06-05 09:33:28'),(484,'0l8UP5nJ',0,127,0,11,'2015-06-05 09:41:18'),(485,'F0fbXBd9',0,127,0,11,'2015-06-05 09:43:51'),(486,'CnJeFAy6',0,127,0,11,'2015-06-05 09:46:39'),(487,'TXYGaMfK',0,127,0,11,'2015-06-05 09:47:14'),(488,'gmcBIs7E',0,127,0,11,'2015-06-05 09:49:41'),(489,'6viNFrdD',1,128,0,11,'2015-06-05 10:16:54'),(490,'WC0r5EMk',0,128,0,11,'2015-06-05 10:17:34'),(491,'av1rQKJj',0,128,0,11,'2015-06-05 10:21:01'),(492,'FKCJyfVH',0,128,0,11,'2015-06-05 10:21:58'),(493,'RPqpIhWU',0,128,0,11,'2015-06-05 10:22:38'),(494,'ImJV6Hei',0,128,0,11,'2015-06-05 10:24:15'),(495,'19GxdWIL',0,128,0,11,'2015-06-05 10:26:11'),(496,'42o6pGUy',0,128,0,11,'2015-06-05 10:30:32'),(497,'3dltXcsn',0,128,0,11,'2015-06-05 10:35:28'),(498,'rmU5KAJh',0,128,0,11,'2015-06-05 10:39:10'),(499,'DmU1OgoB',0,128,0,11,'2015-06-05 10:43:08'),(500,'whHkXGdF',0,128,0,11,'2015-06-05 10:48:22'),(501,'gEOQha3s',0,128,0,11,'2015-06-05 10:56:53'),(502,'LYEuTjI8',0,128,0,11,'2015-06-05 10:57:31'),(503,'Ws1BiHT8',0,128,0,11,'2015-06-05 11:22:39'),(504,'BItxml4u',0,128,0,11,'2015-06-05 11:27:49'),(505,'daUSy8Zo',0,128,0,11,'2015-06-05 11:45:04'),(506,'ARDrbfFg',0,128,0,11,'2015-06-05 11:57:30'),(507,'qwhd59Km',0,128,0,11,'2015-06-05 12:26:34'),(508,'MU2FRgvb',0,128,0,11,'2015-06-05 12:35:13'),(509,'GItvUeT0',0,128,0,11,'2015-06-08 06:21:45'),(510,'nFBEfRwx',0,128,0,11,'2015-06-08 06:34:46'),(511,'OY7m4D9W',0,128,0,11,'2015-06-08 07:00:21'),(512,'A3fF1ykE',0,128,0,11,'2015-06-08 07:06:07'),(513,'U75nJu3O',0,128,0,11,'2015-06-08 07:14:27'),(514,'3tRADj68',0,128,0,11,'2015-06-08 07:19:14'),(515,'J7oBVdZs',0,128,0,11,'2015-06-08 07:32:22'),(516,'IPrnh3US',0,128,0,11,'2015-06-08 07:44:26'),(517,'VudsTKZP',0,128,0,11,'2015-06-08 07:45:39'),(518,'cL5yX2ho',0,128,0,11,'2015-06-08 07:50:17'),(519,'phPvcrXJ',0,128,0,11,'2015-06-08 07:50:57'),(520,'H3iwpzVX',0,128,0,11,'2015-06-08 07:51:27'),(521,'j9h2iXQZ',0,128,0,11,'2015-06-08 07:58:09'),(522,'IvnXeBiD',0,128,0,11,'2015-06-08 08:02:50'),(523,'itT3HIEO',0,128,0,11,'2015-06-08 08:15:40'),(524,'ECFaYkvR',0,128,0,11,'2015-06-08 08:22:08'),(525,'v0aD3OPy',0,128,0,11,'2015-06-08 08:23:50'),(526,'28znKyd5',0,128,0,11,'2015-06-08 08:26:48'),(527,'ls1JPhkD',0,128,0,11,'2015-06-08 08:34:30'),(528,'QxM2sRYv',0,128,0,11,'2015-06-08 08:40:50'),(529,'5x281di3',0,128,0,11,'2015-06-08 08:44:53'),(530,'0tNXBILk',0,128,0,11,'2015-06-08 08:51:51'),(531,'msGuDAYo',0,128,0,11,'2015-06-08 08:55:44'),(532,'Na3QG8f0',0,128,0,11,'2015-06-08 09:00:08'),(533,'IhlUvNo3',0,128,0,11,'2015-06-08 09:29:00'),(534,'Mu59sC6O',0,128,0,11,'2015-06-08 09:33:18'),(535,'ZFE8Pdfz',1,129,0,11,'2015-06-08 09:34:21'),(536,'ojHQO9tk',2,0,0,11,'2015-06-08 09:40:33'),(537,'f3VMbrOA',2,0,3,11,'2015-06-08 09:42:18'),(538,'WU5BToAd',1,131,0,11,'2015-06-08 09:43:15'),(539,'dF4Li3OG',0,131,0,11,'2015-06-08 09:43:40'),(540,'Dj0s1zTQ',0,131,0,11,'2015-06-08 09:47:59'),(541,'SOYuRf1t',0,131,0,11,'2015-06-08 09:48:55'),(542,'68uqiwBb',0,131,0,11,'2015-06-08 09:52:58'),(543,'MVHJNUQO',0,131,0,11,'2015-06-08 09:54:12'),(544,'mVqhs9LZ',1,132,0,11,'2015-06-08 09:57:02'),(545,'WRr8kNou',0,132,0,11,'2015-06-08 09:57:46'),(546,'VOjdWxsZ',1,133,0,11,'2015-06-08 10:10:37'),(547,'WNUJbPZ4',1,134,0,11,'2015-06-08 10:11:51'),(548,'EIXOn7SY',0,134,3,11,'2015-06-08 10:12:23'),(549,'k0K4gcWj',1,135,0,11,'2015-06-08 10:52:39'),(550,'zU6QF4Yb',1,136,0,23,'2015-06-10 21:07:23'),(551,'DuYXTpkl',1,137,1,23,'2015-06-10 22:27:46'),(552,'HDhvGrN2',1,138,0,11,'2015-06-11 01:24:46'),(553,'aSu3AT6b',1,138,0,11,'2015-06-11 03:23:09'),(554,'zL9fKqMA',1,139,0,11,'2015-06-11 05:50:06'),(555,'eLXkOC0u',1,140,0,11,'2015-06-11 06:39:03'),(556,'oUeDJCTy',1,141,0,11,'2015-06-11 06:45:08'),(557,'RI3x9ZQH',1,142,0,11,'2015-06-11 07:23:35'),(558,'KzZekAEP',1,143,0,11,'2015-06-11 07:30:52'),(559,'dZptw9mR',1,144,0,11,'2015-06-11 07:39:30'),(560,'hcGHb7Fu',1,145,0,11,'2015-06-11 07:45:10'),(561,'dmajbEtL',1,146,0,11,'2015-06-11 07:48:48'),(562,'fMqvNo1w',1,147,0,11,'2015-06-11 08:06:17'),(563,'LvytOE4Q',1,148,0,11,'2015-06-11 08:10:53'),(564,'hQAM7BC6',1,149,0,11,'2015-06-11 08:19:02'),(565,'q7jY615k',1,150,0,11,'2015-06-11 08:44:34'),(566,'ETcxBpe6',1,151,0,11,'2015-06-11 08:46:51'),(567,'zgf7dk8U',1,152,0,11,'2015-06-11 08:49:14'),(568,'8Yk6aJ5A',1,153,3,11,'2015-06-11 08:49:14');
/*!40000 ALTER TABLE `VerificationCodes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Websites`
--

DROP TABLE IF EXISTS `Websites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Websites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `owner` int(11) NOT NULL,
  `title` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `description` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `domains` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `categories` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `dateCreated` datetime NOT NULL,
  `dateModified` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Websites`
--

LOCK TABLES `Websites` WRITE;
/*!40000 ALTER TABLE `Websites` DISABLE KEYS */;
INSERT INTO `Websites` VALUES (1,4,'My Website','some description','[\"mywebsite.com\"]','[\"Autos\",\"Blogs\",\"Computers\",\"Dating\",\"Education\"]','0000-00-00 00:00:00','2014-08-24 19:53:10'),(2,4,'My Website 2','some description','[\"mywebsite2.com\"]','[\"Autos\",\"Blogs\",\"Computers\",\"Dating\",\"Education\"]','0000-00-00 00:00:00','2014-08-24 19:53:10'),(3,4,'My Website 3','some description','[\"mywebsite3.com\"]','[\"Autos\",\"Blogs\",\"Computers\",\"Dating\",\"Education\"]','0000-00-00 00:00:00','2014-08-24 19:53:10'),(4,4,'My Website 4','some description','[\"mywebsite4.com\"]','[\"Autos\",\"Blogs\",\"Computers\",\"Dating\",\"Education\"]','0000-00-00 00:00:00','2014-08-24 19:53:10'),(5,4,'My Website 5','Some description','[\"alexanderlomov.com\"]','[\"Autos\",\"Blogs\",\"Computers\",\"Dating\",\"Education\"]','2014-08-23 16:46:53','2014-08-24 19:53:10'),(7,4,'Some Website','','[\"biom.io\"]','[\"Autos\",\"Blogs\",\"Computers\",\"Dating\",\"Education\"]','2014-08-24 19:46:05','2014-08-24 19:53:10'),(8,4,'Google','this is google','[\"google.com\"]','[\"Autos\",\"Blogs\",\"Computers\",\"Dating\",\"Education\"]','2014-08-24 19:47:39','2014-08-24 19:53:10'),(9,4,'Google','this is google','[\"google.com\"]','[\"Autos\",\"Blogs\",\"Computers\",\"Dating\",\"Education\"]','2014-08-24 19:48:50','2014-08-24 19:53:10'),(10,4,'qwerty','qwerty','[\"qwerty.com\"]','[\"Autos\",\"Blogs\",\"Computers\",\"Dating\",\"Education\"]','2014-08-24 19:51:43','2014-08-24 19:51:43');
/*!40000 ALTER TABLE `Websites` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`biom`@`localhost`*/ /*!50003 TRIGGER websites_creation_time BEFORE INSERT ON Websites FOR EACH ROW 
BEGIN
    SET NEW.dateCreated = NOW();
    SET NEW.dateModified = NOW();
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`biom`@`localhost`*/ /*!50003 TRIGGER websites_modification_time BEFORE UPDATE ON Websites FOR EACH ROW 
BEGIN
    SET NEW.dateModified = NOW();
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `application_userinformation`
--

DROP TABLE IF EXISTS `application_userinformation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `application_userinformation` (
  `application` varchar(255) NOT NULL,
  `userinformation` int(11) NOT NULL,
  PRIMARY KEY (`application`,`userinformation`),
  KEY `idx_application_userinformation` (`userinformation`),
  CONSTRAINT `fk_application_userinformation__application` FOREIGN KEY (`application`) REFERENCES `Applications` (`app_id`),
  CONSTRAINT `fk_application_userinformation__userinformation` FOREIGN KEY (`userinformation`) REFERENCES `Profiles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `application_userinformation`
--

LOCK TABLES `application_userinformation` WRITE;
/*!40000 ALTER TABLE `application_userinformation` DISABLE KEYS */;
INSERT INTO `application_userinformation` VALUES ('0e7655e9b04b982df6addf330d4f7f63',11),('18b863486b7e6cec5016016ef46b0d25',11),('31ec8a12d92d79883b0b7b4a9ed479b5',11),('7439ef160abe4af57f0b2f567b13b242',11),('a5140a8cf0041aa5716df93916d6130d',11),('a6e91269f71014828f6e9da3755d598f',11),('aa3f5ec46a19943d04fe85416a8218c3',11),('afc99893dad27c10251f17f5e01a9aee',11),('b65de89efe88e83d25a964e54c26d830',11),('d4bee4618e35f2bf70beec8174bc3867',11),('d8e8fef022ea2bceacb3aed6c0e13e73',11),('3a9d3f79ecc2c42b9114b4300a248777',23),('88b960b1c9805fb586810f270def7378',23);
/*!40000 ALTER TABLE `application_userinformation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'biom_website'
--

--
-- Dumping routines for database 'biom_website'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-06-11 17:53:34

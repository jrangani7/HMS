-- MySQL dump 10.13  Distrib 8.0.20, for Win64 (x86_64)
--
-- Host: localhost    Database: tcs_hms
-- ------------------------------------------------------
-- Server version	8.0.20

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `diagnostic_tests`
--

DROP TABLE IF EXISTS `diagnostic_tests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `diagnostic_tests` (
  `tid` int NOT NULL AUTO_INCREMENT,
  `tname` varchar(45) NOT NULL,
  `charge` float NOT NULL DEFAULT '0',
  PRIMARY KEY (`tid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `diagnostic_tests`
--

LOCK TABLES `diagnostic_tests` WRITE;
/*!40000 ALTER TABLE `diagnostic_tests` DISABLE KEYS */;
INSERT INTO `diagnostic_tests` VALUES (1,'ECG',3000),(2,'CBP',2000),(3,'Lipid',1500),(4,'Echo',4000);
/*!40000 ALTER TABLE `diagnostic_tests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `diagnostic_tests_conducted`
--

DROP TABLE IF EXISTS `diagnostic_tests_conducted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `diagnostic_tests_conducted` (
  `pid` int NOT NULL,
  `tid` int NOT NULL,
  KEY `pid_idx` (`pid`),
  KEY `tid_idx` (`tid`),
  CONSTRAINT `pid_dt` FOREIGN KEY (`pid`) REFERENCES `patient` (`id`),
  CONSTRAINT `tid_dt` FOREIGN KEY (`tid`) REFERENCES `diagnostic_tests` (`tid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `diagnostic_tests_conducted`
--

LOCK TABLES `diagnostic_tests_conducted` WRITE;
/*!40000 ALTER TABLE `diagnostic_tests_conducted` DISABLE KEYS */;
INSERT INTO `diagnostic_tests_conducted` VALUES (2,1),(3,4);
/*!40000 ALTER TABLE `diagnostic_tests_conducted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `issued_medicines`
--

DROP TABLE IF EXISTS `issued_medicines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `issued_medicines` (
  `pid` int NOT NULL,
  `mid` int NOT NULL,
  `quantity_issued` int NOT NULL DEFAULT '0',
  KEY `pid_idx` (`pid`) /*!80000 INVISIBLE */,
  KEY `mid_idx` (`mid`),
  CONSTRAINT `mid` FOREIGN KEY (`mid`) REFERENCES `medicine_inventory` (`mid`),
  CONSTRAINT `pid` FOREIGN KEY (`pid`) REFERENCES `patient` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `issued_medicines`
--

LOCK TABLES `issued_medicines` WRITE;
/*!40000 ALTER TABLE `issued_medicines` DISABLE KEYS */;
INSERT INTO `issued_medicines` VALUES (2,1,3);
/*!40000 ALTER TABLE `issued_medicines` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medicine_inventory`
--

DROP TABLE IF EXISTS `medicine_inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medicine_inventory` (
  `mid` int NOT NULL AUTO_INCREMENT,
  `mname` varchar(45) NOT NULL,
  `quantity` int NOT NULL DEFAULT '0',
  `rate` float NOT NULL DEFAULT '0',
  PRIMARY KEY (`mid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicine_inventory`
--

LOCK TABLES `medicine_inventory` WRITE;
/*!40000 ALTER TABLE `medicine_inventory` DISABLE KEYS */;
INSERT INTO `medicine_inventory` VALUES (1,'Acebutolol',20,55),(2,'Corgard',5,2000),(3,'Tenormin',36,100);
/*!40000 ALTER TABLE `medicine_inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient`
--

DROP TABLE IF EXISTS `patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient` (
  `uid` varchar(12) NOT NULL DEFAULT '0',
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `age` int NOT NULL,
  `doadmission` date NOT NULL,
  `bedtype` varchar(20) NOT NULL,
  `address` varchar(50) NOT NULL,
  `city` varchar(20) NOT NULL,
  `state` varchar(20) NOT NULL,
  `status` varchar(10) NOT NULL DEFAULT 'Active',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient`
--

LOCK TABLES `patient` WRITE;
/*!40000 ALTER TABLE `patient` DISABLE KEYS */;
INSERT INTO `patient` VALUES ('123',2,'Jishnu',22,'2020-06-29','General','shivane','pune','Maharashtra','Active'),('456',3,'Rudra',18,'2020-06-26','Semi Sharing','Bibewadi','Pune','Maharashtra','Active'),('789',4,'nikhil',45,'2020-05-27','Single','marketyard','pune','maharashtra','Discharged');
/*!40000 ALTER TABLE `patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userstore`
--

DROP TABLE IF EXISTS `userstore`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userstore` (
  `loginid` varchar(10) NOT NULL,
  `password` varchar(10) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`loginid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userstore`
--

LOCK TABLES `userstore` WRITE;
/*!40000 ALTER TABLE `userstore` DISABLE KEYS */;
INSERT INTO `userstore` VALUES ('AD123','123AD','2020-06-28 13:09:36'),('DS098','098DS','2020-06-28 13:09:36'),('PH321','321PH','2020-06-28 13:09:36');
/*!40000 ALTER TABLE `userstore` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-06-29 23:51:34

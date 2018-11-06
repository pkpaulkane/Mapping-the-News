-- MySQL dump 10.13  Distrib 8.0.12, for macos10.13 (x86_64)
--
-- Host: localhost    Database: Mapping
-- ------------------------------------------------------
-- Server version	8.0.12

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Coordinates`
--

DROP TABLE IF EXISTS `Coordinates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `Coordinates` (
  `Counter` varchar(45) NOT NULL,
  `Place` varchar(45) NOT NULL,
  `Longitude` varchar(45) DEFAULT NULL,
  `Latitude` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Counter`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Coordinates`
--

LOCK TABLES `Coordinates` WRITE;
/*!40000 ALTER TABLE `Coordinates` DISABLE KEYS */;
INSERT INTO `Coordinates` VALUES ('1','New Zealand','-41.5000831','172.8344077'),('10','Russia','64.6863136','97.7453061'),('11','Vermont','44.5990718','-72.5002608'),('12','Paris','48.8566101','2.3514992'),('13','America','4.81804785','-75.6888617199333'),('14','Florida','27.7567667','-81.4639835'),('15','South Africa','-28.8166236','24.991639'),('16','Montana','47.3752671','-109.6387579'),('17','India','22.3511148','78.6677428'),('18','England','52.7954791','-0.540240286617432'),('19','Liverpool','53.4054719','-2.9805392'),('2','Australia','-24.7761086','134.755'),('20','Middlesbrough','54.5760419','-1.2344047'),('21','China','35.000074','104.999927'),('22','Brazil','-10.3333333','-53.2'),('23','Spain','39.3262345','-4.8380649'),('24','London','51.5073219','-0.1276474'),('25','Germany','51.0834196','10.4234469'),('26','Berlin','52.5170365','13.3888599'),('27','France','46.603354','1.8883335'),('28','Lithuania','55.3500003','23.7499997'),('29','Scotland','56.7861112','-4.1140518'),('3','US','39.7837304','-100.4458825'),('30','Netherlands','52.2379891','5.53460738161551'),('31','Palestine','31.649741','35.162072'),('32','Israel','30.8760272','35.0015196'),('33','Jerusalem','31.778345','35.2250786'),('34','North Dakota','47.6201461','-100.540737'),('35','Missouri','38.7604815','-92.5617875'),('36','Egypt','26.2540493','29.2675469'),('37','Turkey','38.9597594','34.9249653'),('38','Syria','34.6401861','39.0494106'),('39','Lebanon','33.8750629','35.843409'),('4','UK','54.7023545','-3.2765753'),('40','Iraq','33.0955793','44.1749775'),('41','Tunisia','33.8439408','9.400138'),('42','Kuwait','29.2733964','47.4979476'),('43','Saudi Arabia','25.6242618','42.3528328'),('44','Pakistan','30.3308401','71.247499'),('45','Riyadh','24.6319692','46.7150648'),('46','Amman','31.9515694','35.9239625'),('47','Belgium','50.6402809','4.6667145'),('48','Ankara','39.9215219','32.8537929'),('49','Greece','38.9953683','21.9877132'),('5','Moscow','55.7504461','37.6174943'),('50','Wales','52.2928116','-3.73893'),('51','Northern Ireland','54.6294982','-6.7654416'),('52','Brussels','50.8465573','4.351697'),('53','Arizona','34.395342','-111.7632755'),('54','Tbilisi','41.6934591','44.8014495'),('55','Georgia','41.6809707','44.0287382'),('56','South Carolina','33.6874388','-80.4363743'),('57','Jordan','31.1667049','36.941628'),('58','Athens','33.9597677','-83.376398'),('59','Kenya','1.4419683','38.4313975'),('6','Washington','38.8950712','-77.0362758'),('60','Sudan','14.5844444','29.4917691'),('61','Afghanistan','33.7680065','66.2385139'),('62','Watford','51.6553875','-0.3957425'),('63','Hull','53.7435722','-0.3394758'),('64','Telford','52.6780419','-2.4514273'),('7','San Francisco','37.7792808','-122.4192363'),('8','New York','40.7308619','-73.9871558'),('9','Maryland','39.5162234','-76.9382069');
/*!40000 ALTER TABLE `Coordinates` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-11-06 15:51:27

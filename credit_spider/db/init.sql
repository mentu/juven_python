-- MySQL dump 10.13  Distrib 5.5.31, for Linux (x86_64)
--
-- Host: localhost    Database: credit
-- ------------------------------------------------------
-- Server version       5.5.31-log

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
-- Table structure for table `rh_balancetypesum`
--

DROP TABLE IF EXISTS `rh_balancetypesum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rh_balancetypesum` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `midsigncode` varchar(128) DEFAULT NULL,
  `typename` varchar(128) DEFAULT NULL,
  `rmb` varchar(128) DEFAULT NULL,
  `dollars` varchar(128) DEFAULT NULL,
  `searchdate` varchar(128) DEFAULT NULL,
  `dollarstormb` varchar(128) DEFAULT NULL,
  `uploadtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `borrowername` varchar(128) DEFAULT NULL,
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rh_bdbguaranteecontractinfo`
--

DROP TABLE IF EXISTS `rh_bdbguaranteecontractinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rh_bdbguaranteecontractinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `midsigncode` varchar(128) DEFAULT NULL,
  `guaranteeamount` varchar(128) DEFAULT NULL,
  `guaranteecode` varchar(128) DEFAULT NULL,
  `institutionname` varchar(128) DEFAULT NULL,
  `currencytype` varchar(128) DEFAULT NULL,
  `guaranteestate` varchar(128) DEFAULT NULL,
  `signdate` varchar(128) DEFAULT NULL,
  `guaranteemothed` varchar(128) DEFAULT NULL,
  `searchdate` varchar(128) DEFAULT NULL,
  `uploadtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rh_billdiscount`
--

DROP TABLE IF EXISTS `rh_billdiscount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rh_billdiscount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `billcode` varchar(128) DEFAULT NULL,
  `midsigncode` varchar(128) DEFAULT NULL,
  `tickettype` varchar(128) DEFAULT NULL,
  `institutionname` varchar(128) DEFAULT NULL,
  `institutioncode` varchar(128) DEFAULT NULL,
  `applicant` varchar(128) DEFAULT NULL,
  `applicantmidsigncode` varchar(128) DEFAULT NULL,
  `bankname` varchar(128) DEFAULT NULL,
  `bankcode` varchar(128) DEFAULT NULL,
  `currencytype` varchar(128) DEFAULT NULL,
  `discountdate` varchar(128) DEFAULT NULL,
  `acceptancedate` varchar(128) DEFAULT NULL,
  `parvalue` varchar(128) DEFAULT NULL,
  `billstate` varchar(128) DEFAULT NULL,
  `fivegrade` varchar(128) DEFAULT NULL,
  `fourgrade` varchar(128) DEFAULT NULL,
  `searchdate` varchar(128) DEFAULT NULL,
  `discountamount` varchar(128) DEFAULT NULL,
  `uploadtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rh_creditagreeement`
--

DROP TABLE IF EXISTS `rh_creditagreeement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rh_creditagreeement` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `midsigncode` varchar(128) DEFAULT NULL,
  `creditagreementnumber` varchar(128) DEFAULT NULL,
  `creditagreementfrom` varchar(128) DEFAULT NULL,
  `creditagreementto` varchar(128) DEFAULT NULL,
  `currencytype` varchar(128) DEFAULT NULL,
  `creditagreementmoney` varchar(128) DEFAULT NULL,
  `institutionname` varchar(128) DEFAULT NULL,
  `institutioncode` varchar(128) DEFAULT NULL,
  `creditagreementoutdate` varchar(128) DEFAULT NULL,
  `creditagreementoutinfo` varchar(128) DEFAULT NULL,
  `searchdate` varchar(128) DEFAULT NULL,
  `uploadtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `borrowername` varchar(128) DEFAULT NULL,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rh_creditbalance`
--

DROP TABLE IF EXISTS `rh_creditbalance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rh_creditbalance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creditcode` varchar(128) DEFAULT NULL,
  `midsigncode` varchar(128) DEFAULT NULL,
  `institutionname` varchar(128) DEFAULT NULL,
  `institutioncode` varchar(128) DEFAULT NULL,
  `borrowername` varchar(128) DEFAULT NULL,
  `currencytype` varchar(128) DEFAULT NULL,
  `issuingblance` varchar(128) DEFAULT NULL,
  `issuingdate` varchar(128) DEFAULT NULL,
  `marginratio` varchar(128) DEFAULT NULL,
  `payperiod` varchar(128) DEFAULT NULL,
  `creditvalidperiod` varchar(128) DEFAULT NULL,
  `creditreptdate` varchar(128) DEFAULT NULL,
  `creditcardblance` varchar(128) DEFAULT NULL,
  `fivegrade` varchar(128) DEFAULT NULL,
  `guaranteetag` varchar(128) DEFAULT NULL,
  `creditstate` varchar(128) DEFAULT NULL,
  `creditperiod` varchar(128) DEFAULT NULL,
  `advident` varchar(128) DEFAULT NULL,
  `searchdate` varchar(128) DEFAULT NULL,
  `creditoutdate` varchar(128) DEFAULT NULL,
  `uploadtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rh_dbguaranteecontract`
--

DROP TABLE IF EXISTS `rh_dbguaranteecontract`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rh_dbguaranteecontract` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `midsigncode` varchar(128) DEFAULT NULL,
  `guaranteeamount` varchar(128) DEFAULT NULL,
  `guaranteecode` varchar(128) DEFAULT NULL,
  `institutionname` varchar(128) DEFAULT NULL,
  `currencytype` varchar(128) DEFAULT NULL,
  `guaranteestate` varchar(128) DEFAULT NULL,
  `signdate` varchar(128) DEFAULT NULL,
  `guaranteemothed` varchar(128) DEFAULT NULL,
  `searchdate` varchar(128) DEFAULT NULL,
  `uploadtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `gmoneytype` varchar(128) DEFAULT NULL,
  `guaranteemoney` varchar(128) DEFAULT NULL,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rh_dbmortinfo`
--

DROP TABLE IF EXISTS `rh_dbmortinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rh_dbmortinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `midsigncode` varchar(128) DEFAULT NULL,
  `mortamount` varchar(128) DEFAULT NULL,
  `mortcode` varchar(128) DEFAULT NULL,
  `institutionname` varchar(128) DEFAULT NULL,
  `currencytype` varchar(128) DEFAULT NULL,
  `mortstate` varchar(128) DEFAULT NULL,
  `signdate` varchar(128) DEFAULT NULL,
  `searchdate` varchar(128) DEFAULT NULL,
  `guaranteeamount` varchar(128) DEFAULT NULL,
  `guacurrencytype` varchar(128) DEFAULT NULL,
  `uploadtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rh_dbpledgecontract`
--

DROP TABLE IF EXISTS `rh_dbpledgecontract`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rh_dbpledgecontract` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pledgecode` varchar(128) DEFAULT NULL,
  `pledgebalance` varchar(128) DEFAULT NULL,
  `institutionname` varchar(128) DEFAULT NULL,
  `pledgestate` varchar(128) DEFAULT NULL,
  `signdate` varchar(128) DEFAULT NULL,
  `midsigncode` varchar(128) DEFAULT NULL,
  `searchdate` varchar(128) DEFAULT NULL,
  `currencytype` varchar(128) DEFAULT NULL,
  `guaranteeamount` varchar(128) DEFAULT NULL,
  `guacurrencytype` varchar(128) DEFAULT NULL,
  `uploadtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rh_draft`
--

DROP TABLE IF EXISTS `rh_draft`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rh_draft` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `midsigncode` varchar(128) DEFAULT NULL,
  `draftagreementcode` varchar(128) DEFAULT NULL,
  `draftcode` varchar(128) DEFAULT NULL,
  `draftdate` varchar(128) DEFAULT NULL,
  `draftenddate` varchar(128) DEFAULT NULL,
  `draftaccount` varchar(128) DEFAULT NULL,
  `currencytype` varchar(128) DEFAULT NULL,
  `institutionname` varchar(128) DEFAULT NULL,
  `fivegrade` varchar(128) DEFAULT NULL,
  `institutioncode` varchar(128) DEFAULT NULL,
  `drawername` varchar(128) DEFAULT NULL,
  `signtime` varchar(128) DEFAULT NULL,
  `marginratio` varchar(128) DEFAULT NULL,
  `guaranteesign` varchar(128) DEFAULT NULL,
  `draftstate` varchar(128) DEFAULT NULL,
  `advancesign` varchar(128) DEFAULT NULL,
  `searchdate` varchar(128) DEFAULT NULL,
  `uploadtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rh_extensioninfo`
--

DROP TABLE IF EXISTS `rh_extensioninfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rh_extensioninfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `midsigncode` varchar(128) DEFAULT NULL,
  `ioucode` varchar(128) DEFAULT NULL,
  `financecode` varchar(128) DEFAULT NULL,
  `extensionnumber` varchar(128) DEFAULT NULL,
  `extensionfrom` varchar(128) DEFAULT NULL,
  `extensionto` varchar(128) DEFAULT NULL,
  `extensionmoney` varchar(128) DEFAULT NULL,
  `searchdate` varchar(128) DEFAULT NULL,
  `uploadtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `repayamount` varchar(128) DEFAULT NULL,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rh_factoringinfo`
--

DROP TABLE IF EXISTS `rh_factoringinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rh_factoringinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `factoringcode` varchar(128) DEFAULT NULL,
  `midsigncode` varchar(128) DEFAULT NULL,
  `institutionname` varchar(128) DEFAULT NULL,
  `institutioncode` varchar(128) DEFAULT NULL,
  `factoringtype` varchar(128) DEFAULT NULL,
  `factoringstyle` varchar(128) DEFAULT NULL,
  `borrowername` varchar(128) DEFAULT NULL,
  `currencytype` varchar(128) DEFAULT NULL,
  `syamount` varchar(128) DEFAULT NULL,
  `sydate` varchar(128) DEFAULT NULL,
  `syblance` varchar(128) DEFAULT NULL,
  `blancedate` varchar(128) DEFAULT NULL,
  `guaranteesign` varchar(128) DEFAULT NULL,
  `fivegrade` varchar(128) DEFAULT NULL,
  `fourgrade` varchar(128) DEFAULT NULL,
  `advancesign` varchar(128) DEFAULT NULL,
  `searchdate` datetime DEFAULT NULL,
  `uploadtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rh_fagreementinfo`
--

DROP TABLE IF EXISTS `rh_fagreementinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rh_fagreementinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `financecode` varchar(128) DEFAULT NULL,
  `midsigncode` varchar(128) DEFAULT NULL,
  `institutionname` varchar(128) DEFAULT NULL,
  `institutioncode` varchar(128) DEFAULT NULL,
  `borrowername` varchar(128) DEFAULT NULL,
  `currencytype` varchar(128) DEFAULT NULL,
  `financeaccount` varchar(128) DEFAULT NULL,
  `balancecurrencytype` varchar(128) DEFAULT NULL,
  `financeblance` varchar(128) DEFAULT NULL,
  `starttime` varchar(128) DEFAULT NULL,
  `endtime` varchar(128) DEFAULT NULL,
  `guaranteesign` varchar(128) DEFAULT NULL,
  `effectivestate` varchar(128) DEFAULT NULL,
  `searchdate` varchar(128) DEFAULT NULL,
  `financeingbalance` varchar(128) DEFAULT NULL,
  `uploadtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rh_fagreementinfo_list`
--

DROP TABLE IF EXISTS `rh_fagreementinfo_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rh_fagreementinfo_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `financecode` varchar(128) DEFAULT NULL,
  `midsigncode` varchar(128) DEFAULT NULL,
  `starttime` varchar(128) DEFAULT NULL,
  `endtime` varchar(128) DEFAULT NULL,
  `currencytype` varchar(128) DEFAULT NULL,
  `financeblance` varchar(128) DEFAULT NULL,
  `institutionname` varchar(128) DEFAULT NULL,
  `effectivestate` varchar(128) DEFAULT NULL,
  `searchdate` varchar(128) DEFAULT NULL,
  `uploadtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rh_financebusiness`
--

DROP TABLE IF EXISTS `rh_financebusiness`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rh_financebusiness` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `financecode` varchar(128) DEFAULT NULL,
  `midsigncode` varchar(128) DEFAULT NULL,
  `financetype` varchar(128) DEFAULT NULL,
  `currencytype` varchar(128) DEFAULT NULL,
  `financeaccount` varchar(128) DEFAULT NULL,
  `financeblance` varchar(128) DEFAULT NULL,
  `starttime` varchar(128) DEFAULT NULL,
  `endtime` varchar(128) DEFAULT NULL,
  `identification` varchar(128) DEFAULT NULL,
  `fivegrade` varchar(128) DEFAULT NULL,
  `fourgrade` varchar(128) DEFAULT NULL,
  `searchdate` varchar(128) DEFAULT NULL,
  `uploadtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rh_financebusiness_list`
--

DROP TABLE IF EXISTS `rh_financebusiness_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rh_financebusiness_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `financecode` varchar(128) DEFAULT NULL,
  `midsigncode` varchar(128) DEFAULT NULL,
  `financetype` varchar(128) DEFAULT NULL,
  `currencytype` varchar(128) DEFAULT NULL,
  `financeaccount` varchar(128) DEFAULT NULL,
  `financeblance` varchar(128) DEFAULT NULL,
  `starttime` varchar(128) DEFAULT NULL,
  `endtime` varchar(128) DEFAULT NULL,
  `identification` varchar(128) DEFAULT NULL,
  `fivegrade` varchar(128) DEFAULT NULL,
  `fourgrade` varchar(128) DEFAULT NULL,
  `searchdate` varchar(128) DEFAULT NULL,
  `uploadtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `businessdate` varchar(128) DEFAULT NULL,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rh_guaranteecontractinfo`
--

DROP TABLE IF EXISTS `rh_guaranteecontractinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rh_guaranteecontractinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `midsigncode` varchar(128) DEFAULT NULL,
  `contractencoding` varchar(128) DEFAULT NULL,
  `contractvalidstate` varchar(128) DEFAULT NULL,
  `contractamount` varchar(128) DEFAULT NULL,
  `currencytype` varchar(128) DEFAULT NULL,
  `signingdate` varchar(128) DEFAULT NULL,
  `guaranteeform` varchar(128) DEFAULT NULL,
  `contractnumber` varchar(128) DEFAULT NULL,
  `institutionname` varchar(128) DEFAULT NULL,
  `comefrom` varchar(128) DEFAULT NULL,
  `guaranteeamount` varchar(128) DEFAULT NULL,
  `searchdate` varchar(128) DEFAULT NULL,
  `uploadtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rh_guaranteeha`
--

DROP TABLE IF EXISTS `rh_guaranteeha`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rh_guaranteeha` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `guaranteecode` varchar(128) DEFAULT NULL,
  `institutionname` varchar(128) DEFAULT NULL,
  `institutioncode` varchar(128) DEFAULT NULL,
  `borrowername` varchar(128) DEFAULT NULL,
  `midsigncode` varchar(128) DEFAULT NULL,
  `guaranteetype` varchar(128) DEFAULT NULL,
  `guaranteestate` varchar(128) DEFAULT NULL,
  `currencytype` varchar(128) DEFAULT NULL,
  `guaranteeaccount` varchar(128) DEFAULT NULL,
  `starttime` varchar(128) DEFAULT NULL,
  `endtime` varchar(128) DEFAULT NULL,
  `marginratio` varchar(128) DEFAULT NULL,
  `blancedate` varchar(128) DEFAULT NULL,
  `guaranteebalance` varchar(128) DEFAULT NULL,
  `guaranteesign` varchar(128) DEFAULT NULL,
  `fivegrade` varchar(128) DEFAULT NULL,
  `advancesign` varchar(128) DEFAULT NULL,
  `uploadtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `searchdate` varchar(128) DEFAULT NULL,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rh_interestinfo`
--

DROP TABLE IF EXISTS `rh_interestinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rh_interestinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `midsigncode` varchar(128) DEFAULT NULL,
  `interesttype` varchar(128) DEFAULT NULL,
  `interestdate` varchar(128) DEFAULT NULL,
  `institutionname` varchar(128) DEFAULT NULL,
  `institutioncode` varchar(128) DEFAULT NULL,
  `borrowername` varchar(128) DEFAULT NULL,
  `currencytype` varchar(128) DEFAULT NULL,
  `interestblance` varchar(128) DEFAULT NULL,
  `interestchangedate` varchar(128) DEFAULT NULL,
  `searchdate` varchar(128) DEFAULT NULL,
  `uploadtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rh_iouinfo`
--

DROP TABLE IF EXISTS `rh_iouinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rh_iouinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ioucode` varchar(128) DEFAULT NULL,
  `midsigncode` varchar(128) DEFAULT NULL,
  `currencytype` varchar(128) DEFAULT NULL,
  `iocamount` varchar(128) DEFAULT NULL,
  `balance` varchar(128) DEFAULT NULL,
  `loandate` varchar(128) DEFAULT NULL,
  `expirationdate` varchar(128) DEFAULT NULL,
  `gradename` varchar(128) DEFAULT NULL,
  `businessdate` varchar(128) DEFAULT NULL,
  `searchdate` varchar(128) DEFAULT NULL,
  `loanform` varchar(128) DEFAULT NULL,
  `loancharacter` varchar(128) DEFAULT NULL,
  `loanorientation` varchar(128) DEFAULT NULL,
  `loantype` varchar(128) DEFAULT NULL,
  `fourgrade` varchar(128) DEFAULT NULL,
  `showtag` varchar(128) DEFAULT NULL,
  `contractnumber` varchar(128) DEFAULT NULL,
  `uploadtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rh_iouinfo_list`
--

DROP TABLE IF EXISTS `rh_iouinfo_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rh_iouinfo_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ioucode` varchar(128) DEFAULT NULL,
  `midsigncode` varchar(128) DEFAULT NULL,
  `currencytype` varchar(128) DEFAULT NULL,
  `iocamount` varchar(128) DEFAULT NULL,
  `balance` varchar(128) DEFAULT NULL,
  `loandate` varchar(128) DEFAULT NULL,
  `expirationdate` varchar(128) DEFAULT NULL,
  `gradename` varchar(128) DEFAULT NULL,
  `businessdate` varchar(128) DEFAULT NULL,
  `searchdate` varchar(128) DEFAULT NULL,
  `contractnumber` varchar(128) DEFAULT NULL,
  `uploadtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rh_loaninfo`
--

DROP TABLE IF EXISTS `rh_loaninfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rh_loaninfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `contractnumber` varchar(64) DEFAULT NULL,
  `institutioncode` varchar(64) DEFAULT NULL,
  `financialinstitution` varchar(64) DEFAULT NULL,
  `borrowername` varchar(64) DEFAULT NULL,
  `midsigncode` varchar(64) DEFAULT NULL,
  `creditagreementnumber` varchar(64) DEFAULT NULL,
  `currencytype` varchar(64) DEFAULT NULL,
  `loanbalance` varchar(64) DEFAULT NULL,
  `availablebalance` varchar(64) DEFAULT NULL,
  `startdate` varchar(64) DEFAULT NULL,
  `enddate` varchar(64) DEFAULT NULL,
  `syndicatedlogo` varchar(64) DEFAULT NULL,
  `guaranteetag` varchar(64) DEFAULT NULL,
  `loanstate` varchar(64) DEFAULT NULL,
  `uploadtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `searchdate` varchar(15) DEFAULT NULL,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rh_loaninfo_list`
--

DROP TABLE IF EXISTS `rh_loaninfo_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rh_loaninfo_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `midsigncode` varchar(128) DEFAULT NULL,
  `contractnumber` varchar(128) DEFAULT NULL,
  `startdate` varchar(128) DEFAULT NULL,
  `enddate` varchar(128) DEFAULT NULL,
  `currencytype` varchar(128) DEFAULT NULL,
  `availablebalance` varchar(128) DEFAULT NULL,
  `financialinstitution` varchar(128) DEFAULT NULL,
  `loanstate` varchar(128) DEFAULT NULL,
  `uploadtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `searchdate` varchar(15) DEFAULT NULL,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rh_martpad`
--

DROP TABLE IF EXISTS `rh_martpad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rh_martpad` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `padcode` varchar(128) DEFAULT NULL,
  `oldcode` varchar(128) DEFAULT NULL,
  `institutionname` varchar(128) DEFAULT NULL,
  `institutioncode` varchar(128) DEFAULT NULL,
  `borrowername` varchar(128) DEFAULT NULL,
  `midsigncode` varchar(128) DEFAULT NULL,
  `padtype` varchar(128) DEFAULT NULL,
  `paddate` varchar(128) DEFAULT NULL,
  `padbalance` varchar(128) DEFAULT NULL,
  `padamount` varchar(128) DEFAULT NULL,
  `padchangedate` varchar(128) DEFAULT NULL,
  `fivegrade` varchar(128) DEFAULT NULL,
  `fourgrade` varchar(128) DEFAULT NULL,
  `rebackmethod` varchar(128) DEFAULT NULL,
  `searchdate` varchar(128) DEFAULT NULL,
  `currencytype` varchar(128) DEFAULT NULL,
  `uploadtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rh_repaymentinfo`
--

DROP TABLE IF EXISTS `rh_repaymentinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rh_repaymentinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `midsigncode` varchar(128) DEFAULT NULL,
  `ioucode` varchar(128) DEFAULT NULL,
  `repaynumber` varchar(128) DEFAULT NULL,
  `repaydate` varchar(128) DEFAULT NULL,
  `repaymethod` varchar(128) DEFAULT NULL,
  `searchdate` varchar(128) DEFAULT NULL,
  `uploadtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `repayamount` varchar(128) DEFAULT NULL,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rh_securedmort`
--

DROP TABLE IF EXISTS `rh_securedmort`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rh_securedmort` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `midsigncode` varchar(128) DEFAULT NULL,
  `securedmortcode` varchar(128) DEFAULT NULL,
  `securedmortblance` varchar(128) DEFAULT NULL,
  `institutionname` varchar(128) DEFAULT NULL,
  `securedstate` varchar(128) DEFAULT NULL,
  `signdate` varchar(128) DEFAULT NULL,
  `searchdate` varchar(128) DEFAULT NULL,
  `uploadtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `currencytype` varchar(128) DEFAULT NULL,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rh_specialloaninfo`
--

DROP TABLE IF EXISTS `rh_specialloaninfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rh_specialloaninfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `midsigncode` varchar(128) DEFAULT NULL,
  `contractnumber` varchar(128) DEFAULT NULL,
  `institutioncode` varchar(128) DEFAULT NULL,
  `financialinstitution` varchar(128) DEFAULT NULL,
  `specialloanname` varchar(128) DEFAULT NULL,
  `currencytype` varchar(128) DEFAULT NULL,
  `specialloanbalance` varchar(128) DEFAULT NULL,
  `availablebalance` varchar(128) DEFAULT NULL,
  `startdate` varchar(128) DEFAULT NULL,
  `enddate` varchar(128) DEFAULT NULL,
  `loanstate` varchar(128) DEFAULT NULL,
  `guaranteetag` varchar(128) DEFAULT NULL,
  `searchdate` varchar(128) DEFAULT NULL,
  `uploadtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-09-06 14:11:50
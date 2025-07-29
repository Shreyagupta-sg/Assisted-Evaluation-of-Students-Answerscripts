-- phpMyAdmin SQL Dump
-- version 3.2.4
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 04, 2023 at 04:52 PM
-- Server version: 5.1.41
-- PHP Version: 5.3.1

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `subjectiveanalysis`
--
CREATE DATABASE `subjectiveanalysis` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `subjectiveanalysis`;

-- --------------------------------------------------------

--
-- Table structure for table `answerdetails`
--

CREATE TABLE IF NOT EXISTS `answerdetails` (
  `AnswerId` int(11) NOT NULL AUTO_INCREMENT,
  `Answer` varchar(250) NOT NULL,
  `Category` int(11) NOT NULL,
  `QuestionId` int(11) NOT NULL,
  `Recorded_Date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`AnswerId`),
  KEY `QuestionId` (`QuestionId`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=25 ;

--
-- Dumping data for table `answerdetails`
--

INSERT INTO `answerdetails` (`AnswerId`, `Answer`, `Category`, `QuestionId`, `Recorded_Date`) VALUES
(1, ' Inertia', 0, 1, '2023-05-03 23:57:11'),
(2, 'state of rest', 0, 1, '2023-05-05 14:24:05' ),
(3, 'uniform motion', 0, 1, '2023-05-05 14:24:05'),
(4, 'straight line', 0, 1, '2023-05-05 14:24:05'),
(5, 'Polymorphism', 0, 2, '2023-05-03 23:57:11'),
(6, 'ability', 0, 2, '2023-05-05 14:09:08'),
(7, 'object', 0, 2, '2023-05-05 14:24:05'),
(8, 'different', 0, 2, '2023-05-05 14:24:05'),
(9, 'forms', 0, 2,'2023-05-05 14:24:05'),
(10, 'Inheritance', 0, 3, '2023-05-03 23:57:11'),
(11, 'acquires', 0, 3, '2023-05-05 14:05:23'),
(12, 'one class', 0, 3, '2023-05-05 14:24:05'),
(13, 'other class', 0, 3,'2023-05-05 14:24:05'),
(14, 'Encapsulation', 0, 4, '2023-05-04 23:57:11'),
(15, 'bundling', 0, 4, '2023-05-05 13:59:05'),
(16, 'fields and methods', 0, 4,'2023-05-05 14:24:05' ),
(17, 'single class', 0, 4,'2023-05-05 14:24:05'),
(18, 'Data Abstraction', 0, 5, '2023-05-04 23:57:11'),
(19, 'hiding', 0, 5,'2023-05-05 14:24:05'),
(20, 'certain details', 0, 5,'2023-05-05 14:24:05'),
(21, 'showing', 0, 5,'2023-05-05 14:24:05'),
(22, 'essential', 0, 5,'2023-05-05 14:24:05'),
(23, 'information', 0, 5,'2023-05-05 14:24:05'),
(24, 'object', 0, 6, '2023-05-04 23:57:11'),
(25, 'entity', 0, 6,'2023-05-05 14:24:05'),
(26, 'state', 0, 6,'2023-05-05 14:24:05'),
(27, 'behaviour', 0, 6,'2023-05-05 14:24:05');



-- --------------------------------------------------------

--
-- Table structure for table `historydetails`
--

CREATE TABLE IF NOT EXISTS `historydetails` (
  `HistoryId` int(11) NOT NULL AUTO_INCREMENT,
  `PersonId` int(11) NOT NULL,
  `Question1Id` varchar(250) NOT NULL,
  `Question2Id` varchar(250) NOT NULL,
  `Question3Id` varchar(250) NOT NULL,
  `Question4Id` varchar(250) NOT NULL,
  `Question5Id` varchar(250) NOT NULL,
  `Question6Id` varchar(250) NOT NULL,
  `Result` varchar(250) NOT NULL,
  `Percentage` varchar(250) NOT NULL,
  `Recorded_Date` date NOT NULL,
  PRIMARY KEY (`HistoryId`),
  KEY `PersonId` (`PersonId`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=28 ;

--
-- Dumping data for table `historydetails`
--

INSERT INTO `historydetails` (`HistoryId`, `PersonId`, `Question1Id`, `Question2Id`, `Question3Id`, `Question4Id`, `Question5Id`, `Question6Id`, `Result`, `Percentage`, `Recorded_Date`) VALUES
(27, 6, 'Spelling mistake (I am a graduat.)', 'Grammatical problem: agreement error (The pronoun â€˜isâ€™ must be used with â€œareâ€.)', '80', '80', '80', '80', '', '', '2023-05-04');

-- --------------------------------------------------------

--
-- Table structure for table `personaldetails`
--

CREATE TABLE IF NOT EXISTS `personaldetails` (
  `PersonId` int(11) NOT NULL AUTO_INCREMENT,
  `Firstname` varchar(250) NOT NULL,
  `Lastname` varchar(250) NOT NULL,
  `Phoneno` bigint(250) NOT NULL,
  `DOB` date NOT NULL,
  `Age` int(11) NOT NULL,
  `Emailid` varchar(250) NOT NULL,
  `Address` varchar(250) NOT NULL,
  `Username` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL,
  `Recorded_Date` date NOT NULL,
  PRIMARY KEY (`PersonId`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=8 ;

--
-- Dumping data for table `personaldetails`
--

INSERT INTO `personaldetails` (`PersonId`, `Firstname`, `Lastname`, `Phoneno`, `DOB`, `Age`, `Emailid`, `Address`, `Username`, `Password`, `Recorded_Date`) VALUES
(6, 'kiruba', 's', 9043963074, '2023-04-30', 40, 'kirubakarans2009@gmail.com', 'No:10,Chinna Ponnu Nagar,\r\nS.N.Chavady, Cuddalore-607002.', 'kiruba', 'kiruba', '2021-04-26'),
(7, 'hari', 's', 9043963074, '2023-04-25', 34, 'kirubakarans2009@gmail.com', 'dsfdsaasd', 'hari', 'hari', '2023-04-27'),
(8, 'Shivangi', 'J', 9897876543, '2000-04-09', 23, 'sss@gmail.com', 'Don Bosco institute of technology', 'Shivangi', 'shivangi', '2023-04-10');

-- --------------------------------------------------------

--
-- Table structure for table `questiondetails`
--

CREATE TABLE IF NOT EXISTS `questiondetails` (
  `QuestionId` int(11) NOT NULL AUTO_INCREMENT,
  `Question` text NOT NULL,
  `Recorded_Date` date NOT NULL,
  PRIMARY KEY (`QuestionId`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=7 ;

--
-- Dumping data for table `questiondetails`
--

INSERT INTO `questiondetails` (`QuestionId`, `Question`, `Recorded_Date`) VALUES
(1, 'Define inertia.?', '2023-03-12'),
(2, 'What is polymorphism in java?', '2023-03-12'),
(3, 'What is inheritance in java?', '2023-03-12'),
(4, 'what is encapsulation in java?', '2023-03-12'),
(5, 'What is data abstraction in java?', '2023-03-12'),
(6, 'What is object in java?', '2023-03-12');

-- --------------------------------------------------------

--
-- Table structure for table `useranswerdetails`
--

CREATE TABLE IF NOT EXISTS `useranswerdetails` (
  `UserAnswerId` int(11) NOT NULL AUTO_INCREMENT,
  `PersonId` int(11) NOT NULL,
  `QuestionId` int(11) NOT NULL,
  `Answer` text NOT NULL,
  `Recorded_Date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`UserAnswerId`),
  KEY `QuestionId` (`QuestionId`),
  KEY `PersonId` (`PersonId`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=396 ;

--
-- Dumping data for table `useranswerdetails`
--

INSERT INTO `useranswerdetails` (`UserAnswerId`, `PersonId`, `QuestionId`, `Answer`, `Recorded_Date`) VALUES
(390, 6, 1, 'I am a graduat. I want to learn Python. I like learning Python. Python is easy. Python is interesting. Learning increases thinking. Everyone should invest time in learning', '2023-05-04 15:51:58'),
(391, 6, 2, 'How is you?', '2023-05-04 15:51:59'),
(392, 6, 3, 'I am a graduate. I want to learn Python. I like learning Python. Python is easy. Python is interesting. Learning increases thinking. Everyone should invest time in learning', '2023-05-04 15:52:03'),
(393, 6, 4, 'I am a graduate. I want to learn Python. I like learning Python. Python is easy. Python is interesting. Learning increases thinking. Everyone should invest time in learning', '2023-05-04 15:52:04'),
(394, 6, 5, 'I am a graduate. I want to learn Python. I like learning Python. Python is easy. Python is interesting. Learning increases thinking. Everyone should invest time in learning', '2023-05-04 15:52:07'),
(395, 6, 6, 'I am a graduate. I want to learn Python. I like learning Python. Python is easy. Python is interesting. Learning increases thinking. Everyone should invest time in learning', '2023-05-04 15:52:08');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `historydetails`
--
ALTER TABLE `historydetails`
  ADD CONSTRAINT `historydetails_ibfk_1` FOREIGN KEY (`PersonId`) REFERENCES `personaldetails` (`PersonId`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `useranswerdetails`
--
ALTER TABLE `useranswerdetails`
  ADD CONSTRAINT `useranswerdetails_ibfk_1` FOREIGN KEY (`PersonId`) REFERENCES `personaldetails` (`PersonId`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `useranswerdetails_ibfk_2` FOREIGN KEY (`QuestionId`) REFERENCES `questiondetails` (`QuestionId`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

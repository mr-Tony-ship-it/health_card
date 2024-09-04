-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Sep 04, 2024 at 10:11 AM
-- Server version: 8.3.0
-- PHP Version: 8.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `vitasync`
--

-- --------------------------------------------------------

--
-- Table structure for table `d_reg`
--

DROP TABLE IF EXISTS `d_reg`;
CREATE TABLE IF NOT EXISTS `d_reg` (
  `d_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `office_location` varchar(100) DEFAULT NULL,
  `specialty` varchar(50) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`d_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
CREATE TABLE IF NOT EXISTS `login` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` int NOT NULL,
  `pass` int NOT NULL,
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`id`, `username`, `pass`, `date`) VALUES
(1, 0, 123, '2024-09-04 15:34:51');

-- --------------------------------------------------------

--
-- Table structure for table `medhistory`
--

DROP TABLE IF EXISTS `medhistory`;
CREATE TABLE IF NOT EXISTS `medhistory` (
  `id` int NOT NULL AUTO_INCREMENT,
  `blood_type` varchar(3) DEFAULT NULL,
  `allergies` text,
  `current_medication` text,
  `surgery_history` text,
  `emergency_contact` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `patientinsurance`
--

DROP TABLE IF EXISTS `patientinsurance`;
CREATE TABLE IF NOT EXISTS `patientinsurance` (
  `insurance_id` int NOT NULL AUTO_INCREMENT,
  `p_id` int NOT NULL,
  `provider` varchar(100) DEFAULT NULL,
  `policy_number` varchar(50) DEFAULT NULL,
  `coverage_type` enum('Full','Partial') DEFAULT NULL,
  `valid_from` date DEFAULT NULL,
  `valid_until` date DEFAULT NULL,
  PRIMARY KEY (`insurance_id`),
  KEY `p_id` (`p_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `p_reg`
--

DROP TABLE IF EXISTS `p_reg`;
CREATE TABLE IF NOT EXISTS `p_reg` (
  `p_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `gen` varchar(10) NOT NULL,
  `dob` date NOT NULL,
  `password` varchar(255) NOT NULL,
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`p_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `register`
--

DROP TABLE IF EXISTS `register`;
CREATE TABLE IF NOT EXISTS `register` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `gen` varchar(10) NOT NULL,
  `email` varchar(40) NOT NULL,
  `dob` date NOT NULL,
  `phno` int NOT NULL,
  `pass` int NOT NULL,
  `img` varchar(3000) NOT NULL,
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `register`
--

INSERT INTO `register` (`id`, `name`, `gen`, `email`, `dob`, `phno`, `pass`, `img`, `date`) VALUES
(1, 'rhrhr', '', 'joyaljose674@gmail.com', '0000-00-00', 2147483647, 123, '', '2024-09-04 15:17:09'),
(2, 'rgerg', '', 'joyaljose674@gmail.com', '0000-00-00', 12434646, 1234, '', '2024-09-04 15:20:00'),
(3, 'kevin', '', 'joyaljose674@gmail.com', '0000-00-00', 2147483647, 123, '', '2024-09-04 15:22:49'),
(4, 'efwef', '', 'joyaljose674@gmail.com', '2024-01-01', 2147483647, 123, '', '2024-09-04 15:24:20'),
(5, 'albin', 'male', 'joyaljose674@gmail.com', '2024-09-03', 2147483647, 12345, '', '2024-09-04 15:28:16');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

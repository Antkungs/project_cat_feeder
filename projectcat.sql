-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 24, 2024 at 11:42 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `projectcat`
--

-- --------------------------------------------------------

--
-- Table structure for table `catinformation`
--

CREATE TABLE `catinformation` (
  `id_cat` int(11) NOT NULL,
  `name_cat` varchar(255) DEFAULT NULL,
  `food_give` int(11) DEFAULT NULL,
  `id_tank` int(11) DEFAULT NULL,
  `time1_start` time DEFAULT NULL,
  `time1_end` time DEFAULT NULL,
  `time2_start` time DEFAULT NULL,
  `time2_end` time DEFAULT NULL,
  `time3_start` time DEFAULT NULL,
  `time3_end` time DEFAULT NULL,
  `time1_status` tinyint(1) DEFAULT NULL,
  `time2_status` tinyint(1) DEFAULT NULL,
  `time3_status` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `catinformation`
--

INSERT INTO `catinformation` (`id_cat`, `name_cat`, `food_give`, `id_tank`, `time1_start`, `time1_end`, `time2_start`, `time2_end`, `time3_start`, `time3_end`, `time1_status`, `time2_status`, `time3_status`) VALUES
(1, 'Whiskers', 10, 1, '08:00:00', '08:30:00', '12:00:00', '12:30:00', '18:00:00', '23:30:00', 0, 0, 1),
(2, 'cat2', 111, 1, '00:33:00', '01:33:00', '02:33:00', '03:33:00', '04:33:00', '05:33:00', 0, 0, 1);

-- --------------------------------------------------------

--
-- Table structure for table `eatinformation`
--

CREATE TABLE `eatinformation` (
  `ID_Cat` int(11) DEFAULT NULL,
  `Food_give` int(11) DEFAULT NULL,
  `Food_eat` int(11) DEFAULT NULL,
  `Food_remaining` int(11) DEFAULT NULL,
  `CurrentTime` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `eatinformation`
--

INSERT INTO `eatinformation` (`ID_Cat`, `Food_give`, `Food_eat`, `Food_remaining`, `CurrentTime`) VALUES
(1, 100, 20, 80, '2024-06-28 12:00:00'),
(2, 2, 2, 0, '2024-06-28 13:30:00'),
(2, 100, 80, 20, '2024-07-10 13:30:00'),
(2, 100, 80, 20, '2024-07-10 16:30:00'),
(2, 100, 80, 20, '2024-07-10 05:30:00'),
(2, 100, 80, 20, '2024-07-09 13:30:00'),
(2, 100, 80, 20, '2024-07-08 13:30:00');

-- --------------------------------------------------------

--
-- Table structure for table `notification`
--

CREATE TABLE `notification` (
  `token` varchar(255) NOT NULL,
  `hour` int(2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notification`
--

INSERT INTO `notification` (`token`, `hour`) VALUES
('j5Vy1V07apBG2tuWIuJ4S5aolnhM7VhBRla7ZdDnYgh', 1);

-- --------------------------------------------------------

--
-- Table structure for table `tank`
--

CREATE TABLE `tank` (
  `id_tank` int(11) NOT NULL,
  `name_tank` varchar(255) NOT NULL,
  `notification_percen` int(3) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tank`
--

INSERT INTO `tank` (`id_tank`, `name_tank`, `notification_percen`) VALUES
(1, 'tank1', 20),
(2, 'tank2', 2);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `catinformation`
--
ALTER TABLE `catinformation`
  ADD PRIMARY KEY (`id_cat`),
  ADD KEY `id_tank` (`id_tank`);

--
-- Indexes for table `tank`
--
ALTER TABLE `tank`
  ADD PRIMARY KEY (`id_tank`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `catinformation`
--
ALTER TABLE `catinformation`
  MODIFY `id_cat` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `catinformation`
--
ALTER TABLE `catinformation`
  ADD CONSTRAINT `catinformation_ibfk_1` FOREIGN KEY (`id_tank`) REFERENCES `tank` (`id_tank`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

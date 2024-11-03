-- phpMyAdmin SQL Dump
-- version 5.2.1deb3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Nov 03, 2024 at 01:33 PM
-- Server version: 8.0.39-0ubuntu0.24.04.2
-- PHP Version: 8.3.6

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
  `id_cat` int NOT NULL,
  `name_cat` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `food_give` int DEFAULT NULL,
  `id_tank` int DEFAULT NULL,
  `time1_start` time DEFAULT NULL,
  `time1_end` time DEFAULT NULL,
  `time2_start` time DEFAULT NULL,
  `time2_end` time DEFAULT NULL,
  `time3_start` time DEFAULT NULL,
  `time3_end` time DEFAULT NULL,
  `time1_status` tinyint(1) DEFAULT NULL,
  `time2_status` tinyint(1) DEFAULT NULL,
  `time3_status` tinyint(1) DEFAULT NULL,
  `image_url` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `catinformation`
--

INSERT INTO `catinformation` (`id_cat`, `name_cat`, `food_give`, `id_tank`, `time1_start`, `time1_end`, `time2_start`, `time2_end`, `time3_start`, `time3_end`, `time1_status`, `time2_status`, `time3_status`, `image_url`) VALUES
(1, 'เห็ดหอม', 50, 1, '12:00:00', '15:27:00', '12:19:00', '14:20:00', '20:21:00', '23:58:00', 0, 0, 0, NULL),
(2, 'cat2', 50, 2, '12:15:00', '13:40:00', '20:21:00', '20:25:00', '18:26:00', '23:30:00', 0, 1, 1, '/home/antkung/Desktop/project_cat_feeder/code/static/images/cat2.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `cat_detection`
--

CREATE TABLE `cat_detection` (
  `id` int NOT NULL,
  `detected_at` datetime NOT NULL,
  `idcatfound` int NOT NULL,
  `conf` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `cat_detection`
--

INSERT INTO `cat_detection` (`id`, `detected_at`, `idcatfound`, `conf`) VALUES
(1, '2024-11-03 20:32:24', 2, 0.970403),
(2, '2024-11-03 20:32:27', 2, 0.959656),
(3, '2024-11-03 20:32:45', 2, 0.955416);

-- --------------------------------------------------------

--
-- Table structure for table `eatinformation`
--

CREATE TABLE `eatinformation` (
  `ID_Cat` int DEFAULT NULL,
  `Food_give` int DEFAULT NULL,
  `Food_eat` int DEFAULT NULL,
  `Food_remaining` int DEFAULT NULL,
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
(2, 100, 80, 20, '2024-07-08 13:30:00'),
(1, 200, 122, 78, '2024-09-05 00:42:03'),
(2, 111, -11, 122, '2024-09-05 00:42:54'),
(1, 187, 86, 101, '2024-09-18 14:54:09'),
(1, 110, 50, 60, '2024-10-04 19:25:52'),
(1, 110, 50, 60, '2024-10-04 19:26:32'),
(2, 110, 50, 60, '2024-10-05 02:49:07'),
(2, 110, 50, 60, '2024-10-05 02:49:19'),
(1, 63, 12, 51, '2024-10-07 03:42:20'),
(1, 55, 10, 44, '2024-10-09 00:16:33'),
(1, 64, 0, 64, '2024-10-09 02:09:21'),
(1, 71, 71, 0, '2024-10-09 03:50:07'),
(1, 65, 17, 48, '2024-10-09 04:29:54'),
(1, 68, -2, 70, '2024-10-09 04:33:10'),
(1, 60, 37, 23, '2024-10-11 05:45:26'),
(1, 65, 33, 32, '2024-10-11 05:46:02'),
(2, 40, 17, 24, '2024-10-12 22:24:14'),
(2, 63, 0, 62, '2024-10-12 22:29:12'),
(2, 75, -1, 75, '2024-10-12 22:47:42'),
(2, 71, 14, 57, '2024-10-12 22:49:24'),
(2, 68, 11, 57, '2024-10-12 23:44:02'),
(1, 79, 8, 71, '2024-10-15 12:55:44'),
(1, 63, 6, 57, '2024-10-15 13:25:56'),
(2, 73, 73, 0, '2024-10-15 13:35:05'),
(2, 23, -1, 25, '2024-10-15 13:36:36'),
(1, 63, -1, 64, '2024-10-15 13:40:56'),
(1, 72, 72, 0, '2024-10-15 13:46:40'),
(2, 61, -1, 62, '2024-11-03 19:53:46'),
(2, 1, 0, 1, '2024-11-03 20:24:05');

-- --------------------------------------------------------

--
-- Table structure for table `notification`
--

CREATE TABLE `notification` (
  `token` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `hour` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notification`
--

INSERT INTO `notification` (`token`, `hour`) VALUES
('WvZuoFoZx8HVVJrT53KPxOYJNpFcNr9IWXbcvyvCJkr', 1);

-- --------------------------------------------------------

--
-- Table structure for table `tank`
--

CREATE TABLE `tank` (
  `id_tank` int NOT NULL,
  `name_tank` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `notification_percen` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tank`
--

INSERT INTO `tank` (`id_tank`, `name_tank`, `notification_percen`) VALUES
(1, 'tank1', 80),
(2, 'tank2', 10);

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
-- Indexes for table `cat_detection`
--
ALTER TABLE `cat_detection`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `idcatfound` (`idcatfound`,`detected_at`);

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
  MODIFY `id_cat` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `cat_detection`
--
ALTER TABLE `cat_detection`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `catinformation`
--
ALTER TABLE `catinformation`
  ADD CONSTRAINT `catinformation_ibfk_1` FOREIGN KEY (`id_tank`) REFERENCES `tank` (`id_tank`);

--
-- Constraints for table `cat_detection`
--
ALTER TABLE `cat_detection`
  ADD CONSTRAINT `cat_detection_ibfk_1` FOREIGN KEY (`idcatfound`) REFERENCES `catinformation` (`id_cat`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

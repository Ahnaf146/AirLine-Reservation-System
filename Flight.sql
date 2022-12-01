-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Nov 29, 2022 at 01:21 AM
-- Server version: 5.7.34
-- PHP Version: 7.4.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `Air Ticket Reservation System`
--

-- --------------------------------------------------------

--
-- Table structure for table `Flight`
--

CREATE TABLE `Flight` (
  `flight_number` int(255) NOT NULL,
  `Base_Price` int(255) DEFAULT NULL,
  `Departure_airport` varchar(255) DEFAULT NULL,
  `Departure_date` datetime DEFAULT NULL,
  `Departure_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `Arrival_airport` varchar(255) DEFAULT NULL,
  `Arrival_date` datetime DEFAULT NULL,
  `Arrival_time` time DEFAULT NULL,
  `Destination` varchar(255) DEFAULT NULL,
  `flight_status` varchar(255) DEFAULT NULL,
  `Airline_name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Flight`
--

INSERT INTO `Flight` (`flight_number`, `Base_Price`, `Departure_airport`, `Departure_date`, `Departure_time`, `Arrival_airport`, `Arrival_date`, `Arrival_time`, `Destination`, `flight_status`, `Airline_name`) VALUES
(12345, 1250, '\'JFK\'', '2022-11-06 01:52:43', '2022-11-17 02:52:43', '\'LHR\'', '2022-11-06 01:52:43', '15:39:43', '\'London\'', '\'on-time\'', 'Jet Blue'),
(67890, 1260, '\'JFK\'', '2022-11-06 01:55:14', '2022-11-27 02:55:14', '\'DAC\'', '2022-11-06 01:55:14', '19:55:14', '\'Bangladesh\'', '\'delayed\'', 'Jet Blue');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Flight`
--
ALTER TABLE `Flight`
  ADD PRIMARY KEY (`flight_number`),
  ADD KEY `Airline_name` (`Airline_name`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Flight`
--
ALTER TABLE `Flight`
  ADD CONSTRAINT `flight_ibfk_1` FOREIGN KEY (`Airline_name`) REFERENCES `Airline` (`airline_name`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

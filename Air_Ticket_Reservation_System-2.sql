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
-- Table structure for table `Airline`
--

CREATE TABLE `Airline` (
  `airline_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Airline`
--

INSERT INTO `Airline` (`airline_name`) VALUES
('Jet Blue');

-- --------------------------------------------------------

--
-- Table structure for table `AirlineStaff`
--

CREATE TABLE `AirlineStaff` (
  `Username` varchar(255) NOT NULL,
  `Password` varchar(255) DEFAULT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `Date_of_birth` varchar(255) DEFAULT NULL,
  `phone_number` int(255) DEFAULT NULL,
  `Airline_name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `AirlineStaff`
--

INSERT INTO `AirlineStaff` (`Username`, `Password`, `Name`, `Date_of_birth`, `phone_number`, `Airline_name`) VALUES
('\'DonT\'', '\'Vintage\'', '\'Tahmidur Rabb\'', '\'08/22/2000\'', 555350, 'Jet Blue');

-- --------------------------------------------------------

--
-- Table structure for table `Airplane`
--

CREATE TABLE `Airplane` (
  `Airplane_id` varchar(255) DEFAULT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `Manufacturing_company` varchar(255) DEFAULT NULL,
  `Num_of_seats` int(255) DEFAULT NULL,
  `Age` int(255) DEFAULT NULL,
  `Airline_name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Airplane`
--

INSERT INTO `Airplane` (`Airplane_id`, `Name`, `Manufacturing_company`, `Num_of_seats`, `Age`, `Airline_name`) VALUES
('020406', '\'Jet Blue\'', '\'Boeing\'', 1000, 55, 'Jet Blue'),
('010305', '\'Boeing749\'', '\'Boeing\'', 1500, 56, 'Jet Blue'),
('57 ', 'Boeing750', 'Boeing', 1450, 57, 'Jet Blue');

-- --------------------------------------------------------

--
-- Table structure for table `Airport`
--

CREATE TABLE `Airport` (
  `Name` varchar(255) NOT NULL,
  `City` varchar(255) DEFAULT NULL,
  `Country` varchar(255) DEFAULT NULL,
  `AirportType` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Airport`
--

INSERT INTO `Airport` (`Name`, `City`, `Country`, `AirportType`) VALUES
('JFK', 'NYC', 'US', 'International'),
('PVG', 'Shanghai', 'China', 'International');

-- --------------------------------------------------------

--
-- Table structure for table `Customer`
--

CREATE TABLE `Customer` (
  `email` varchar(255) NOT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `Password` varchar(255) DEFAULT NULL,
  `building_num` varchar(255) NOT NULL,
  `street` varchar(255) NOT NULL,
  `City` varchar(255) DEFAULT NULL,
  `State` varchar(255) DEFAULT NULL,
  `passport` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Customer`
--

INSERT INTO `Customer` (`email`, `Name`, `Password`, `building_num`, `street`, `City`, `State`, `passport`) VALUES
('ga1002@email.com', 'Gilbert Arenas', 'agent0', '60-13', '60st', 'Miami', 'Florida', '12468'),
('ra1001@email.com', 'Ray Allen', 'shuttleworth', '50-12', '54st', 'Brooklyn', 'NY', '13579'),
('sm1000@email.com', 'Stephon Marbury', 'starbury', '40-11', '50st', 'Queens', 'NY', '12345');

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

-- --------------------------------------------------------

--
-- Table structure for table `login_data`
--

CREATE TABLE `login_data` (
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `Ticket`
--

CREATE TABLE `Ticket` (
  `Ticket_id` int(255) NOT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `flight_number` int(255) DEFAULT NULL,
  `sold_price` int(255) DEFAULT NULL,
  `card_type` varchar(255) DEFAULT NULL,
  `card_number` int(255) DEFAULT NULL,
  `Name_on_card` varchar(255) DEFAULT NULL,
  `Expiration_date` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Ticket`
--

INSERT INTO `Ticket` (`Ticket_id`, `Email`, `flight_number`, `sold_price`, `card_type`, `card_number`, `Name_on_card`, `Expiration_date`) VALUES
(20406, 'ra1001@email.com', 67890, 1250, '\'Discover\'', 11111111, '\'Ray Allen\'', '\'12/25\''),
(30507, 'ga1002@email.com', 67890, 1260, '\'visa\'', 99999999, '\'Gilbert Arenas\'', '\'09/23\'');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Airline`
--
ALTER TABLE `Airline`
  ADD PRIMARY KEY (`airline_name`);

--
-- Indexes for table `AirlineStaff`
--
ALTER TABLE `AirlineStaff`
  ADD PRIMARY KEY (`Username`),
  ADD KEY `Airline_name` (`Airline_name`);

--
-- Indexes for table `Airplane`
--
ALTER TABLE `Airplane`
  ADD KEY `Airline_name` (`Airline_name`);

--
-- Indexes for table `Airport`
--
ALTER TABLE `Airport`
  ADD PRIMARY KEY (`Name`);

--
-- Indexes for table `Customer`
--
ALTER TABLE `Customer`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `Flight`
--
ALTER TABLE `Flight`
  ADD PRIMARY KEY (`flight_number`),
  ADD KEY `Airline_name` (`Airline_name`);

--
-- Indexes for table `Ticket`
--
ALTER TABLE `Ticket`
  ADD PRIMARY KEY (`Ticket_id`),
  ADD KEY `Email` (`Email`),
  ADD KEY `flight_number` (`flight_number`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `AirlineStaff`
--
ALTER TABLE `AirlineStaff`
  ADD CONSTRAINT `airlinestaff_ibfk_1` FOREIGN KEY (`Airline_name`) REFERENCES `Airline` (`airline_name`);

--
-- Constraints for table `Airplane`
--
ALTER TABLE `Airplane`
  ADD CONSTRAINT `airplane_ibfk_1` FOREIGN KEY (`Airline_name`) REFERENCES `Airline` (`airline_name`);

--
-- Constraints for table `Flight`
--
ALTER TABLE `Flight`
  ADD CONSTRAINT `flight_ibfk_1` FOREIGN KEY (`Airline_name`) REFERENCES `Airline` (`airline_name`);

--
-- Constraints for table `Ticket`
--
ALTER TABLE `Ticket`
  ADD CONSTRAINT `ticket_ibfk_1` FOREIGN KEY (`Email`) REFERENCES `Customer` (`email`),
  ADD CONSTRAINT `ticket_ibfk_2` FOREIGN KEY (`flight_number`) REFERENCES `Flight` (`flight_number`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

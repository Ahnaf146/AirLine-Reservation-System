-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 08, 2022 at 11:06 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `air ticket reservation system`
--

-- --------------------------------------------------------

--
-- Table structure for table `airline`
--

CREATE TABLE `airline` (
  `airline_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `airline`
--

INSERT INTO `airline` (`airline_name`) VALUES
('Jet Blue');

-- --------------------------------------------------------

--
-- Table structure for table `airlinestaff`
--

CREATE TABLE `airlinestaff` (
  `Username` varchar(255) NOT NULL,
  `Password` varchar(255) DEFAULT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `Date_of_birth` varchar(255) DEFAULT NULL,
  `phone_number` int(255) DEFAULT NULL,
  `Airline_name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `airlinestaff`
--

INSERT INTO `airlinestaff` (`Username`, `Password`, `Name`, `Date_of_birth`, `phone_number`, `Airline_name`) VALUES
('\'DonT\'', '\'Vintage\'', '\'Tahmidur Rabb\'', '\'08/22/2000\'', 555350, 'Jet Blue'),
('Majid778', '$2b$12$1/lXVI3NyIVjTiQSIbm.mewEeACHn7BtnIw1Wn3aGXMmRV8vgk2JW', 'Majid Mohamed Ibrahim', '04/07/2001', 558516520, 'Jet Blue'),
('pen', '$2b$12$iwwRhnwg0vkfRMtjK7w47uGgM6qzRmci0Rlo8OfwFHhFeHcLM90wW', 'elfbar', '08/22/2000', 21, 'Jet Blue'),
('tonysoprano', '$2b$12$5Vzj8kW7QfY.gr.vwsfNauZF1N.XV6eyLOPJ2X/MFxpo51jvRwXwO', 'Tony Soprano', '09/12/1961', 1234556788, 'Jet Blue');

-- --------------------------------------------------------

--
-- Table structure for table `airplane`
--

CREATE TABLE `airplane` (
  `Airplane_id` varchar(255) DEFAULT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `Manufacturing_company` varchar(255) DEFAULT NULL,
  `Num_of_seats` int(255) DEFAULT NULL,
  `Age` int(255) DEFAULT NULL,
  `Airline_name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `airplane`
--

INSERT INTO `airplane` (`Airplane_id`, `Name`, `Manufacturing_company`, `Num_of_seats`, `Age`, `Airline_name`) VALUES
('020406', '\'Jet Blue\'', '\'Boeing\'', 1000, 55, 'Jet Blue'),
('010305', '\'Boeing749\'', '\'Boeing\'', 1500, 56, 'Jet Blue'),
('57 ', 'Boeing750', 'Boeing', 1450, 57, 'Jet Blue');

-- --------------------------------------------------------

--
-- Table structure for table `airport`
--

CREATE TABLE `airport` (
  `Name` varchar(255) NOT NULL,
  `City` varchar(255) DEFAULT NULL,
  `Country` varchar(255) DEFAULT NULL,
  `AirportType` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `airport`
--

INSERT INTO `airport` (`Name`, `City`, `Country`, `AirportType`) VALUES
('JFK', 'NYC', 'US', 'International'),
('PVG', 'Shanghai', 'China', 'International');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `email` varchar(255) NOT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `Password` varchar(255) DEFAULT NULL,
  `building_num` varchar(255) NOT NULL,
  `street` varchar(255) NOT NULL,
  `City` varchar(255) DEFAULT NULL,
  `State` varchar(255) DEFAULT NULL,
  `passport` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`email`, `Name`, `Password`, `building_num`, `street`, `City`, `State`, `passport`) VALUES
('ga1002@email.com', 'Gilbert Arenas', 'agent0', '60-13', '60st', 'Miami', 'Florida', '12468'),
('google123@google.com', 'meta verse', '$2b$12$e1xgb1IVvfvTpk9.Uhum4e6TjeEeZmkbCGEM8eLxwxJd5I6uCsBiq', '1234567', '90st', 'Brooklyn', 'NY', '11368'),
('majidibrahim778@gmail.com', 'Majid Mohamed Ibrahim', '$2b$12$hEbuzqjz0YIM14j4120N6.CVDmDrU8l8pI8/IKOsQm2dYzAystciu', '80', 'LAf', 'Abu Dhabi', 'ny', '123123'),
('ra1001@email.com', 'Ray Allen', 'shuttleworth', '50-12', '54st', 'Brooklyn', 'NY', '13579'),
('sm1000@email.com', 'Stephon Marbury', 'starbury', '40-11', '50st', 'Queens', 'NY', '12345'),
('tr1476@nyu.edu', 'Tahmidur Rabb', '$2b$12$nsmuRoGevxAZ57wFQ6zMSetr5www.1Jp37tfAh9Tb0N2ahxTCpRx6', '60-13', '33-21 111st', 'Corona', 'NY', '670353');

-- --------------------------------------------------------

--
-- Table structure for table `customer_review`
--

CREATE TABLE `customer_review` (
  `flight_id` int(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `rating` int(255) NOT NULL,
  `review` text NOT NULL,
  `Airline` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `customer_review`
--

INSERT INTO `customer_review` (`flight_id`, `name`, `rating`, `review`, `Airline`) VALUES
(67890, 'Tahmidur Rabb', 5, 'awesome flight dude', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `flight`
--

CREATE TABLE `flight` (
  `flight_number` int(255) NOT NULL,
  `Base_Price` int(255) DEFAULT NULL,
  `Departure_airport` varchar(255) DEFAULT NULL,
  `Departure_date` date DEFAULT NULL,
  `Departure_time` time DEFAULT NULL,
  `Arrival_airport` varchar(255) DEFAULT NULL,
  `Arrival_date` date DEFAULT NULL,
  `Arrival_time` time DEFAULT NULL,
  `Destination` varchar(255) DEFAULT NULL,
  `flight_status` varchar(255) DEFAULT NULL,
  `Airline_name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `flight`
--

INSERT INTO `flight` (`flight_number`, `Base_Price`, `Departure_airport`, `Departure_date`, `Departure_time`, `Arrival_airport`, `Arrival_date`, `Arrival_time`, `Destination`, `flight_status`, `Airline_name`) VALUES
(12345, 1250, 'JFK', '2022-11-06', '19:17:20', 'LHR', '2022-11-06', '15:39:43', 'London', 'on-time', 'Jet Blue'),
(67890, 1260, 'JFK', '2022-11-06', '19:17:37', 'DAC', '2022-11-06', '19:55:14', 'Bangladesh', 'delayed', 'Jet Blue');

-- --------------------------------------------------------

--
-- Table structure for table `login_data`
--

CREATE TABLE `login_data` (
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `login_data`
--

INSERT INTO `login_data` (`username`, `password`) VALUES
('ga1002@email.com', 'agent0'),
('ga1002@email.com', 'agent0'),
('username', 'password'),
('tr1476@nyu.edu', 'tahmy'),
('tr1476@nyu.edu', 'emtech');

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

CREATE TABLE `ticket` (
  `Ticket_id` int(255) NOT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `flight_number` int(255) DEFAULT NULL,
  `sold_price` int(255) DEFAULT NULL,
  `card_type` varchar(255) DEFAULT NULL,
  `card_number` int(255) DEFAULT NULL,
  `Name_on_card` varchar(255) DEFAULT NULL,
  `Expiration_date` varchar(255) DEFAULT NULL,
  `purchase_date` date DEFAULT NULL,
  `Airline_name` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`Ticket_id`, `Email`, `flight_number`, `sold_price`, `card_type`, `card_number`, `Name_on_card`, `Expiration_date`, `purchase_date`, `Airline_name`) VALUES
(2355, 'majidibrahim778@gmail.com', 12345, 1250, 'Credit', 123, 'Majid', '123', '2022-11-20', 'Jet Blue'),
(3386, 'majidibrahim778@gmail.com', 67890, 1260, 'Credit', 123, 'Majid', '123', '2022-11-25', 'Jet Blue'),
(5097, 'majidibrahim778@gmail.com', 12345, 1250, 'Credit', 123, 'Majid Ibrahim', '123', '2022-10-10', 'Jet Blue'),
(9604, 'majidibrahim778@gmail.com', 12345, 1250, 'Credit', 123, '123', '123', '2022-12-08', 'Jet Blue'),
(20406, 'ra1001@email.com', 67890, 1250, '\'Discover\'', 11111111, '\'Ray Allen\'', '\'12/25\'', '2022-10-02', 'Jet Blue'),
(30507, 'ga1002@email.com', 67890, 1260, '\'visa\'', 99999999, '\'Gilbert Arenas\'', '\'09/23\'', '2021-12-15', 'Jet Blue');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `airline`
--
ALTER TABLE `airline`
  ADD PRIMARY KEY (`airline_name`);

--
-- Indexes for table `airlinestaff`
--
ALTER TABLE `airlinestaff`
  ADD PRIMARY KEY (`Username`),
  ADD KEY `Airline_name` (`Airline_name`);

--
-- Indexes for table `airplane`
--
ALTER TABLE `airplane`
  ADD KEY `Airline_name` (`Airline_name`);

--
-- Indexes for table `airport`
--
ALTER TABLE `airport`
  ADD PRIMARY KEY (`Name`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `flight`
--
ALTER TABLE `flight`
  ADD PRIMARY KEY (`flight_number`),
  ADD KEY `Airline_name` (`Airline_name`);

--
-- Indexes for table `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`Ticket_id`),
  ADD KEY `Email` (`Email`),
  ADD KEY `flight_number` (`flight_number`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `airlinestaff`
--
ALTER TABLE `airlinestaff`
  ADD CONSTRAINT `airlinestaff_ibfk_1` FOREIGN KEY (`Airline_name`) REFERENCES `airline` (`airline_name`);

--
-- Constraints for table `airplane`
--
ALTER TABLE `airplane`
  ADD CONSTRAINT `airplane_ibfk_1` FOREIGN KEY (`Airline_name`) REFERENCES `airline` (`airline_name`);

--
-- Constraints for table `flight`
--
ALTER TABLE `flight`
  ADD CONSTRAINT `flight_ibfk_1` FOREIGN KEY (`Airline_name`) REFERENCES `airline` (`airline_name`);

--
-- Constraints for table `ticket`
--
ALTER TABLE `ticket`
  ADD CONSTRAINT `ticket_ibfk_1` FOREIGN KEY (`Email`) REFERENCES `customer` (`email`),
  ADD CONSTRAINT `ticket_ibfk_2` FOREIGN KEY (`flight_number`) REFERENCES `flight` (`flight_number`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

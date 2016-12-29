-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: 29-Dez-2016 às 01:32
-- Versão do servidor: 5.6.17
-- PHP Version: 5.5.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `kutiva_2016`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `course`
--

CREATE TABLE IF NOT EXISTS `course` (
  `course_id` int(11) NOT NULL AUTO_INCREMENT,
  `course_name` varchar(50) NOT NULL,
  `course_category` varchar(20) NOT NULL,
  `course_description` text,
  `course_price` double(10,2) NOT NULL,
  `course_audience_level` varchar(20) NOT NULL,
  `course_tags` varchar(250) NOT NULL,
  `course_duration_time` time NOT NULL,
  `course_stars` int(5) NOT NULL,
  `course_status` varchar(10) NOT NULL DEFAULT 'Pending',
  `course_publishing_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`course_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=51 ;

--
-- Extraindo dados da tabela `course`
--

INSERT INTO `course` (`course_id`, `course_name`, `course_category`, `course_description`, `course_price`, `course_audience_level`, `course_tags`, `course_duration_time`, `course_stars`, `course_status`, `course_publishing_date`) VALUES
(1, '', 'Web Design', 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum', 499.00, 'beginner', 'web', '12:00:00', 5, 'Pending', '2016-12-05 01:28:48'),
(2, 'Basics of Android ', 'Programming', 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 599.00, '', '', '11:44:12', 1, 'Pending', '2016-12-05 01:56:37'),
(3, 'CSS3 Basics', 'Web Design', 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 450.00, '', '', '11:21:33', 5, 'Pending', '2016-12-05 14:12:30'),
(4, 'Up and Running with Flask', 'Programming', 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 799.00, '', '', '11:03:11', 5, 'Pending', '2016-12-05 14:12:30');

-- --------------------------------------------------------

--
-- Estrutura da tabela `course_image`
--

CREATE TABLE IF NOT EXISTS `course_image` (
  `course_image_id` int(11) NOT NULL AUTO_INCREMENT,
  `course_image_path` varchar(150) NOT NULL,
  `course_image_active` tinyint(1) NOT NULL DEFAULT '0',
  `course_image_upload_datetime` datetime DEFAULT CURRENT_TIMESTAMP,
  `course_image_course_id` int(11) NOT NULL,
  PRIMARY KEY (`course_image_id`),
  KEY `course_image_course_id` (`course_image_course_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=51 ;

--
-- Extraindo dados da tabela `course_image`
--

INSERT INTO `course_image` (`course_image_id`, `course_image_path`, `course_image_active`, `course_image_upload_datetime`, `course_image_course_id`) VALUES
(1, '../static/content/img/html.jpg', 0, '2016-12-05 01:50:30', 1),
(2, '../static/content/img/cover.png', 0, '2016-12-05 01:56:57', 2),
(3, '../static/content/img/css.jpg', 0, '2016-12-05 14:14:46', 3),
(4, '../static/content/img/flask.jpg', 0, '2016-12-05 14:14:46', 4);

-- --------------------------------------------------------

--
-- Estrutura da tabela `course_mentor`
--

CREATE TABLE IF NOT EXISTS `course_mentor` (
  `cm_id` int(11) NOT NULL AUTO_INCREMENT,
  `cm_course_id` int(11) NOT NULL,
  `cm_mentor_id` int(11) NOT NULL,
  PRIMARY KEY (`cm_id`),
  KEY `cm_course_id` (`cm_course_id`),
  KEY `cm_mentor_id` (`cm_mentor_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=47 ;

--
-- Extraindo dados da tabela `course_mentor`
--

INSERT INTO `course_mentor` (`cm_id`, `cm_course_id`, `cm_mentor_id`) VALUES
(1, 1, 1),
(3, 2, 2),
(4, 3, 2),
(5, 4, 1);

-- --------------------------------------------------------

--
-- Estrutura da tabela `email_verfication`
--

CREATE TABLE IF NOT EXISTS `email_verfication` (
  `email_verification_id` int(11) NOT NULL AUTO_INCREMENT,
  `email_verification_token` varchar(50) NOT NULL,
  `email_verification_active` tinyint(1) NOT NULL DEFAULT '1',
  `email_verification_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `email_verification_account_type` varchar(10) NOT NULL,
  `email_verification_account_id` int(11) NOT NULL,
  PRIMARY KEY (`email_verification_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=51 ;

--
-- Extraindo dados da tabela `email_verfication`
--

INSERT INTO `email_verfication` (`email_verification_id`, `email_verification_token`, `email_verification_active`, `email_verification_datetime`, `email_verification_account_type`, `email_verification_account_id`) VALUES
(31, 'd509827075a2b0c7451482c3483b10a', 1, '2016-12-10 12:34:02', 'Student', 77),
(32, '2cb9e0cf7194b39770d68d9dc67da1c2', 0, '2016-12-11 14:08:47', 'Student', 78),
(39, '1f1d4c891ef3f3a1eb3515ffd8a34d3a', 1, '2016-12-11 14:29:17', 'Student', 77),
(40, '2a86da40fafadacaee0876808a1cc5de', 1, '2016-12-11 14:31:12', 'Student', 77),
(41, '6fb50b4d50b1e913fddc2119ea689111', 0, '2016-12-11 14:37:59', 'Student', 77),
(42, '59b0db815d39dd6d106d81a7fcab09a6', 1, '2016-12-11 14:42:55', 'Student', 77),
(43, '727e6b0c889d2f3dbb8e8bd18275b29f', 0, '2016-12-11 14:48:31', 'Student', 79),
(44, 'a6fa128d701820a66e55276a61b77adf', 1, '2016-12-12 17:45:04', 'Mentor', 3),
(45, '0d1d5c809310424dbbb44a007975c4e0', 1, '2016-12-13 08:33:56', 'Student', 80),
(46, 'bc42edacc7e55d398ecaf9f0f553f0ca', 1, '2016-12-13 08:34:41', 'Student', 81),
(47, 'c35fed6b7bc5165c8fb91fdae754d637', 1, '2016-12-13 08:39:54', 'Student', 82),
(48, '8ccd8bdb302402dabfff3ce8d30d2d93', 0, '2016-12-13 08:41:25', 'Student', 83),
(49, 'e40420c2812bdd2bbc5b98778c4fcd80', 0, '2016-12-13 08:54:43', 'Student', 84),
(50, '9e643567e3e3ce66a14a7f80846d848a', 1, '2016-12-29 02:12:06', 'Student', 85);

-- --------------------------------------------------------

--
-- Estrutura da tabela `lesson`
--

CREATE TABLE IF NOT EXISTS `lesson` (
  `lesson_id` int(11) NOT NULL AUTO_INCREMENT,
  `lesson_title` varchar(50) NOT NULL,
  `lesson_location_path` varchar(150) NOT NULL,
  `lesson_length_time` time NOT NULL,
  `lesson_locked` tinyint(1) NOT NULL,
  `lesson_section_number` int(2) NOT NULL,
  `lesson_section_name` varchar(100) NOT NULL,
  `lesson_course_id` int(11) NOT NULL,
  PRIMARY KEY (`lesson_id`),
  KEY `lesson_course_id` (`lesson_course_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=14 ;

-- --------------------------------------------------------

--
-- Estrutura da tabela `mentor`
--

CREATE TABLE IF NOT EXISTS `mentor` (
  `mentor_id` int(11) NOT NULL AUTO_INCREMENT,
  `mentor_first_name` varchar(12) NOT NULL,
  `mentor_last_name` varchar(12) NOT NULL,
  `mentor_scope_category` varchar(20) NOT NULL,
  `mentor_email` varchar(50) NOT NULL,
  `mentor_country_code` int(3) NOT NULL,
  `mentor_phone` int(9) NOT NULL,
  `mentor_profile_image` varchar(250) DEFAULT NULL,
  `mentor_account_status` varchar(12) NOT NULL DEFAULT 'Not actived',
  `mentor_account_creation_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`mentor_id`),
  UNIQUE KEY `mentor_email` (`mentor_email`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Extraindo dados da tabela `mentor`
--

INSERT INTO `mentor` (`mentor_id`, `mentor_first_name`, `mentor_last_name`, `mentor_scope_category`, `mentor_email`, `mentor_country_code`, `mentor_phone`, `mentor_profile_image`, `mentor_account_status`, `mentor_account_creation_datetime`) VALUES
(1, 'Arnaldo', 'Govene', 'programming', 'arnaldo.govene@mfarj', 258, 841237444, '../static/content/img/arnaldo.jpg', 'Not actived', '2016-12-04 08:35:51'),
(2, 'José', 'Machava', 'android', 'jose.s.machava@gmail.com', 356, 564564, '../static/content/img/jose.jpg', 'Not actived', '2016-12-05 02:09:48'),
(3, 'TestName', 'TestSurname', 'TestCategory', 'Test@mail.com', 0, 0, '', 'Not actived', '2016-12-12 13:09:44');

-- --------------------------------------------------------

--
-- Estrutura da tabela `password`
--

CREATE TABLE IF NOT EXISTS `password` (
  `password_id` int(11) NOT NULL AUTO_INCREMENT,
  `password_encrypted` varchar(200) NOT NULL,
  `password_status` varchar(10) NOT NULL DEFAULT 'Actve',
  `password_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `password_owner_account_type` varchar(10) NOT NULL,
  `password_owner_account_id` int(11) NOT NULL,
  PRIMARY KEY (`password_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=87 ;

--
-- Extraindo dados da tabela `password`
--

INSERT INTO `password` (`password_id`, `password_encrypted`, `password_status`, `password_datetime`, `password_owner_account_type`, `password_owner_account_id`) VALUES
(77, '670b14728ad9902aecba32e22fa4f6bd', 'Actve', '2016-12-10 14:06:50', 'Student', 77),
(78, '670b14728ad9902aecba32e22fa4f6bd', 'Actve', '2016-12-10 14:08:47', 'Student', 78),
(79, '4096926abc98216c6d90b101a1ec3504', 'Actve', '2016-12-11 14:48:31', 'Student', 79),
(80, 'TestPassword', 'Actve', '2016-12-12 13:09:45', 'Mentor', 3),
(81, '0ef57fbe2db49d8956efc45b5a4d44d0', 'Actve', '2016-12-13 08:33:56', 'Student', 3),
(82, 'ea92692f716e7f8103a4b7b921ac90b9', 'Actve', '2016-12-13 08:34:41', 'Student', 81),
(83, '0ef57fbe2db49d8956efc45b5a4d44d0', 'Actve', '2016-12-13 08:39:54', 'Student', 82),
(84, '0ef57fbe2db49d8956efc45b5a4d44d0', 'Actve', '2016-12-13 08:41:25', 'Student', 83),
(85, '0ef57fbe2db49d8956efc45b5a4d44d0', 'Actve', '2016-12-13 08:54:43', 'Student', 84),
(86, '4096926abc98216c6d90b101a1ec3504', 'Actve', '2016-12-29 02:12:06', 'Student', 85);

-- --------------------------------------------------------

--
-- Estrutura da tabela `phone_verfication`
--

CREATE TABLE IF NOT EXISTS `phone_verfication` (
  `phone_verification_id` int(11) NOT NULL AUTO_INCREMENT,
  `phone_verification_token` varchar(50) NOT NULL,
  `phone_verification_active` tinyint(1) NOT NULL,
  `phone_verification_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `phone_verification_account_type` varchar(10) NOT NULL,
  `phone_verification_account_id` int(11) NOT NULL,
  PRIMARY KEY (`phone_verification_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estrutura da tabela `student`
--

CREATE TABLE IF NOT EXISTS `student` (
  `student_id` int(11) NOT NULL AUTO_INCREMENT,
  `student_first_name` varchar(12) NOT NULL,
  `student_last_name` varchar(12) NOT NULL,
  `student_gender` varchar(6) DEFAULT NULL,
  `student_birthdate` date DEFAULT NULL,
  `student_email` varchar(50) NOT NULL,
  `student_country_code` int(3) DEFAULT NULL,
  `student_phone` int(9) DEFAULT NULL,
  `student_profile_image` varchar(250) DEFAULT NULL,
  `student_account_status` varchar(12) NOT NULL DEFAULT 'Not actived',
  `student_account_creation_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`student_id`),
  UNIQUE KEY `student_email` (`student_email`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=86 ;

--
-- Extraindo dados da tabela `student`
--

INSERT INTO `student` (`student_id`, `student_first_name`, `student_last_name`, `student_gender`, `student_birthdate`, `student_email`, `student_country_code`, `student_phone`, `student_profile_image`, `student_account_status`, `student_account_creation_datetime`) VALUES
(85, 'arnaldo', 'Govene', NULL, NULL, 'arnaldo.govene12@gmail.com', NULL, NULL, NULL, 'Not actived', '2016-12-29 02:12:06');

-- --------------------------------------------------------

--
-- Estrutura da tabela `view`
--

CREATE TABLE IF NOT EXISTS `view` (
  `view_id` int(11) NOT NULL AUTO_INCREMENT,
  `view_location` varchar(20) NOT NULL,
  `view_user_agent` varchar(50) NOT NULL,
  `view_ip` varchar(20) NOT NULL,
  `view_device_type` varchar(50) NOT NULL,
  `view_datetime` datetime DEFAULT NULL,
  `view_course_id` int(11) NOT NULL,
  `view_account_type` varchar(10) DEFAULT NULL,
  `view_account_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`view_id`),
  KEY `view_course_id` (`view_course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Constraints for dumped tables
--

--
-- Limitadores para a tabela `course_image`
--
ALTER TABLE `course_image`
  ADD CONSTRAINT `course_image_ibfk_1` FOREIGN KEY (`course_image_course_id`) REFERENCES `course` (`course_id`);

--
-- Limitadores para a tabela `course_mentor`
--
ALTER TABLE `course_mentor`
  ADD CONSTRAINT `course_mentor_ibfk_1` FOREIGN KEY (`cm_course_id`) REFERENCES `course` (`course_id`),
  ADD CONSTRAINT `course_mentor_ibfk_2` FOREIGN KEY (`cm_mentor_id`) REFERENCES `mentor` (`mentor_id`);

--
-- Limitadores para a tabela `lesson`
--
ALTER TABLE `lesson`
  ADD CONSTRAINT `lesson_ibfk_1` FOREIGN KEY (`lesson_course_id`) REFERENCES `course` (`course_id`);

--
-- Limitadores para a tabela `view`
--
ALTER TABLE `view`
  ADD CONSTRAINT `view_ibfk_1` FOREIGN KEY (`view_course_id`) REFERENCES `course` (`course_id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

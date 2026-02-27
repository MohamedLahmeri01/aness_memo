-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Feb 27, 2026 at 10:49 AM
-- Server version: 9.1.0
-- PHP Version: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `freelance_arena_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts_user`
--

DROP TABLE IF EXISTS `accounts_user`;
CREATE TABLE IF NOT EXISTS `accounts_user` (
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `bio` longtext COLLATE utf8mb4_unicode_ci,
  `profile_picture` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `skills` longtext COLLATE utf8mb4_unicode_ci,
  `hourly_rate` decimal(10,2) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `last_seen` datetime(6) DEFAULT NULL,
  `email_verified` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `accounts_user`
--

INSERT INTO `accounts_user` (`password`, `last_login`, `is_superuser`, `id`, `email`, `username`, `first_name`, `last_name`, `role`, `bio`, `profile_picture`, `skills`, `hourly_rate`, `is_active`, `is_staff`, `date_joined`, `last_seen`, `email_verified`) VALUES
('pbkdf2_sha256$1000000$r7tysc6SptFpuT224OPTse$HrFWgkJoNeLtx0gUBoapv40nqtW/hlOOowiSNtso794=', NULL, 1, '083a0e03d1614f0cad9ae0442a865f9b', 'admin@freelancearena.com', 'admin', 'Admin', 'User', 'ADMIN', NULL, '', NULL, NULL, 1, 1, '2026-02-26 19:21:56.956087', NULL, 0),
('pbkdf2_sha256$1000000$YemCqGE7LGwWhs28NpxOsJ$cJslZmBwR7BiOqbp3U6+Li2mrgQsQ+sbUmClylC0kUA=', NULL, 0, '3204e1bc4c7d45418eced4357bd93691', 'freelancer@test.com', 'freelanceruser', 'Free', 'Lancer', 'FREELANCER', NULL, '', NULL, NULL, 1, 0, '2026-02-26 19:23:43.965276', NULL, 0),
('pbkdf2_sha256$1000000$MVwdft3mN8DKuX6nOSqzcK$V3mURRKiUlZ7ZtR3R7U/M6Vg9Z7slrc3M0+ObALGFTo=', NULL, 0, '8d6da5f3d71a4fab8b91ca7e04835c8f', 'client@test.com', 'clientuser', 'Client', 'User', 'CLIENT', NULL, '', NULL, NULL, 1, 0, '2026-02-26 19:23:43.321642', NULL, 0);

-- --------------------------------------------------------

--
-- Table structure for table `accounts_user_groups`
--

DROP TABLE IF EXISTS `accounts_user_groups`;
CREATE TABLE IF NOT EXISTS `accounts_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_groups_user_id_group_id_59c0b32f_uniq` (`user_id`,`group_id`),
  KEY `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `accounts_user_user_permissions`
--

DROP TABLE IF EXISTS `accounts_user_user_permissions`;
CREATE TABLE IF NOT EXISTS `accounts_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq` (`user_id`,`permission_id`),
  KEY `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add Blacklisted Token', 6, 'add_blacklistedtoken'),
(22, 'Can change Blacklisted Token', 6, 'change_blacklistedtoken'),
(23, 'Can delete Blacklisted Token', 6, 'delete_blacklistedtoken'),
(24, 'Can view Blacklisted Token', 6, 'view_blacklistedtoken'),
(25, 'Can add Outstanding Token', 7, 'add_outstandingtoken'),
(26, 'Can change Outstanding Token', 7, 'change_outstandingtoken'),
(27, 'Can delete Outstanding Token', 7, 'delete_outstandingtoken'),
(28, 'Can view Outstanding Token', 7, 'view_outstandingtoken'),
(29, 'Can add user', 8, 'add_user'),
(30, 'Can change user', 8, 'change_user'),
(31, 'Can delete user', 8, 'delete_user'),
(32, 'Can view user', 8, 'view_user'),
(33, 'Can add competition bookmark', 9, 'add_competitionbookmark'),
(34, 'Can change competition bookmark', 9, 'change_competitionbookmark'),
(35, 'Can delete competition bookmark', 9, 'delete_competitionbookmark'),
(36, 'Can view competition bookmark', 9, 'view_competitionbookmark'),
(37, 'Can add competition question', 10, 'add_competitionquestion'),
(38, 'Can change competition question', 10, 'change_competitionquestion'),
(39, 'Can delete competition question', 10, 'delete_competitionquestion'),
(40, 'Can view competition question', 10, 'view_competitionquestion'),
(41, 'Can add competition', 11, 'add_competition'),
(42, 'Can change competition', 11, 'change_competition'),
(43, 'Can delete competition', 11, 'delete_competition'),
(44, 'Can view competition', 11, 'view_competition'),
(45, 'Can add proposal', 12, 'add_proposal'),
(46, 'Can change proposal', 12, 'change_proposal'),
(47, 'Can delete proposal', 12, 'delete_proposal'),
(48, 'Can view proposal', 12, 'view_proposal'),
(49, 'Can add proposal attachment', 13, 'add_proposalattachment'),
(50, 'Can change proposal attachment', 13, 'change_proposalattachment'),
(51, 'Can delete proposal attachment', 13, 'delete_proposalattachment'),
(52, 'Can view proposal attachment', 13, 'view_proposalattachment'),
(53, 'Can add proposal revision', 14, 'add_proposalrevision'),
(54, 'Can change proposal revision', 14, 'change_proposalrevision'),
(55, 'Can delete proposal revision', 14, 'delete_proposalrevision'),
(56, 'Can view proposal revision', 14, 'view_proposalrevision'),
(57, 'Can add user rating', 15, 'add_userrating'),
(58, 'Can change user rating', 15, 'change_userrating'),
(59, 'Can delete user rating', 15, 'delete_userrating'),
(60, 'Can view user rating', 15, 'view_userrating'),
(61, 'Can add review', 16, 'add_review'),
(62, 'Can change review', 16, 'change_review'),
(63, 'Can delete review', 16, 'delete_review'),
(64, 'Can view review', 16, 'view_review'),
(65, 'Can add notification', 17, 'add_notification'),
(66, 'Can change notification', 17, 'change_notification'),
(67, 'Can delete notification', 17, 'delete_notification'),
(68, 'Can view notification', 17, 'view_notification'),
(69, 'Can add payment record', 18, 'add_paymentrecord'),
(70, 'Can change payment record', 18, 'change_paymentrecord'),
(71, 'Can delete payment record', 18, 'delete_paymentrecord'),
(72, 'Can view payment record', 18, 'view_paymentrecord');

-- --------------------------------------------------------

--
-- Table structure for table `competitions_competition`
--

DROP TABLE IF EXISTS `competitions_competition`;
CREATE TABLE IF NOT EXISTS `competitions_competition` (
  `id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `requirements` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `budget` decimal(12,2) NOT NULL,
  `currency` varchar(3) COLLATE utf8mb4_unicode_ci NOT NULL,
  `deadline` datetime(6) NOT NULL,
  `submission_deadline` datetime(6) NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `category` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tags` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `max_proposals` int UNSIGNED DEFAULT NULL,
  `allow_questions` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `client_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `winner_id` char(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `winning_proposal_id` char(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `competitions_competition_client_id_73416005_fk_accounts_user_id` (`client_id`),
  KEY `competitions_competition_winner_id_75c85f87_fk_accounts_user_id` (`winner_id`),
  KEY `competitions_competi_winning_proposal_id_bf844ff8_fk_proposals` (`winning_proposal_id`)
) ;

-- --------------------------------------------------------

--
-- Table structure for table `competitions_competitionbookmark`
--

DROP TABLE IF EXISTS `competitions_competitionbookmark`;
CREATE TABLE IF NOT EXISTS `competitions_competitionbookmark` (
  `id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `competition_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `competitions_competition_competition_id_user_id_312a6695_uniq` (`competition_id`,`user_id`),
  KEY `competitions_competi_user_id_42f02bfc_fk_accounts_` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `competitions_competitionquestion`
--

DROP TABLE IF EXISTS `competitions_competitionquestion`;
CREATE TABLE IF NOT EXISTS `competitions_competitionquestion` (
  `id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `question` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `answer` longtext COLLATE utf8mb4_unicode_ci,
  `answered_at` datetime(6) DEFAULT NULL,
  `is_public` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `answered_by_id` char(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `asked_by_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `competition_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `competitions_competi_answered_by_id_1688ffb3_fk_accounts_` (`answered_by_id`),
  KEY `competitions_competi_asked_by_id_d0cea78e_fk_accounts_` (`asked_by_id`),
  KEY `competitions_competi_competition_id_515492d7_fk_competiti` (`competition_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_user_id` (`user_id`)
) ;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(8, 'accounts', 'user'),
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(11, 'competitions', 'competition'),
(9, 'competitions', 'competitionbookmark'),
(10, 'competitions', 'competitionquestion'),
(4, 'contenttypes', 'contenttype'),
(16, 'feedback', 'review'),
(15, 'feedback', 'userrating'),
(17, 'notifications', 'notification'),
(18, 'payments', 'paymentrecord'),
(12, 'proposals', 'proposal'),
(13, 'proposals', 'proposalattachment'),
(14, 'proposals', 'proposalrevision'),
(5, 'sessions', 'session'),
(6, 'token_blacklist', 'blacklistedtoken'),
(7, 'token_blacklist', 'outstandingtoken');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2026-02-26 19:21:38.136103'),
(2, 'contenttypes', '0002_remove_content_type_name', '2026-02-26 19:21:38.293017'),
(3, 'auth', '0001_initial', '2026-02-26 19:21:39.416057'),
(4, 'auth', '0002_alter_permission_name_max_length', '2026-02-26 19:21:39.548215'),
(5, 'auth', '0003_alter_user_email_max_length', '2026-02-26 19:21:39.560974'),
(6, 'auth', '0004_alter_user_username_opts', '2026-02-26 19:21:39.595445'),
(7, 'auth', '0005_alter_user_last_login_null', '2026-02-26 19:21:39.599251'),
(8, 'auth', '0006_require_contenttypes_0002', '2026-02-26 19:21:39.606087'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2026-02-26 19:21:39.609869'),
(10, 'auth', '0008_alter_user_username_max_length', '2026-02-26 19:21:39.619111'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2026-02-26 19:21:39.622429'),
(12, 'auth', '0010_alter_group_name_max_length', '2026-02-26 19:21:39.632288'),
(13, 'auth', '0011_update_proxy_permissions', '2026-02-26 19:21:39.636680'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2026-02-26 19:21:39.641731'),
(15, 'accounts', '0001_initial', '2026-02-26 19:21:39.943227'),
(16, 'admin', '0001_initial', '2026-02-26 19:21:40.058446'),
(17, 'admin', '0002_logentry_remove_auto_add', '2026-02-26 19:21:40.064416'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2026-02-26 19:21:40.069288'),
(19, 'competitions', '0001_initial', '2026-02-26 19:21:40.290145'),
(20, 'proposals', '0001_initial', '2026-02-26 19:21:40.728325'),
(21, 'competitions', '0002_initial', '2026-02-26 19:21:41.129561'),
(22, 'feedback', '0001_initial', '2026-02-26 19:21:41.379440'),
(23, 'notifications', '0001_initial', '2026-02-26 19:21:41.440943'),
(24, 'payments', '0001_initial', '2026-02-26 19:21:41.617540'),
(25, 'sessions', '0001_initial', '2026-02-26 19:21:41.639006'),
(26, 'token_blacklist', '0001_initial', '2026-02-26 19:21:41.857658'),
(27, 'token_blacklist', '0002_outstandingtoken_jti_hex', '2026-02-26 19:21:41.878457'),
(28, 'token_blacklist', '0003_auto_20171017_2007', '2026-02-26 19:21:41.909474'),
(29, 'token_blacklist', '0004_auto_20171017_2013', '2026-02-26 19:21:42.047757'),
(30, 'token_blacklist', '0005_remove_outstandingtoken_jti', '2026-02-26 19:21:42.089337'),
(31, 'token_blacklist', '0006_auto_20171017_2113', '2026-02-26 19:21:42.109239'),
(32, 'token_blacklist', '0007_auto_20171017_2214', '2026-02-26 19:21:42.299227'),
(33, 'token_blacklist', '0008_migrate_to_bigautofield', '2026-02-26 19:21:42.468244'),
(34, 'token_blacklist', '0010_fix_migrate_to_bigautofield', '2026-02-26 19:21:42.481282'),
(35, 'token_blacklist', '0011_linearizes_history', '2026-02-26 19:21:42.482935'),
(36, 'token_blacklist', '0012_alter_outstandingtoken_user', '2026-02-26 19:21:42.494393'),
(37, 'token_blacklist', '0013_alter_blacklistedtoken_options_and_more', '2026-02-26 19:21:42.506713');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `feedback_review`
--

DROP TABLE IF EXISTS `feedback_review`;
CREATE TABLE IF NOT EXISTS `feedback_review` (
  `id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `rating` int UNSIGNED NOT NULL,
  `comment` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `review_type` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `is_public` tinyint(1) NOT NULL,
  `competition_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `reviewee_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `reviewer_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `feedback_review_reviewer_id_competition_id_1dc212dd_uniq` (`reviewer_id`,`competition_id`),
  KEY `feedback_review_competition_id_ee1ab75a_fk_competiti` (`competition_id`),
  KEY `feedback_review_reviewee_id_e3253456_fk_accounts_user_id` (`reviewee_id`)
) ;

-- --------------------------------------------------------

--
-- Table structure for table `feedback_userrating`
--

DROP TABLE IF EXISTS `feedback_userrating`;
CREATE TABLE IF NOT EXISTS `feedback_userrating` (
  `user_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `average_rating` decimal(3,2) NOT NULL,
  `total_reviews` int UNSIGNED NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`user_id`)
) ;

-- --------------------------------------------------------

--
-- Table structure for table `notifications_notification`
--

DROP TABLE IF EXISTS `notifications_notification`;
CREATE TABLE IF NOT EXISTS `notifications_notification` (
  `id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `notification_type` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `read_at` datetime(6) DEFAULT NULL,
  `related_competition_id` char(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `related_proposal_id` char(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `recipient_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `notifications_notifi_recipient_id_d055f3f0_fk_accounts_` (`recipient_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `payments_paymentrecord`
--

DROP TABLE IF EXISTS `payments_paymentrecord`;
CREATE TABLE IF NOT EXISTS `payments_paymentrecord` (
  `id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `amount` decimal(12,2) NOT NULL,
  `currency` varchar(3) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `platform_fee` decimal(10,2) NOT NULL,
  `net_amount` decimal(12,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `completed_at` datetime(6) DEFAULT NULL,
  `transaction_reference` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `notes` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `client_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `competition_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `freelancer_id` char(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `competition_id` (`competition_id`),
  UNIQUE KEY `transaction_reference` (`transaction_reference`),
  KEY `payments_paymentrecord_client_id_286b5508_fk_accounts_user_id` (`client_id`),
  KEY `payments_paymentreco_freelancer_id_7b8b8e26_fk_accounts_` (`freelancer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `proposals_proposal`
--

DROP TABLE IF EXISTS `proposals_proposal`;
CREATE TABLE IF NOT EXISTS `proposals_proposal` (
  `id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `proposed_budget` decimal(12,2) NOT NULL,
  `estimated_duration` int UNSIGNED NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `submission_note` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `client_score` int UNSIGNED DEFAULT NULL,
  `client_note` longtext COLLATE utf8mb4_unicode_ci,
  `is_winner` tinyint(1) NOT NULL,
  `competition_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `freelancer_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `proposals_proposal_competition_id_freelancer_id_68df0d93_uniq` (`competition_id`,`freelancer_id`),
  KEY `proposals_proposal_freelancer_id_c12f9a4e_fk_accounts_user_id` (`freelancer_id`)
) ;

-- --------------------------------------------------------

--
-- Table structure for table `proposals_proposalattachment`
--

DROP TABLE IF EXISTS `proposals_proposalattachment`;
CREATE TABLE IF NOT EXISTS `proposals_proposalattachment` (
  `id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `file` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `original_filename` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `file_size` int UNSIGNED NOT NULL,
  `file_type` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `proposal_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `proposals_proposalat_proposal_id_00fdd1bf_fk_proposals` (`proposal_id`)
) ;

-- --------------------------------------------------------

--
-- Table structure for table `proposals_proposalrevision`
--

DROP TABLE IF EXISTS `proposals_proposalrevision`;
CREATE TABLE IF NOT EXISTS `proposals_proposalrevision` (
  `id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `revision_number` int UNSIGNED NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `proposal_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `revised_by_id` char(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `proposals_proposalre_proposal_id_d0c8fbfa_fk_proposals` (`proposal_id`),
  KEY `proposals_proposalre_revised_by_id_64972da3_fk_accounts_` (`revised_by_id`)
) ;

-- --------------------------------------------------------

--
-- Table structure for table `token_blacklist_blacklistedtoken`
--

DROP TABLE IF EXISTS `token_blacklist_blacklistedtoken`;
CREATE TABLE IF NOT EXISTS `token_blacklist_blacklistedtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `blacklisted_at` datetime(6) NOT NULL,
  `token_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_id` (`token_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `token_blacklist_outstandingtoken`
--

DROP TABLE IF EXISTS `token_blacklist_outstandingtoken`;
CREATE TABLE IF NOT EXISTS `token_blacklist_outstandingtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `expires_at` datetime(6) NOT NULL,
  `user_id` char(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `jti` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_uniq` (`jti`),
  KEY `token_blacklist_outs_user_id_83bc629a_fk_accounts_` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `token_blacklist_outstandingtoken`
--

INSERT INTO `token_blacklist_outstandingtoken` (`id`, `token`, `created_at`, `expires_at`, `user_id`, `jti`) VALUES
(1, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MjczODYyMywiaWF0IjoxNzcyMTMzODIzLCJqdGkiOiIwMTQ2NzJiMjJjMmQ0NzkxYjRiMzcxZTM5Nzc0ZGZhNiIsInVzZXJfaWQiOiI4ZDZkYTVmMy1kNzFhLTRmYWItOGI5MS1jYTdlMDQ4MzVjOGYifQ.Nyw3eKL1sQuiMxaxhBsVSg3nWxswqWWSwPUSGZhQ548', '2026-02-26 19:23:43.331531', '2026-03-05 19:23:43.000000', '8d6da5f3d71a4fab8b91ca7e04835c8f', '014672b22c2d4791b4b371e39774dfa6'),
(2, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MjczODYyMywiaWF0IjoxNzcyMTMzODIzLCJqdGkiOiJjMmQ4MjE5Y2I2OTc0ZmNhOWU3NGY4NTAyYWE1YmI4MSIsInVzZXJfaWQiOiIzMjA0ZTFiYy00YzdkLTQ1NDEtOGVjZS1kNDM1N2JkOTM2OTEifQ.aU6IX2RS9n4OckFheOAQGmfkFGTFrfjkOEYvyu4wq0U', '2026-02-26 19:23:43.967426', '2026-03-05 19:23:43.000000', '3204e1bc4c7d45418eced4357bd93691', 'c2d8219cb6974fca9e74f8502aa5bb81'),
(3, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MjczODYyNCwiaWF0IjoxNzcyMTMzODI0LCJqdGkiOiJmOGU3ZmIwOWM3ODg0NmMyYjVhMmJmMjczMjUzZGZkZCIsInVzZXJfaWQiOiI4ZDZkYTVmMy1kNzFhLTRmYWItOGI5MS1jYTdlMDQ4MzVjOGYifQ.hkf6v2frJ9jj9boE4nqS8GiNIFEiLu6oteoqCFauDMY', '2026-02-26 19:23:44.261414', '2026-03-05 19:23:44.000000', '8d6da5f3d71a4fab8b91ca7e04835c8f', 'f8e7fb09c78846c2b5a2bf273253dfdd'),
(4, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MjczODYyNCwiaWF0IjoxNzcyMTMzODI0LCJqdGkiOiI1ZTgwZDQ5MDZlZDg0ZmI4ODEwMmMwMzY4MTE1NmYyNiIsInVzZXJfaWQiOiIzMjA0ZTFiYy00YzdkLTQ1NDEtOGVjZS1kNDM1N2JkOTM2OTEifQ.3mmH0d2feBzPo21x0H4mZr22-ZxhPqGjNO5K0Y7Z9dU', '2026-02-26 19:23:44.549609', '2026-03-05 19:23:44.000000', '3204e1bc4c7d45418eced4357bd93691', '5e80d4906ed84fb88102c03681156f26'),
(5, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MjczODY1NiwiaWF0IjoxNzcyMTMzODU2LCJqdGkiOiI5OGQ1ZjdjMTAxYTA0Yjk1OTI0MDkzZWU2NThhY2FhZiIsInVzZXJfaWQiOiI4ZDZkYTVmMy1kNzFhLTRmYWItOGI5MS1jYTdlMDQ4MzVjOGYifQ.nBuD5dNsEHrDgpd-vGdoAOdIsv9H0GnkN63N1GtxYJY', '2026-02-26 19:24:16.453585', '2026-03-05 19:24:16.000000', '8d6da5f3d71a4fab8b91ca7e04835c8f', '98d5f7c101a04b95924093ee658acaaf'),
(6, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3MjczODY1NiwiaWF0IjoxNzcyMTMzODU2LCJqdGkiOiI1NzhkNTM3MjcwNzI0YTIxODE0OWRiZmFkYjNiODBjZiIsInVzZXJfaWQiOiIzMjA0ZTFiYy00YzdkLTQ1NDEtOGVjZS1kNDM1N2JkOTM2OTEifQ.ELdj61rcNARvhZhsqcanwWr1AxC4a2wyjKxIaYTXpcw', '2026-02-26 19:24:16.741720', '2026-03-05 19:24:16.000000', '3204e1bc4c7d45418eced4357bd93691', '578d537270724a218149dbfadb3b80cf');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `accounts_user_groups`
--
ALTER TABLE `accounts_user_groups`
  ADD CONSTRAINT `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `accounts_user_groups_user_id_52b62117_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `accounts_user_user_permissions`
--
ALTER TABLE `accounts_user_user_permissions`
  ADD CONSTRAINT `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `accounts_user_user_p_user_id_e4f0a161_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `competitions_competition`
--
ALTER TABLE `competitions_competition`
  ADD CONSTRAINT `competitions_competi_winning_proposal_id_bf844ff8_fk_proposals` FOREIGN KEY (`winning_proposal_id`) REFERENCES `proposals_proposal` (`id`),
  ADD CONSTRAINT `competitions_competition_client_id_73416005_fk_accounts_user_id` FOREIGN KEY (`client_id`) REFERENCES `accounts_user` (`id`),
  ADD CONSTRAINT `competitions_competition_winner_id_75c85f87_fk_accounts_user_id` FOREIGN KEY (`winner_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `competitions_competitionbookmark`
--
ALTER TABLE `competitions_competitionbookmark`
  ADD CONSTRAINT `competitions_competi_competition_id_18bc34d7_fk_competiti` FOREIGN KEY (`competition_id`) REFERENCES `competitions_competition` (`id`),
  ADD CONSTRAINT `competitions_competi_user_id_42f02bfc_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `competitions_competitionquestion`
--
ALTER TABLE `competitions_competitionquestion`
  ADD CONSTRAINT `competitions_competi_answered_by_id_1688ffb3_fk_accounts_` FOREIGN KEY (`answered_by_id`) REFERENCES `accounts_user` (`id`),
  ADD CONSTRAINT `competitions_competi_asked_by_id_d0cea78e_fk_accounts_` FOREIGN KEY (`asked_by_id`) REFERENCES `accounts_user` (`id`),
  ADD CONSTRAINT `competitions_competi_competition_id_515492d7_fk_competiti` FOREIGN KEY (`competition_id`) REFERENCES `competitions_competition` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `feedback_review`
--
ALTER TABLE `feedback_review`
  ADD CONSTRAINT `feedback_review_competition_id_ee1ab75a_fk_competiti` FOREIGN KEY (`competition_id`) REFERENCES `competitions_competition` (`id`),
  ADD CONSTRAINT `feedback_review_reviewee_id_e3253456_fk_accounts_user_id` FOREIGN KEY (`reviewee_id`) REFERENCES `accounts_user` (`id`),
  ADD CONSTRAINT `feedback_review_reviewer_id_78e822d2_fk_accounts_user_id` FOREIGN KEY (`reviewer_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `feedback_userrating`
--
ALTER TABLE `feedback_userrating`
  ADD CONSTRAINT `feedback_userrating_user_id_75d75c2e_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `notifications_notification`
--
ALTER TABLE `notifications_notification`
  ADD CONSTRAINT `notifications_notifi_recipient_id_d055f3f0_fk_accounts_` FOREIGN KEY (`recipient_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `payments_paymentrecord`
--
ALTER TABLE `payments_paymentrecord`
  ADD CONSTRAINT `payments_paymentreco_competition_id_ec4fd957_fk_competiti` FOREIGN KEY (`competition_id`) REFERENCES `competitions_competition` (`id`),
  ADD CONSTRAINT `payments_paymentreco_freelancer_id_7b8b8e26_fk_accounts_` FOREIGN KEY (`freelancer_id`) REFERENCES `accounts_user` (`id`),
  ADD CONSTRAINT `payments_paymentrecord_client_id_286b5508_fk_accounts_user_id` FOREIGN KEY (`client_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `proposals_proposal`
--
ALTER TABLE `proposals_proposal`
  ADD CONSTRAINT `proposals_proposal_competition_id_f8387daa_fk_competiti` FOREIGN KEY (`competition_id`) REFERENCES `competitions_competition` (`id`),
  ADD CONSTRAINT `proposals_proposal_freelancer_id_c12f9a4e_fk_accounts_user_id` FOREIGN KEY (`freelancer_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `proposals_proposalattachment`
--
ALTER TABLE `proposals_proposalattachment`
  ADD CONSTRAINT `proposals_proposalat_proposal_id_00fdd1bf_fk_proposals` FOREIGN KEY (`proposal_id`) REFERENCES `proposals_proposal` (`id`);

--
-- Constraints for table `proposals_proposalrevision`
--
ALTER TABLE `proposals_proposalrevision`
  ADD CONSTRAINT `proposals_proposalre_proposal_id_d0c8fbfa_fk_proposals` FOREIGN KEY (`proposal_id`) REFERENCES `proposals_proposal` (`id`),
  ADD CONSTRAINT `proposals_proposalre_revised_by_id_64972da3_fk_accounts_` FOREIGN KEY (`revised_by_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `token_blacklist_blacklistedtoken`
--
ALTER TABLE `token_blacklist_blacklistedtoken`
  ADD CONSTRAINT `token_blacklist_blacklistedtoken_token_id_3cc7fe56_fk` FOREIGN KEY (`token_id`) REFERENCES `token_blacklist_outstandingtoken` (`id`);

--
-- Constraints for table `token_blacklist_outstandingtoken`
--
ALTER TABLE `token_blacklist_outstandingtoken`
  ADD CONSTRAINT `token_blacklist_outs_user_id_83bc629a_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

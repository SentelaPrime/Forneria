-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 10-12-2025 a las 06:53:51
-- Versión del servidor: 8.3.0
-- Versión de PHP: 8.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `forneria`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_group_id_b120cbf9` (`group_id`),
  KEY `auth_group_permissions_permission_id_84c5c92e` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id_2f476e4b` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `auth_permission`
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
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add producto', 7, 'add_producto'),
(26, 'Can change producto', 7, 'change_producto'),
(27, 'Can delete producto', 7, 'delete_producto'),
(28, 'Can view producto', 7, 'view_producto'),
(29, 'Can add venta', 8, 'add_venta'),
(30, 'Can change venta', 8, 'change_venta'),
(31, 'Can delete venta', 8, 'delete_venta'),
(32, 'Can view venta', 8, 'view_venta'),
(33, 'Can add detalle venta', 9, 'add_detalleventa'),
(34, 'Can change detalle venta', 9, 'change_detalleventa'),
(35, 'Can delete detalle venta', 9, 'delete_detalleventa'),
(36, 'Can view detalle venta', 9, 'view_detalleventa');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$1000000$xyNb8EtU16f4181yt1WZa9$T9XlKhSSTZbXhNdrUsvSp3QQZOgm1EOYFM2E3q/UBRs=', '2025-12-10 06:33:03.388667', 0, 'trabajador1', '', '', '', 0, 1, '2025-12-10 01:53:04.763250');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_user_id_6a12ed8b` (`user_id`),
  KEY `auth_user_groups_group_id_97559544` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_user_id_a95ead1b` (`user_id`),
  KEY `auth_user_user_permissions_permission_id_1fbb5f2c` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6` (`user_id`)
) ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'permission'),
(3, 'auth', 'group'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session'),
(7, 'ventas', 'producto'),
(8, 'ventas', 'venta'),
(9, 'ventas', 'detalleventa');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-12-10 01:50:21.723719'),
(2, 'auth', '0001_initial', '2025-12-10 01:50:22.442973'),
(3, 'admin', '0001_initial', '2025-12-10 01:50:22.805258'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-12-10 01:50:22.820141'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-12-10 01:50:22.833585'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-12-10 01:50:22.921879'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-12-10 01:50:22.963562'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-12-10 01:50:23.006882'),
(9, 'auth', '0004_alter_user_username_opts', '2025-12-10 01:50:23.019965'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-12-10 01:50:23.072473'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-12-10 01:50:23.074043'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-12-10 01:50:23.083935'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-12-10 01:50:23.130187'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-12-10 01:50:23.167462'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-12-10 01:50:23.217460'),
(16, 'auth', '0011_update_proxy_permissions', '2025-12-10 01:50:23.232233'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-12-10 01:50:23.270799'),
(18, 'sessions', '0001_initial', '2025-12-10 01:50:23.322057'),
(19, 'ventas', '0001_initial', '2025-12-10 01:50:23.617055');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('bqacob71mu02f7786ntmm0b66d0upv2k', '.eJxVzMEOwiAQBNB_4WxIKVtKPXrvN5CFXaRqICntyfjvlqQHvc68mbdwuG_J7ZVXt5C4CiUuv5nH8OTcCnpgvhcZSt7WxctG5NlWORfi1-20fwcJazrWYDWj1xYDG-64MxoHAuhjiEDkPfAUhwMYFYgsx3HslMGeGjQIk_h8AREKOOY:1vT9RE:osjD2DCjFqA3ummpRB0tK5QoKlXUlyme4ENcdj2pP60', '2025-12-24 01:56:20.334241'),
('vat03yvyeh3cpnclpa49iorkpewl37zy', '.eJxVzMEOwiAQBNB_4WxIKVtKPXrvN5CFXaRqICntyfjvlqQHvc68mbdwuG_J7ZVXt5C4CiUuv5nH8OTcCnpgvhcZSt7WxctG5NlWORfi1-20fwcJazrWYDWj1xYDG-64MxoHAuhjiEDkPfAUhwMYFYgsx3HslMGeGjQIk_h8AREKOOY:1vT9j1:_x-FZuD-XZljEQw6kWw5OME7Stv5a_AZMWdR7gTGW_I', '2025-12-24 02:14:43.657963'),
('ddwppa2cnyz2zcmv44t5e5pc5oz3uurd', '.eJxVzMEOwiAQBNB_4WxIKVtKPXrvN5CFXaRqICntyfjvlqQHvc68mbdwuG_J7ZVXt5C4CiUuv5nH8OTcCnpgvhcZSt7WxctG5NlWORfi1-20fwcJazrWYDWj1xYDG-64MxoHAuhjiEDkPfAUhwMYFYgsx3HslMGeGjQIk_h8AREKOOY:1vTAF2:NtrSqhoWetPEqyEM4-orOvfHgQyArJqp4MKeSmPMzhw', '2025-12-24 02:47:48.866477'),
('r1yjodbk93i9ldwxdos08k4wxwdniws1', '.eJxVzMEOwiAQBNB_4WxIKVtKPXrvN5CFXaRqICntyfjvlqQHvc68mbdwuG_J7ZVXt5C4CiUuv5nH8OTcCnpgvhcZSt7WxctG5NlWORfi1-20fwcJazrWYDWj1xYDG-64MxoHAuhjiEDkPfAUhwMYFYgsx3HslMGeGjQIk_h8AREKOOY:1vTCRv:MfVjBIqlRcbc8KoFxyKx7Ml2bWTg8gQoWmx4OGg2VAc', '2025-12-24 05:09:15.178992'),
('m0mw71xfas0fz6ledty4xwn9nu6vo25w', '.eJxVzMEOwiAQBNB_4WxIKVtKPXrvN5CFXaRqICntyfjvlqQHvc68mbdwuG_J7ZVXt5C4CiUuv5nH8OTcCnpgvhcZSt7WxctG5NlWORfi1-20fwcJazrWYDWj1xYDG-64MxoHAuhjiEDkPfAUhwMYFYgsx3HslMGeGjQIk_h8AREKOOY:1vTDl1:iFIRr_uBVmK5NQ2U993jUVClFHrwvGlHYx5ZEhZ5QIM', '2025-12-24 06:33:03.402391');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas_detalleventa`
--

DROP TABLE IF EXISTS `ventas_detalleventa`;
CREATE TABLE IF NOT EXISTS `ventas_detalleventa` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cantidad` int UNSIGNED NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `producto_id` bigint NOT NULL,
  `venta_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ventas_detalleventa_producto_id_a820c807` (`producto_id`),
  KEY `ventas_detalleventa_venta_id_c370bcd7` (`venta_id`)
) ;

--
-- Volcado de datos para la tabla `ventas_detalleventa`
--

INSERT INTO `ventas_detalleventa` (`id`, `cantidad`, `precio_unitario`, `subtotal`, `producto_id`, `venta_id`) VALUES
(1, 1, 123.00, 123.00, 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas_producto`
--

DROP TABLE IF EXISTS `ventas_producto`;
CREATE TABLE IF NOT EXISTS `ventas_producto` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `stock` int UNSIGNED NOT NULL,
  `categoria` varchar(20) NOT NULL,
  `imagen` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ;

--
-- Volcado de datos para la tabla `ventas_producto`
--

INSERT INTO `ventas_producto` (`id`, `nombre`, `precio`, `stock`, `categoria`, `imagen`) VALUES
(1, 'Botella', 123.00, 5, 'bebida', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas_venta`
--

DROP TABLE IF EXISTS `ventas_venta`;
CREATE TABLE IF NOT EXISTS `ventas_venta` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fecha` datetime(6) NOT NULL,
  `metodo_pago` varchar(20) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `descuento` decimal(5,2) NOT NULL,
  `iva` decimal(5,2) NOT NULL,
  `cliente_nombre` varchar(100) NOT NULL,
  `cliente_rut` varchar(20) DEFAULT NULL,
  `cliente_email` varchar(254) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `ventas_venta`
--

INSERT INTO `ventas_venta` (`id`, `fecha`, `metodo_pago`, `total`, `descuento`, `iva`, `cliente_nombre`, `cliente_rut`, `cliente_email`) VALUES
(1, '2025-12-10 04:11:14.374367', 'Tarjeta', 210.33, 10.00, 90.00, 'Joaquin', '22.062.642-3', 'joaquin.cortes19@inacapmail.cl');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

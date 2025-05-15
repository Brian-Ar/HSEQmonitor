-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 05-05-2025 a las 09:08:19
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `hseqmonitor`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asis_no_iden`
--

CREATE TABLE `asis_no_iden` (
  `id_asis_no_iden` int(11) NOT NULL,
  `id_evento` int(11) NOT NULL,
  `cedula_ingresada` varchar(20) NOT NULL,
  `nombre_ingresado` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleados`
--

CREATE TABLE `empleados` (
  `id_empleado` int(11) NOT NULL,
  `cedula_em` varchar(20) NOT NULL,
  `nombre_em` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `empleados`
--

INSERT INTO `empleados` (`id_empleado`, `cedula_em`, `nombre_em`) VALUES
(1, '777', 'prueba_admin'),
(2, '333', 'prueba_regular'),
(3, '111', 'prueba_emp');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `eventos`
--

CREATE TABLE `eventos` (
  `id_evento` int(11) NOT NULL,
  `fecha_ev` date NOT NULL,
  `titulo_ev` varchar(255) NOT NULL,
  `duracion_ev` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `eventos_temp`
--

CREATE TABLE `eventos_temp` (
  `id_evento_temp` int(11) NOT NULL,
  `t_ev_temp` varchar(255) NOT NULL,
  `f_ev_temp` date NOT NULL,
  `d_ev_temp` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `lista_asis`
--

CREATE TABLE `lista_asis` (
  `id_asis` int(11) NOT NULL,
  `id_evento` int(11) NOT NULL,
  `id_empleado` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `lista_asis_temp`
--

CREATE TABLE `lista_asis_temp` (
  `id_asis_temp` int(11) NOT NULL,
  `id_evento_temp` int(11) NOT NULL,
  `id_empleado` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `contra_us` varchar(255) NOT NULL,
  `correo_us` varchar(255) DEFAULT NULL,
  `tipo_us` enum('Regular','Administrador') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `contra_us`, `correo_us`, `tipo_us`) VALUES
(1, 'scrypt:32768:8:1$LoTElzJFkJrazuqQ$ca20957ab90c4316144b88219e227325959b15e406e6930dd7f9aac9707e786756513a53488b0bfc035e7e2f21528bbcc6e1df0cf796f6bb628b668ca9e54e59', 'p.admin@hseqmonitor.com', 'Administrador'),
(2, 'scrypt:32768:8:1$8Cr2Y5eidokfvBxk$2c2ada3234c06ffb1f5a6a16763bad34ae7e5e5792a1e41e621301be42082f7bfb38befcead49cc124d2e69b288c2c2c87068315a5c3db121fe5a7443521e382', 'p.regular@hseqmonitor.com', 'Regular');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `asis_no_iden`
--
ALTER TABLE `asis_no_iden`
  ADD PRIMARY KEY (`id_asis_no_iden`),
  ADD KEY `ani_id_evento_FK` (`id_evento`);

--
-- Indices de la tabla `empleados`
--
ALTER TABLE `empleados`
  ADD PRIMARY KEY (`id_empleado`);

--
-- Indices de la tabla `eventos`
--
ALTER TABLE `eventos`
  ADD PRIMARY KEY (`id_evento`);

--
-- Indices de la tabla `eventos_temp`
--
ALTER TABLE `eventos_temp`
  ADD PRIMARY KEY (`id_evento_temp`);

--
-- Indices de la tabla `lista_asis`
--
ALTER TABLE `lista_asis`
  ADD PRIMARY KEY (`id_asis`),
  ADD KEY `la_id_evento_FK` (`id_evento`),
  ADD KEY `la_id_empleado_FK` (`id_empleado`);

--
-- Indices de la tabla `lista_asis_temp`
--
ALTER TABLE `lista_asis_temp`
  ADD PRIMARY KEY (`id_asis_temp`),
  ADD KEY `lat_id_evento_temp_FK` (`id_evento_temp`),
  ADD KEY `lat_id_empleado_FK` (`id_empleado`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `asis_no_iden`
--
ALTER TABLE `asis_no_iden`
  MODIFY `id_asis_no_iden` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT de la tabla `empleados`
--
ALTER TABLE `empleados`
  MODIFY `id_empleado` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `eventos`
--
ALTER TABLE `eventos`
  MODIFY `id_evento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `eventos_temp`
--
ALTER TABLE `eventos_temp`
  MODIFY `id_evento_temp` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `lista_asis`
--
ALTER TABLE `lista_asis`
  MODIFY `id_asis` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `lista_asis_temp`
--
ALTER TABLE `lista_asis_temp`
  MODIFY `id_asis_temp` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `asis_no_iden`
--
ALTER TABLE `asis_no_iden`
  ADD CONSTRAINT `ani_id_evento_FK` FOREIGN KEY (`id_evento`) REFERENCES `eventos` (`id_evento`);

--
-- Filtros para la tabla `lista_asis`
--
ALTER TABLE `lista_asis`
  ADD CONSTRAINT `la_id_empleado_FK` FOREIGN KEY (`id_empleado`) REFERENCES `empleados` (`id_empleado`),
  ADD CONSTRAINT `la_id_evento_FK` FOREIGN KEY (`id_evento`) REFERENCES `eventos` (`id_evento`);

--
-- Filtros para la tabla `lista_asis_temp`
--
ALTER TABLE `lista_asis_temp`
  ADD CONSTRAINT `lat_id_empleado_FK` FOREIGN KEY (`id_empleado`) REFERENCES `empleados` (`id_empleado`),
  ADD CONSTRAINT `lat_id_evento_temp_FK` FOREIGN KEY (`id_evento_temp`) REFERENCES `eventos_temp` (`id_evento_temp`);

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `us_id_usuario_FK` FOREIGN KEY (`id_usuario`) REFERENCES `empleados` (`id_empleado`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

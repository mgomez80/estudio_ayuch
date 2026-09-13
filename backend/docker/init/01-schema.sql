USE db_estudio_ayuch;
SET NAMES utf8mb4;

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
DROP TABLE IF EXISTS `acciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `acciones` (
  `id_accion` int unsigned NOT NULL AUTO_INCREMENT,
  `desc_accion` char(250) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `activa` char(1) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_accion`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `agenda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `agenda` (
  `id_agenda` int unsigned NOT NULL AUTO_INCREMENT,
  `usuarios_id_usuario` int unsigned NOT NULL,
  `cuentas_id_cta` int unsigned NOT NULL,
  `desc_agenda` char(250) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `fecha_agenda` date DEFAULT NULL,
  `activo` char(1) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_agenda`),
  KEY `Agenda_FKIndex1` (`cuentas_id_cta`),
  KEY `Agenda_FKIndex2` (`usuarios_id_usuario`)
) ENGINE=MyISAM AUTO_INCREMENT=377 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `boca_de_pago`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `boca_de_pago` (
  `id_boca_de_pago` int unsigned NOT NULL AUTO_INCREMENT,
  `cobros_id_cobros` int unsigned NOT NULL,
  `desc_boca_de_pago` char(254) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `activo` char(1) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_boca_de_pago`),
  KEY `boca_de_pago_FKIndex1` (`cobros_id_cobros`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `carga_masiva_contactos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carga_masiva_contactos` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `matricula` varchar(30) COLLATE utf8mb4_general_ci NOT NULL,
  `accion` varchar(150) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `resultado` varchar(150) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `fecha_contacto` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `hora_contacto` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nota` varchar(500) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `contacto_actualizado` char(1) COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'N',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `carga_masiva_ctas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carga_masiva_ctas` (
  `matricula` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nombre` varchar(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `contacto` varchar(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `monto_deuda` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `fecha_deuda` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `fecha_asignacion` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `empleador` varchar(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `cuenta_cliente` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `id_sub_cliente` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `observacion` varchar(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `mora` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ent_actualizada` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'N',
  `cta_actualizada` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'N'
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `carga_masiva_demandas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carga_masiva_demandas` (
  `matricula` char(30) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `nombre` char(250) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `caratula` char(250) DEFAULT NULL,
  `expediente` char(250) DEFAULT NULL,
  `secretaria` int DEFAULT NULL,
  `juzgado` int DEFAULT NULL,
  `monto_demanda` decimal(10,2) DEFAULT NULL,
  `apoderado` char(40) DEFAULT NULL,
  `fecha_inicio_demanda` char(20) DEFAULT NULL,
  `fecha_mora` char(20) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `fecha_inicio_caducidad` char(20) DEFAULT NULL,
  `monto_deuda` decimal(10,2) DEFAULT NULL,
  `fecha_deuda` char(50) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `fecha_asignacion` char(50) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `empleador` char(250) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `cuenta_cliente` char(50) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `id_sub_cliente` int unsigned DEFAULT NULL,
  `observacion` char(250) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `ent_actualizada` char(1) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT 'N',
  `cta_actualzada` char(1) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT 'N',
  `demanda_actualizada` char(1) DEFAULT NULL,
  `id_cuenta` int DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `carga_masiva_dir`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carga_masiva_dir` (
  `matricula` char(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `calle_dir` varchar(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nro_dir` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `piso_dir` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `dpto_dir` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `casa_dir` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `manzana_dir` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `barrio_dir` varchar(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `CP_dir` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `localidad_dir` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `departamento_dir` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `provincia_dir` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `seccional_dir` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `tipo_dir` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `observacion_dir` varchar(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `dir_actualizada` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'N'
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `carga_masiva_mail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carga_masiva_mail` (
  `matricula` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci DEFAULT NULL,
  `mail` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci DEFAULT NULL,
  `mail_actualizado` char(1) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci DEFAULT 'N'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `carga_masiva_tel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carga_masiva_tel` (
  `matricula` char(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `tipo` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `codigo_area` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `numero_tel` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `observaciones` varchar(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `tel_actualizado` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'N'
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `categorias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categorias` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `creado_en` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `actualizado_en` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `id_cliente` int unsigned NOT NULL AUTO_INCREMENT,
  `cuenta_cliente` int unsigned NOT NULL,
  `desc_cliente` char(200) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `activo` char(1) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT 'S',
  PRIMARY KEY (`id_cliente`,`cuenta_cliente`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `cobros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cobros` (
  `id_cobros` int unsigned NOT NULL AUTO_INCREMENT,
  `movimientos_id_mov` int unsigned NOT NULL,
  `CONCEPTOS_id_concepto` int unsigned NOT NULL,
  `concepto_cobro` int DEFAULT NULL,
  `cuentas_id_cta` int NOT NULL,
  `convenios_id_convenios` int unsigned DEFAULT NULL,
  `fcha_cobro` date DEFAULT NULL,
  `cuota` int unsigned DEFAULT NULL,
  `desc_cobro` char(250) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `importe` decimal(10,2) DEFAULT NULL,
  `rendido` char(1) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `anulado` char(1) COLLATE latin1_general_ci NOT NULL DEFAULT 'N',
  `anulado_por` int DEFAULT NULL,
  `anulado_ts` datetime DEFAULT NULL,
  PRIMARY KEY (`id_cobros`)
) ENGINE=MyISAM AUTO_INCREMENT=1217 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `conceptos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `conceptos` (
  `id_concepto` int unsigned NOT NULL AUTO_INCREMENT,
  `rubros_id_rubro` int unsigned NOT NULL,
  `desc_concepto` char(254) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `activo` char(1) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_concepto`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `condicion_iva`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `condicion_iva` (
  `id_cond_iva` int unsigned NOT NULL AUTO_INCREMENT,
  `detalle` char(50) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `porcentaje` decimal(10,0) DEFAULT NULL,
  PRIMARY KEY (`id_cond_iva`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `configuracion_negocio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `configuracion_negocio` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre_negocio` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `direccion` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `telefono` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `cuit_rif` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `logo_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `moneda_simbolo` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '$',
  `actualizado_en` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `contactos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contactos` (
  `id_contacto` int unsigned NOT NULL AUTO_INCREMENT,
  `usuarios_id_usuario` int unsigned NOT NULL,
  `cuentas_id_cta` int unsigned NOT NULL,
  `resultados_id_resultado` int unsigned NOT NULL,
  `acciones_id_accion` int unsigned NOT NULL,
  `fecha_contacto` date DEFAULT NULL,
  `hora_contacto` char(10) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `nota_contacto` longblob,
  `activo` char(1) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_contacto`),
  KEY `contactos_FKIndex1` (`acciones_id_accion`),
  KEY `contactos_FKIndex4` (`usuarios_id_usuario`)
) ENGINE=MyISAM AUTO_INCREMENT=9308 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `contactos_judiciales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contactos_judiciales` (
  `id_contacto_judicial` int unsigned NOT NULL AUTO_INCREMENT,
  `usuarios_id_usuario` int unsigned NOT NULL,
  `cuentas_id_cta` int unsigned NOT NULL,
  `resultados_id_resultado` int unsigned NOT NULL,
  `acciones_id_accion` int unsigned NOT NULL,
  `fecha_contacto` date DEFAULT NULL,
  `hora_contacto` char(10) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `nota_contacto` longblob,
  `fecha_inicio_caducidad` date DEFAULT NULL,
  `activo` char(1) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_contacto_judicial`),
  KEY `contactos_FKIndex2` (`cuentas_id_cta`),
  KEY `contactos_FKIndex3` (`resultados_id_resultado`),
  KEY `contactos_FKIndex1` (`acciones_id_accion`),
  KEY `contactos_FKIndex4` (`usuarios_id_usuario`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `convenios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `convenios` (
  `id_convenios` int unsigned NOT NULL AUTO_INCREMENT,
  `cuentas_id_cta` int unsigned NOT NULL,
  `propuestas_id_propuesta` int unsigned NOT NULL,
  `fecha_convenio` date DEFAULT NULL,
  `concepto_convenio` int unsigned DEFAULT NULL,
  `estado_convenio` char(50) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `importe_convenio` decimal(10,2) DEFAULT NULL,
  `anticipo_convenio` decimal(10,2) DEFAULT NULL,
  `cant_cuotas_convenio` int unsigned DEFAULT NULL,
  `importe_cuota_convenio` decimal(10,2) DEFAULT NULL,
  `cuotas_pagadas` int unsigned DEFAULT NULL,
  `saldo_convenio` decimal(10,2) DEFAULT NULL,
  `observaciones_convenio` char(254) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `cancelado` char(1) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `activo` char(1) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_convenios`),
  KEY `convenios_FKIndex2` (`cuentas_id_cta`)
) ENGINE=MyISAM AUTO_INCREMENT=35 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `convenios_judiciales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `convenios_judiciales` (
  `id_convenios_judiciales` int unsigned NOT NULL AUTO_INCREMENT,
  `cuentas_id_cta` int unsigned NOT NULL,
  `propuestas_id_propuesta` int unsigned NOT NULL,
  `fecha_convenio` date DEFAULT NULL,
  `concepto_convenio` int unsigned DEFAULT NULL,
  `estado_convenio` char(50) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `importe_convenio` decimal(10,2) DEFAULT NULL,
  `anticipo_convenio` decimal(10,2) DEFAULT NULL,
  `cant_cuotas_convenio` int unsigned DEFAULT NULL,
  `importe_cuota_convenio` decimal(10,2) DEFAULT NULL,
  `cuotas_pagadas` int unsigned DEFAULT NULL,
  `saldo_convenio` decimal(10,2) DEFAULT NULL,
  `observaciones_convenio` char(254) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `cancelado` char(1) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `activo` char(1) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_convenios_judiciales`),
  KEY `convenios_FKIndex1` (`propuestas_id_propuesta`),
  KEY `convenios_FKIndex2` (`cuentas_id_cta`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `ctas_tmp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ctas_tmp` (
  `cuenta` char(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `cuentas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cuentas` (
  `id_cta` int unsigned NOT NULL AUTO_INCREMENT,
  `estados_id_estado` int unsigned DEFAULT NULL,
  `sub_estados_id_sub_est` int unsigned DEFAULT NULL,
  `entidades_matricula_ent` char(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `cuenta_cliente` char(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `subclientes_id_subcli` int unsigned NOT NULL,
  `deudatrans_cta` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `deudaact_cta` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `fechaingreso_cta` date DEFAULT NULL,
  `fecha_padron_cta` char(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '0001-01-01',
  `fecha_asignacion_cta` char(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '0001-01-01',
  `empleador_cta` char(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `activa_cta` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'S',
  `supervisor` int unsigned DEFAULT NULL,
  `observacion_cta` char(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ejecutivo` int unsigned DEFAULT NULL,
  `judicial` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'N',
  `promo` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `descripcion_promo` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `mora` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_cta`),
  KEY `cuentas_FKIndex1` (`subclientes_id_subcli`),
  KEY `cuentas_FKIndex2` (`entidades_matricula_ent`)
) ENGINE=MyISAM AUTO_INCREMENT=10105 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `cuentas_reemplazar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cuentas_reemplazar` (
  `id_cta` int unsigned NOT NULL AUTO_INCREMENT,
  `estados_id_estado` int unsigned DEFAULT NULL,
  `sub_estados_id_sub_est` int unsigned DEFAULT NULL,
  `entidades_matricula_ent` char(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `cuenta_cliente` char(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `subclientes_id_subcli` int unsigned NOT NULL,
  `deudatrans_cta` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `deudaact_cta` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `fechaingreso_cta` date DEFAULT NULL,
  `fecha_padron_cta` char(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '0001-01-01',
  `fecha_asignacion_cta` char(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '0001-01-01',
  `empleador_cta` char(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `activa_cta` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'S',
  `supervisor` int unsigned DEFAULT NULL,
  `observacion_cta` char(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ejecutivo` int unsigned DEFAULT NULL,
  `judicial` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'N',
  `promo` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `descripcion_promo` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `mora` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_cta`),
  KEY `cuentas_FKIndex1` (`subclientes_id_subcli`),
  KEY `cuentas_FKIndex2` (`entidades_matricula_ent`)
) ENGINE=MyISAM AUTO_INCREMENT=9788 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `demandas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `demandas` (
  `id_demanda` int NOT NULL AUTO_INCREMENT,
  `caratula` char(250) DEFAULT NULL,
  `expediente` char(250) DEFAULT NULL,
  `secretarias_id_secretaria` int DEFAULT NULL,
  `juzgados_id_juzgado` int DEFAULT NULL,
  `monto_demanda` decimal(10,2) DEFAULT NULL,
  `apoderado` char(40) DEFAULT NULL,
  `fecha_inicio_demanda` char(20) DEFAULT NULL,
  `fecha_mora` char(20) DEFAULT NULL,
  `cuentas_id_cta` int DEFAULT NULL,
  `fecha_inicio_caducidad` char(20) DEFAULT NULL,
  `activa` char(1) DEFAULT 'S',
  PRIMARY KEY (`id_demanda`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `direcciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `direcciones` (
  `id_dir` int unsigned NOT NULL AUTO_INCREMENT,
  `entidades_matricula_ent` char(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `calle_dir` char(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nro_dir` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `piso_dir` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `dpto_dir` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `casa_dir` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `manzana_dir` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `barrio_dir` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `CP_dir` char(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `localidad_dir` char(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `departamento_dir` char(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `provincia_dir` char(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `activa_dir` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'S',
  `seccional_dir` char(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `tipo_dir` char(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `observacion_dir` char(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_dir`),
  KEY `direcciones_FKIndex1` (`entidades_matricula_ent`)
) ENGINE=MyISAM AUTO_INCREMENT=14554 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `entidades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `entidades` (
  `tipo_matricula_id_tipomatricula` int unsigned DEFAULT NULL,
  `condicion_iva_id_cond_iva` int unsigned DEFAULT NULL,
  `razon_social_ent` char(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `matricula_ent` char(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `contacto_ent` char(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `activo_ent` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'S',
  `genero` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`matricula_ent`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `estados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estados` (
  `id_estado` int unsigned NOT NULL AUTO_INCREMENT,
  `desc_estado` char(254) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `tipo_estado` char(50) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `activo` char(1) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_estado`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `gastos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gastos` (
  `id_gastos` int unsigned NOT NULL AUTO_INCREMENT,
  `movimientos_id_mov` int unsigned NOT NULL,
  `fcha_gasto` date DEFAULT NULL,
  `desc_gasto` char(254) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `importe_gasto` decimal(10,2) DEFAULT NULL,
  `activo` char(1) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_gastos`),
  KEY `gastos_FKIndex1` (`movimientos_id_mov`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `gastos_judiciales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gastos_judiciales` (
  `id_gasto_judicial` int unsigned NOT NULL AUTO_INCREMENT,
  `bono_profesional` decimal(10,2) DEFAULT NULL,
  `tasa_judicial` int DEFAULT NULL,
  `monto_tasa_judicial` decimal(10,2) DEFAULT NULL,
  `planilla_fiscal` decimal(10,2) DEFAULT NULL,
  `movilidad` decimal(10,2) DEFAULT NULL,
  `fotocopias` decimal(10,2) DEFAULT NULL,
  `sellado` decimal(10,2) DEFAULT NULL,
  `diligencias` decimal(10,2) DEFAULT NULL,
  `otros` decimal(10,2) DEFAULT NULL,
  `observaciones` char(250) DEFAULT NULL,
  `cuentas_id_cta` char(20) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  PRIMARY KEY (`id_gasto_judicial`),
  KEY `FK_gastos_jud_ctas` (`cuentas_id_cta`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `gestor_acciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gestor_acciones` (
  `id_accion` int NOT NULL AUTO_INCREMENT,
  `id_sesion` int NOT NULL,
  `id_usuario` int NOT NULL,
  `tool_name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `argumentos_json` text COLLATE utf8mb4_general_ci NOT NULL,
  `estado` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `resultado_json` text COLLATE utf8mb4_general_ci,
  `creado_at` datetime NOT NULL,
  `resuelto_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id_accion`),
  KEY `idx_ga_sesion` (`id_sesion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `gestor_chat_mensajes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gestor_chat_mensajes` (
  `id_mensaje` int NOT NULL AUTO_INCREMENT,
  `id_sesion` int NOT NULL,
  `rol` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `contenido` mediumtext COLLATE utf8mb4_general_ci,
  `tool_calls_json` mediumtext COLLATE utf8mb4_general_ci,
  `creado_at` datetime NOT NULL,
  PRIMARY KEY (`id_mensaje`),
  KEY `idx_gcm_sesion` (`id_sesion`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `gestor_chat_sesiones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gestor_chat_sesiones` (
  `id_sesion` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `titulo` varchar(200) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `creado_at` datetime NOT NULL,
  PRIMARY KEY (`id_sesion`),
  KEY `idx_gcs_usuario` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `gestor_informes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gestor_informes` (
  `id_informe` int NOT NULL AUTO_INCREMENT,
  `id_sesion` int DEFAULT NULL,
  `id_usuario` int NOT NULL,
  `tipo` varchar(30) COLLATE utf8mb4_general_ci NOT NULL,
  `titulo` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `parametros_json` text COLLATE utf8mb4_general_ci,
  `html` mediumtext COLLATE utf8mb4_general_ci NOT NULL,
  `creado_at` datetime NOT NULL,
  PRIMARY KEY (`id_informe`),
  KEY `idx_gi_usuario` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `historial_precios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historial_precios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_producto` int NOT NULL,
  `precio_costo_anterior` decimal(10,2) DEFAULT NULL,
  `precio_venta_anterior` decimal(10,2) DEFAULT NULL,
  `precio_costo_nuevo` decimal(10,2) DEFAULT NULL,
  `precio_venta_nuevo` decimal(10,2) DEFAULT NULL,
  `fecha_cambio` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `id_usuario` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_producto` (`id_producto`),
  KEY `id_usuario` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `juzgados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `juzgados` (
  `id_juzgado` int unsigned NOT NULL AUTO_INCREMENT,
  `nombre` char(50) DEFAULT NULL,
  `detalle` char(200) DEFAULT NULL,
  PRIMARY KEY (`id_juzgado`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `mail_envios_masivos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mail_envios_masivos` (
  `id_envio` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `tipo_mensaje` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `origen` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `total` int NOT NULL DEFAULT '0',
  `enviados` int NOT NULL DEFAULT '0',
  `errores` int NOT NULL DEFAULT '0',
  `descartados_sin_cliente` int NOT NULL DEFAULT '0',
  `descartados_duplicados` int NOT NULL DEFAULT '0',
  `estado` varchar(20) COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'pendiente',
  `creado_at` datetime NOT NULL,
  `finalizado_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id_envio`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `mails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mails` (
  `id_mails` int unsigned NOT NULL AUTO_INCREMENT,
  `entidades_matricula_ent` char(30) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `mail` varchar(250) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `tipo_mail` varchar(50) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `activo_mail` char(1) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT 'S',
  PRIMARY KEY (`id_mails`),
  KEY `mails_FKIndex1` (`entidades_matricula_ent`)
) ENGINE=MyISAM AUTO_INCREMENT=18036 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `movimientos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movimientos` (
  `id_mov` int unsigned NOT NULL AUTO_INCREMENT,
  `importe_ingreso_mov` decimal(10,2) DEFAULT NULL,
  `importe_egreso_mov` decimal(10,2) DEFAULT NULL,
  `fecha_mov` date DEFAULT NULL,
  `desc_mov` char(254) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `anulado_mov` char(1) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT 'N',
  PRIMARY KEY (`id_mov`)
) ENGINE=MyISAM AUTO_INCREMENT=1215 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `movimientos_stock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movimientos_stock` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_producto` int NOT NULL,
  `tipo_movimiento` enum('Entrada','Salida','Ajuste Positivo','Ajuste Negativo','Venta','Merma','Devolución') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `cantidad` int NOT NULL,
  `fecha_movimiento` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `id_usuario` int DEFAULT NULL,
  `referencia` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `stock_anterior` int DEFAULT '0',
  `stock_nuevo` int DEFAULT '0',
  `notas` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  KEY `id_usuario` (`id_usuario`),
  KEY `idx_movimiento_producto_fecha` (`id_producto`,`fecha_movimiento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `pago_comisiones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pago_comisiones` (
  `id_pago_com` int unsigned NOT NULL AUTO_INCREMENT,
  `movimientos_id_mov` int unsigned NOT NULL,
  `subclientes_id_subcli` int unsigned NOT NULL,
  `importe_comision` decimal(10,2) DEFAULT NULL,
  `fecha_pago_comision` date DEFAULT NULL,
  `mes_de_comision` char(20) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_pago_com`),
  KEY `pago_comisiones_FKIndex1` (`subclientes_id_subcli`),
  KEY `pago_comisiones_FKIndex2` (`movimientos_id_mov`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `pagos_judiciales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pagos_judiciales` (
  `id_pago_judicial` int NOT NULL AUTO_INCREMENT,
  `importe` decimal(10,2) DEFAULT NULL,
  `detalle` char(250) DEFAULT NULL,
  `gastos_pendientes` decimal(10,2) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `cuentas_id_cta` int DEFAULT NULL,
  `id_mov` int DEFAULT NULL,
  `cancelado` char(1) DEFAULT NULL,
  `id_concepto` int DEFAULT NULL,
  `concepto_cobro` int DEFAULT NULL,
  `cuota` int DEFAULT NULL,
  PRIMARY KEY (`id_pago_judicial`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `privilegios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `privilegios` (
  `id_privilegio` int unsigned NOT NULL AUTO_INCREMENT,
  `desc_privilegio` char(254) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_privilegio`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `codigo_interno` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `codigo_barras` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `nombre` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `id_categoria` int DEFAULT NULL,
  `id_proveedor` int DEFAULT NULL,
  `unidad_medida` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'unidad',
  `precio_costo` decimal(10,2) DEFAULT '0.00',
  `precio_venta` decimal(10,2) NOT NULL DEFAULT '0.00',
  `stock_actual` int DEFAULT '0',
  `stock_minimo` int DEFAULT '0',
  `imagen_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `estado` enum('Activo','Inactivo') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Activo',
  `creado_en` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `actualizado_en` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `cuentas_id_cta` int NOT NULL,
  `nro_producto` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `desc_producto` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `saldo_prod` decimal(10,0) NOT NULL,
  `observacion_prod` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `activo` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codigo_interno` (`codigo_interno`),
  UNIQUE KEY `codigo_barras` (`codigo_barras`),
  KEY `id_categoria` (`id_categoria`),
  KEY `id_proveedor` (`id_proveedor`),
  KEY `idx_producto_nombre` (`nombre`(191))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `propuestas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `propuestas` (
  `id_propuesta` int unsigned NOT NULL AUTO_INCREMENT,
  `contactos_id_contacto` int unsigned NOT NULL,
  `cuentas_id_cta` int unsigned NOT NULL,
  `fecha_propuesta` date DEFAULT NULL,
  `concepto_propuesta` char(100) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `fechavto_propuesta` date DEFAULT NULL,
  `estado_propuesta` char(100) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `activa` char(1) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_propuesta`),
  KEY `propuestas_FKIndex1` (`cuentas_id_cta`),
  KEY `propuestas_FKIndex2` (`contactos_id_contacto`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `proveedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedores` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `contacto_nombre` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `telefono` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `direccion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `creado_en` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `actualizado_en` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_proveedor_nombre` (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `provincias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `provincias` (
  `id_provincia` int unsigned NOT NULL AUTO_INCREMENT,
  `nombre_provincia` char(50) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_provincia`)
) ENGINE=MyISAM AUTO_INCREMENT=24 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `registro_envios_mail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registro_envios_mail` (
  `id` int NOT NULL AUTO_INCREMENT,
  `matricula` varchar(50) DEFAULT NULL,
  `cuentas_id_cta` int DEFAULT NULL,
  `destino` varchar(255) DEFAULT NULL,
  `asunto` varchar(250) DEFAULT NULL,
  `mensaje` text,
  `tipo` varchar(50) DEFAULT NULL,
  `id_usuario` int DEFAULT NULL,
  `estado` varchar(255) DEFAULT NULL,
  `fecha_envio` datetime DEFAULT NULL,
  `envio_masivo_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_registro_envios_mail_usuario` (`id_usuario`),
  KEY `idx_registro_envios_mail_fecha` (`fecha_envio`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `registro_envios_whatsapp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registro_envios_whatsapp` (
  `id` int NOT NULL AUTO_INCREMENT,
  `matricula` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `cuentas_id_cta` int DEFAULT NULL,
  `destino` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `mensaje` text CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci,
  `tipo` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `id_usuario` int DEFAULT NULL,
  `estado` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `fecha_envio` datetime DEFAULT NULL,
  `envio_masivo_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_rew_fecha` (`fecha_envio`),
  KEY `idx_rew_usuario_fecha` (`id_usuario`,`fecha_envio`)
) ENGINE=InnoDB AUTO_INCREMENT=1186 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `rendidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rendidos` (
  `id_rendido` int unsigned NOT NULL AUTO_INCREMENT,
  `movimientos_id_mov` int unsigned NOT NULL,
  `subclientes_id_subcli` int unsigned NOT NULL,
  `cobros_id_cobros` int unsigned NOT NULL,
  `fecha_rendido` date DEFAULT NULL,
  `importe_rendido` decimal(10,2) DEFAULT NULL,
  `periodo_rendido` char(40) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_rendido`),
  KEY `rendidos_FKIndex1` (`cobros_id_cobros`),
  KEY `rendidos_FKIndex2` (`subclientes_id_subcli`),
  KEY `rendidos_FKIndex3` (`movimientos_id_mov`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `resultados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resultados` (
  `id_resultado` int unsigned NOT NULL AUTO_INCREMENT,
  `desc_resultado` char(254) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `positivo` char(1) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `activo` char(1) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_resultado`)
) ENGINE=MyISAM AUTO_INCREMENT=28 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `rubros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rubros` (
  `id_rubro` int unsigned NOT NULL AUTO_INCREMENT,
  `desc_rubro` char(250) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `activo` char(1) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_rubro`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `secretarias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `secretarias` (
  `id_secretaria` int unsigned NOT NULL AUTO_INCREMENT,
  `nombre` char(50) DEFAULT NULL,
  PRIMARY KEY (`id_secretaria`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `sincronizacion_cta_24_05_26`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sincronizacion_cta_24_05_26` (
  `COL 1` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `COL 2` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `COL 3` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `COL 4` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `COL 5` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `COL 6` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `COL 7` varchar(7) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `COL 8` varchar(17) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `COL 9` varchar(13) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `COL 10` varchar(14) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `COL 11` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `COL 12` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `COL 13` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `sub_estados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sub_estados` (
  `id_sub_est` int unsigned NOT NULL AUTO_INCREMENT,
  `estados_id_estado` int unsigned NOT NULL,
  `desc_sub_est` char(254) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `activo` char(1) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_sub_est`),
  KEY `sub_estados_FKIndex1` (`estados_id_estado`)
) ENGINE=MyISAM AUTO_INCREMENT=28 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `subclientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subclientes` (
  `id_subcli` int unsigned NOT NULL AUTO_INCREMENT,
  `clientes_id_cliente` int unsigned NOT NULL,
  `clientes_cuenta_cliente` int unsigned NOT NULL,
  `nombre_subcli` char(100) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `decuento_subcli` decimal(10,0) DEFAULT NULL,
  `porccomi_subcli` decimal(10,0) DEFAULT NULL,
  `porcquita_subcli` decimal(10,0) DEFAULT NULL,
  `porcact_subcli` decimal(10,0) DEFAULT NULL,
  `plazogestion_subcli` int unsigned DEFAULT NULL,
  `activo_subcli` char(1) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT 'S',
  PRIMARY KEY (`id_subcli`),
  KEY `subclientes_FKIndex1` (`clientes_cuenta_cliente`,`clientes_id_cliente`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `tasas_de_justicia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tasas_de_justicia` (
  `id_tasa` int unsigned NOT NULL AUTO_INCREMENT,
  `nombre` char(20) DEFAULT NULL,
  `valor` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id_tasa`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `telefonos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `telefonos` (
  `id_tel` int unsigned NOT NULL AUTO_INCREMENT,
  `entidades_matricula_ent` char(30) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  `tipo_tel` char(50) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `codigo_area_tel` varchar(50) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `numero_tel` char(150) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `observaciones_tel` char(250) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `activo_tel` char(1) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT 'S',
  PRIMARY KEY (`id_tel`),
  KEY `telefonos_FKIndex1` (`entidades_matricula_ent`)
) ENGINE=MyISAM AUTO_INCREMENT=67816 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `tipo_matricula`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_matricula` (
  `id_tipomatricula` int unsigned NOT NULL AUTO_INCREMENT,
  `detalle_tipomatricula` char(10) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_tipomatricula`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `tmp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tmp` (
  `matricula` char(30) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `cuenta_cliente` char(50) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `cta` int DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id_usuario` int unsigned NOT NULL AUTO_INCREMENT,
  `privilegios_id_privilegio` int unsigned NOT NULL,
  `nom_usuario` char(200) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `cargo_usuario` char(100) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `direccion_usuario` char(254) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `telefono_usuario` char(50) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `mail_usuario` char(254) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `loguin_usuario` char(50) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `pass_usuario` char(254) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  `activo` char(1) CHARACTER SET latin1 COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_usuario`),
  KEY `usuarios_FKIndex1` (`privilegios_id_privilegio`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `vencimientos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vencimientos` (
  `id_vto` int NOT NULL AUTO_INCREMENT,
  `id_cta` int NOT NULL,
  `id_convenio` int NOT NULL,
  `fecha` date NOT NULL,
  `nro_cuota` int NOT NULL,
  `monto` decimal(10,2) DEFAULT NULL,
  `descripcion` varchar(300) NOT NULL,
  `fecha_pago` date NOT NULL,
  `pagado` char(1) DEFAULT 'N',
  PRIMARY KEY (`id_vto`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `wa_conversaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wa_conversaciones` (
  `id_conv` int NOT NULL AUTO_INCREMENT,
  `telefono` varchar(30) NOT NULL,
  `nombre_contacto` varchar(200) DEFAULT NULL,
  `cuentas_id_cta` int DEFAULT NULL,
  `ultimo_mensaje` varchar(500) DEFAULT NULL,
  `ultimo_mensaje_at` datetime DEFAULT NULL,
  `no_leidos` int NOT NULL DEFAULT '0',
  `estado` varchar(20) NOT NULL DEFAULT 'abierta',
  `creado_at` datetime NOT NULL,
  PRIMARY KEY (`id_conv`),
  UNIQUE KEY `uq_wa_conv_telefono` (`telefono`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `wa_envios_masivos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wa_envios_masivos` (
  `id_envio` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `tipo_mensaje` varchar(50) NOT NULL,
  `origen` varchar(10) NOT NULL,
  `total` int NOT NULL DEFAULT '0',
  `enviados` int NOT NULL DEFAULT '0',
  `errores` int NOT NULL DEFAULT '0',
  `descartados_sin_cliente` int NOT NULL DEFAULT '0',
  `descartados_duplicados` int NOT NULL DEFAULT '0',
  `estado` varchar(20) NOT NULL DEFAULT 'pendiente',
  `creado_at` datetime NOT NULL,
  `finalizado_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id_envio`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `wa_mensajes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wa_mensajes` (
  `id_msg` int NOT NULL AUTO_INCREMENT,
  `conversaciones_id_conv` int NOT NULL,
  `direccion` varchar(3) NOT NULL,
  `texto` text,
  `tipo` varchar(20) NOT NULL DEFAULT 'text',
  `media_url` varchar(500) DEFAULT NULL,
  `ycloud_id` varchar(100) DEFAULT NULL,
  `estado` varchar(20) NOT NULL DEFAULT 'pendiente',
  `usuarios_id_usuario` int DEFAULT NULL,
  `creado_at` datetime NOT NULL,
  PRIMARY KEY (`id_msg`),
  KEY `idx_wa_msg_conv` (`conversaciones_id_conv`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 DROP PROCEDURE IF EXISTS `anula_mov` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `anula_mov`(IN `vid_mov` INT)
BEGIN



	update movimientos SET anulado_mov = 'S'



  WHERE id_mov = vid_mov;



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_ALTA_COBRO` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_ALTA_COBRO`(IN `vid_concepto` INT, IN `vid_convenios` INT, IN `vfcha_cobro` DATE, IN `vimporte` DECIMAL(10,2), IN `vrendido` CHAR(1))
BEGIN



	INSERT INTO cobros (



   CONCEPTOS_id_concepto



  ,convenios_id_convenios



  ,fcha_cobro



  ,importe



  ,rendido



) VALUES (



  vid_concepto



  ,vid_convenios



  ,vfcha_cobro



  ,vimporte



  ,vrendido);



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_AM_ACCION` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_AM_ACCION`(IN `vid` INT, IN `vdesc_accion` CHAR(254), IN `vactivo` CHAR(1))
BEGIN







if (vid <> 0) then 



 update acciones SET desc_accion = vdesc_accion WHERE id_accion = vid;



else 



 if (vdesc_accion <> "") then



	insert into acciones (desc_accion,activa) VALUES (vdesc_accion,vactivo);



 end if;



end if; 



 



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_AM_AGENDA` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_AM_AGENDA`(IN `vid_agenda` INT, IN `vid_cta` INT, IN `vdesc_agenda` CHAR(250), IN `vfecha_agenda` DATE, IN `vactivo` CHAR(1), IN `vusuario` INT)
BEGIN



	if (vid_agenda <> 0) then



  



    if (vdesc_agenda <> '') then



     update agenda SET desc_agenda = vdesc_agenda WHERE id_agenda = vid_agenda;



    end if;



    if (vfecha_agenda <> '') then



     update agenda SET fecha_agenda = vfecha_agenda WHERE id_agenda = vid_agenda;



    end if;



    if (vactivo <> '') then



     update agenda SET activo = vactivo WHERE id_agenda = vid_agenda;



    end if;



    if (vusuario <> null) then



     update agenda SET usuarios_id_usuario = vusuario WHERE id_agenda = vid_agenda;



    end if;



  else



    insert into agenda (cuentas_id_cta,desc_agenda,fecha_agenda,activo,usuarios_id_usuario)



    VALUES (vid_cta,vdesc_agenda,vfecha_agenda,vactivo,vusuario);



    



  end if;



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_AM_BOCA_DE_PAGO` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_AM_BOCA_DE_PAGO`(IN `vid_boca_de_pago` INT, IN `vid_cobros` INT, IN `vdesc_boca_de_pago` CHAR(254), IN `vactivo` CHAR(1))
BEGIN



	If ( vid_boca_de_pago <> 0) then



   UPDATE boca_de_pago SET



   cobros_id_cobros = vid_cobros



   ,desc_boca_de_pago = vdesc_boca_de_pago



   ,activo = vactivo



   WHERE id_boca_de_pago = vid_boca_de_pago;



  else



   insert into boca_de_pago (



   cobros_id_cobros



   ,desc_boca_de_pago



   ,activo



   ) VALUES (



   vid_cobros



   ,vdesc_boca_de_pago



   ,vactivo);



  end if;



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_AM_CONCEPTO` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_AM_CONCEPTO`(IN `vid_concepto` INT, IN `vrubro` CHAR(254), IN `vdesc_concepto` CHAR(254), IN `vactivo` CHAR(1))
BEGIN



	If ( vid_concepto <> 0) then



   UPDATE conceptos SET



   rubro = vrubro



   ,desc_concepto = vdesc_concepto



   ,activo = vactivo



   WHERE id_concepto = vid_concepto;



  else



   insert into conceptos (



   rubro



   ,desc_concepto



   ,activo



   ) VALUES (



   vrubro



   ,vdesc_concepto



   ,vactivo);



  end if;



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_AM_CONTACTOS` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_AM_CONTACTOS`(IN `vid_contacto` INT, IN `vid_cta` INT, IN `vid_resultado` INT, IN `vid_accion` INT, IN `vfecha_contacto` DATE, IN `vhora_contacto` CHAR(10), IN `vnota_contacto` CHAR(254), IN `vsubestado` INT, IN `vusuario` INT, IN `vactivo` CHAR(1))
BEGIN



DECLARE vid_estado int;







	if (vid_contacto <> 0) then



   UPDATE contactos SET



   resultados_id_resultado = vid_resultado



   ,acciones_id_accion = vid_accion



   ,nota_contacto = vnota_contacto     



   WHERE id_contacto = vid_contacto;



  else



   insert into contactos (



   cuentas_id_cta



   ,resultados_id_resultado



   ,acciones_id_accion



   ,fecha_contacto



   ,hora_contacto



   ,nota_contacto



   ,usuarios_id_usuario



   ,activo



   ) VALUES (vid_cta



   ,vid_resultado



   ,vid_accion



   ,vfecha_contacto



   ,vhora_contacto



   ,vnota_contacto



   ,vusuario



   ,vactivo



   );



  end if;



  



  if(vsubestado <> null) then



    set vid_estado=(select id_estado FROM estados



    inner join sub_estados on estados.id_estado= sub_estados.estados_id_estado



    where sub_estados.id_sub_est=vsubestado);



  END IF;



  



  update cuentas SET sub_estados_id_sub_est = vsubestado, estados_id_estado=vid_estado 



  WHERE id_cta = vid_cta;



  



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_AM_CONTACTOS_JUDICIALES` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_AM_CONTACTOS_JUDICIALES`(IN `vid_contacto_judicial` INT, IN `vid_cta` INT, IN `vid_resultado` INT, IN `vid_accion` INT, IN `vfecha_contacto` DATE, IN `vhora_contacto` CHAR(10), IN `vnota_contacto` CHAR(254), IN `vsubestado` INT, IN `vusuario` INT, IN `vactivo` CHAR(1))
BEGIN



DECLARE vid_estado int;







	if (vid_contacto_judicial <> 0) then



   UPDATE contactos_judiciales SET



   resultados_id_resultado = vid_resultado



   ,acciones_id_accion = vid_accion



   ,nota_contacto = vnota_contacto     



   WHERE id_contacto_judicial = vid_contacto_judicial;



  else



   insert into contactos_judiciales (



   cuentas_id_cta



   ,resultados_id_resultado



   ,acciones_id_accion



   ,fecha_contacto



   ,hora_contacto



   ,nota_contacto



   ,fecha_inicio_caducidad



   ,usuarios_id_usuario  



   ,activo



   ) VALUES (vid_cta



   ,vid_resultado



   ,vid_accion



   ,vfecha_contacto



   ,vhora_contacto



   ,vnota_contacto



   ,vfecha_contacto



   ,vusuario



   ,vactivo



   );



  END IF;



  



    update demandas set fecha_inicio_caducidad=vfecha_contacto;



  



  if(vsubestado <> null) then



    set vid_estado=(select id_estado FROM estados



    inner join sub_estados on estados.id_estado= sub_estados.estados_id_estado



    where sub_estados.id_sub_est=vsubestado);



  END IF;



  



  update cuentas SET sub_estados_id_sub_est = vsubestado, estados_id_estado=vid_estado 



  WHERE id_cta = vid_cta;



  



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_AM_CONVENIOS` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_AM_CONVENIOS`(IN `vid_cuenta` INT, IN `vid_convenio` INT, IN `vid_propuesta` INT, IN `vfecha_convenio` DATE, IN `vconcepto_convenio` INT, IN `vestado_convenio` INT, IN `vimporte_convenio` DECIMAL(10,2), IN `vanticipo_convenio` DECIMAL(10,2), IN `vcant_cuotas_convenio` INT, IN `vimporte_cuota_convenio` DECIMAL(10,2), IN `vcuotas_pagadas` INT, IN `vsaldo_convenio` DECIMAL(10,2), IN `vobservaciones_convenio` CHAR(254), IN `vactivo` CHAR(1))
BEGIN







	If ( vid_convenio <> 0) then







   update convenios SET







   propuestas_id_propuesta = vid_propuesta







   ,fecha_convenio = vfecha_convenio







   ,concepto_convenio = vconcepto_convenio







   ,estado_convenio = vestado_convenio







   ,importe_convenio = vimporte_convenio







   ,anticipo_convenio = vanticipo_convenio







   ,cant_cuotas_convenio = vcant_cuotas_convenio







   ,importe_cuota_convenio = vimporte_cuota_convenio







   ,cuotas_pagadas = vcuotas_pagadas







   ,saldo_convenio = vsaldo_convenio







   ,observaciones_convenio = vobservaciones_convenio







   ,activo = vactivo







   WHERE id_convenios= vid_convenio;







  else







   insert into convenios (







   cuentas_id_cta,







   propuestas_id_propuesta







   ,fecha_convenio







   ,concepto_convenio







   ,estado_convenio







   ,importe_convenio







   ,anticipo_convenio







   ,cant_cuotas_convenio







   ,importe_cuota_convenio







   ,cuotas_pagadas







   ,saldo_convenio







   ,observaciones_convenio







   ,activo







   ) VALUES (







   vid_cuenta,







   vid_propuesta







   ,vfecha_convenio







   ,vconcepto_convenio







   ,vestado_convenio







   ,vimporte_convenio







   ,vanticipo_convenio







   ,vcant_cuotas_convenio







   ,vimporte_cuota_convenio







   ,vcuotas_pagadas







   ,vsaldo_convenio







   ,vobservaciones_convenio







   ,vactivo);







   







  end if;







END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_AM_CONVENIOS_JUDICIALES` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_AM_CONVENIOS_JUDICIALES`(IN `vid_cuenta` INT, IN `vid_convenio_judicial` INT, IN `vid_propuesta` INT, IN `vfecha_convenio` DATE, IN `vconcepto_convenio` INT, IN `vestado_convenio` INT, IN `vimporte_convenio` DECIMAL(10,2), IN `vanticipo_convenio` DECIMAL(10,2), IN `vcant_cuotas_convenio` INT, IN `vimporte_cuota_convenio` DECIMAL(10,2), IN `vcuotas_pagadas` INT, IN `vsaldo_convenio` DECIMAL(10,2), IN `vobservaciones_convenio` CHAR(254), IN `vactivo` CHAR(1))
BEGIN



	If ( vid_convenio_judicial <> 0) then

  

    UPDATE convenios_judiciales SET

    propuestas_id_propuesta = vid_propuesta

    ,fecha_convenio = vfecha_convenio

    ,concepto_convenio = vconcepto_convenio

    ,estado_convenio = vestado_convenio

    ,importe_convenio = vimporte_convenio

    ,anticipo_convenio = vanticipo_convenio

    ,cant_cuotas_convenio = vcant_cuotas_convenio

    ,importe_cuota_convenio = vimporte_cuota_convenio

    ,cuotas_pagadas = vcuotas_pagadas

    ,saldo_convenio = vsaldo_convenio

    ,observaciones_convenio = vobservaciones_convenio    

  WHERE id_convenios_judiciales = vid_convenio_judicial;



  else



   INSERT INTO convenios_judiciales (

   cuentas_id_cta

  ,propuestas_id_propuesta

  ,fecha_convenio

  ,concepto_convenio

  ,estado_convenio

  ,importe_convenio

  ,anticipo_convenio

  ,cant_cuotas_convenio

  ,importe_cuota_convenio

  ,cuotas_pagadas

  ,saldo_convenio

  ,observaciones_convenio

  ,activo



   ) VALUES (



   vid_cuenta,



   vid_propuesta



   ,vfecha_convenio



   ,vconcepto_convenio



   ,vestado_convenio



   ,vimporte_convenio



   ,vanticipo_convenio



   ,vcant_cuotas_convenio



   ,vimporte_cuota_convenio



   ,vcuotas_pagadas



   ,vsaldo_convenio



   ,vobservaciones_convenio



   ,vactivo);   



  end if;



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_AM_CUENTAS` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_AM_CUENTAS`(IN `vmatricula` CHAR(50), IN `vid_cta` INT, IN `vid_subcli` INT, IN `vcuenta_cliente` CHAR(50), IN `vdeudatrans_cta` DECIMAL(10,2), IN `vdeudaact_cta` DECIMAL(10,2), IN `vfechaingreso_cta` DATE, IN `vfecha_padron_cta` DATE, IN `vfecha_asignacion_cta` DATE, IN `vempleador` CHAR(100), IN `vobservacion` CHAR(250), IN `vjudicial` CHAR(1), IN `vactiva_cta` CHAR(1))
BEGIN



	if (vid_cta <> 0) then



   update cuentas SET



   subclientes_id_subcli = vid_subcli



   ,cuenta_cliente=vcuenta_cliente



   ,deudatrans_cta = vdeudatrans_cta



   ,deudaact_cta = vdeudaact_cta



   ,fechaingreso_cta = vfechaingreso_cta



   ,fecha_padron_cta = vfecha_padron_cta



   ,fecha_asignacion_cta = vfecha_asignacion_cta



   ,observacion_cta = vobservacion



   ,empleador_cta= vempleador



   ,activa_cta = vactiva_cta



   ,judicial= vjudicial



   WHERE id_cta = vid_cta;



  else



   insert into cuentas (



   entidades_matricula_ent,



   subclientes_id_subcli



   ,cuenta_cliente



   ,deudatrans_cta



   ,deudaact_cta



   ,fechaingreso_cta



   ,fecha_padron_cta



   ,fecha_asignacion_cta



   ,empleador_cta



   ,observacion_cta



   ,judicial



   ,activa_cta



   ) VALUES (



   vmatricula



   ,vid_subcli



   ,vcuenta_cliente



   ,vdeudatrans_cta



   ,vdeudaact_cta



   ,vfechaingreso_cta



   ,vfecha_padron_cta



   ,vfecha_asignacion_cta



   ,vempleador



   ,vobservacion



   ,vjudicial



   ,vactiva_cta);



  END IF;



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_AM_DEMANDA` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_AM_DEMANDA`(IN `vdemanda` INT, IN `vcuenta` CHAR(20), IN `vcaratula` CHAR(200), IN `vexpediente` CHAR(200), IN `vsecretarias_id_secretaria` INT, IN `vjuzgados_id_juzgado` INT, IN `vmonto_demanda` DECIMAL(10,2), IN `vapoderado` CHAR(40), IN `vfecha_inicio_demanda` DATE, IN `vfecha_mora` DATE, IN `vfecha_inicio_caducidad` DATE, IN `vactiva` CHAR(1))
BEGIN





if vdemanda = 0 THEN





	INSERT INTO demandas (caratula,expediente,secretarias_id_secretaria,juzgados_id_juzgado,monto_demanda,



apoderado,fecha_inicio_demanda,fecha_mora,fecha_inicio_caducidad,cuentas_id_cta)



VALUES (vcaratula,vexpediente,vsecretarias_id_secretaria,vjuzgados_id_juzgado,vmonto_demanda,vapoderado,



vfecha_inicio_demanda,vfecha_mora,vfecha_inicio_caducidad,vcuenta);



ELSE

  UPDATE demandas SET

  caratula = vcaratula

  ,expediente = vexpediente

  ,secretarias_id_secretaria = vsecretarias_id_secretaria

  ,juzgados_id_juzgado = vjuzgados_id_juzgado

  ,monto_demanda = vmonto_demanda

  ,apoderado = vapoderado

  ,fecha_inicio_demanda = vfecha_inicio_demanda

  ,fecha_mora = vfecha_mora

  ,cuentas_id_cta = vcuenta

  ,fecha_inicio_caducidad = vfecha_inicio_caducidad  

  WHERE id_demanda=vdemanda;

  

END IF;



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_AM_DIRECCIONES` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_AM_DIRECCIONES`(IN `vid_dir` INT, IN `vmatricula` CHAR(50), IN `vcalle_dir` CHAR(254), IN `vnro_dir` INT, IN `vpiso_dir` CHAR(10), IN `vdpto_dir` CHAR(10), IN `vcasa_dir` CHAR(10), IN `vmanzana_dir` CHAR(10), IN `vbarrio_dir` CHAR(50), IN `vCP_dir` CHAR(20), IN `vlocalidad_dir` CHAR(200), IN `vprovincia_dir` CHAR(50), IN `vobservacion_dir` CHAR(250), IN `vtipo_dir` CHAR(50))
BEGIN



IF (vid_dir <> 0) THEN



  UPDATE direcciones SET



  calle_dir = vcalle_dir



  ,nro_dir = vnro_dir



  ,piso_dir = vpiso_dir



  ,dpto_dir = vdpto_dir



  ,casa_dir = vcasa_dir



  ,manzana_dir = vmanzana_dir



  ,barrio_dir = vbarrio_dir



  ,CP_dir = vCP_dir



  ,localidad_dir = vlocalidad_dir



  ,provincia_dir = vprovincia_dir



  ,tipo_dir = vtipo_dir



  ,observacion_dir = vobservacion_dir



  ,activa_dir = 'S'



  WHERE id_dir = vid_dir;



  



 ELSE



  insert into direcciones (



  entidades_matricula_ent



  ,calle_dir



  ,nro_dir



  ,piso_dir



  ,dpto_dir



  ,casa_dir



  ,manzana_dir



  ,barrio_dir



  ,CP_dir



  ,localidad_dir



  ,provincia_dir



  ,activa_dir



  ,tipo_dir



  ,observacion_dir



) VALUES (



  vmatricula



  ,vcalle_dir



  ,vnro_dir



  ,vpiso_dir



  ,vdpto_dir



  ,vcasa_dir



  ,vmanzana_dir



  ,vbarrio_dir



  ,vCP_dir



  ,vlocalidad_dir



  ,vprovincia_dir



  ,'S'



  ,vtipo_dir



  ,vobservacion_dir



);



 END IF;



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_AM_ENTIDADES` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_AM_ENTIDADES`(IN `vexiste` CHAR(2), IN `vtipo_matricula` INT, IN `vcond_iva` INT, IN `vnombre` CHAR(200), IN `vmatricula` CHAR(30), IN `vcontacto` CHAR(20), IN `vactivo` CHAR(1))
BEGIN







if (vexiste = 'NO') THEN



insert into entidades (



   tipo_matricula_id_tipomatricula



  ,condicion_iva_id_cond_iva



  ,razon_social_ent



  ,matricula_ent



  ,contacto_ent



  ,activo_ent



 ) VALUES (



   vtipo_matricula



  ,vcond_iva



  ,vnombre



  ,vmatricula



  ,vcontacto



  ,vactivo



);







END IF;







END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_AM_ESTADO` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_AM_ESTADO`(IN `vid_estado` INT, IN `vid_cta` INT, IN `vdesc_estado` CHAR(254), IN `vtipo_estado` CHAR(50), IN `vactivo` CHAR(1))
BEGIN



	If (vid_estado <> 0) then



   UPDATE estados SET



   cuentas_id_cta = vid_cta



   ,desc_estado = vesc_estado



   ,tipo_estado = vtipo_estado



   ,activo = vactivo



   WHERE id_estado = vid_estado;



  else



   insert into estados (



   cuentas_id_cta



   ,desc_estado



   ,tipo_estado



   ,activo



   ) VALUES (



   vid_cta



   ,vdesc_estado



   ,vtipo_estado



   ,vactivo);



   



  end if;



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_AM_MAIL` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_AM_MAIL`(IN `vid_mails` INT, IN `vmatricula` CHAR(50), IN `vmail` CHAR(250), IN `vtipo_mail` CHAR(50), IN `vactivo_mail` CHAR(1))
BEGIN



	IF (vid_mails <> 0) THEN



   UPDATE mails SET



   entidades_matricula_ent = vmatricula



   ,mail = vmail



   ,tipo_mail = vtipo_mail



   ,activo_mail = vactivo_mail



   WHERE id_mails = id_mails;



  ELSE



   insert into mails (



   entidades_matricula_ent



   ,mail



   ,tipo_mail



   ,activo_mail



   ) VALUES (



   vmatricula



   ,vmail



   ,vtipo_mail



   ,vactivo_mail



);



  END IF;



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_AM_PRIVILEGIOS` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_AM_PRIVILEGIOS`(IN `vid_privilegio` INT, IN `vdesc_privilegio` CHAR(254))
BEGIN



	IF (vid_privilegio <> 0) THEN



   UPDATE privilegios SET



   desc_privilegio = vdesc_privilegio



   WHERE id_privilegio = vid_privilegio;



  ELSE



   INSERT INTO privilegios (



   desc_privilegio



   ) VALUES ( vdesc_privilegio);



  END IF;



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_AM_PRODUCTO` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_AM_PRODUCTO`(IN `vid_prod` INT, IN `vid_cta` INT, IN `vnro_producto` INT, IN `vdesc_producto` CHAR(254), IN `vmoneda_producto` DECIMAL(10,2), IN `vsaldo_prod` DECIMAL(10,2), IN `vactivo` CHAR(1))
BEGIN



	If ( vid_prod <> 0) then



   update productos SET



   cuentas_id_cta = vid_cta



   ,nro_producto = vnro_product



   ,desc_producto = vdesc_producto



   ,moneda_producto = vmoneda_producto



   ,saldo_prod = vsaldo_prod



   ,activo = vactivo



   WHERE id_prod = vid_prod;



  else



   insert into productos (



   cuentas_id_cta



   ,nro_producto



   ,desc_producto



   ,moneda_producto



   ,saldo_prod



   ,activo



   ) VALUES (



   vid_cta



   ,vnro_producto



   ,vdesc_producto



   ,vmoneda_producto



   ,vsaldo_prod



   ,vactivo);



   



  end if;



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_AM_PROPUESTAS` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_AM_PROPUESTAS`(IN `vid_propuesta` INT, IN `vid_contacto` INT, IN `vid_cta` INT, IN `vfecha_propuesta` DATE, IN `vconcepto_propuesta` CHAR(100), IN `vfechavto_propuesta` DATE, IN `vestado_propuesta` CHAR(100), IN `vactiva` CHAR(1))
BEGIN



	If ( vid_propuesta <> 0) then



   UPDATE propuestas SET



   contactos_id_contacto = vid_contacto



   ,cuentas_id_cta = vid_cta



   ,fecha_propuesta = vfecha_propuesta



   ,concepto_propuesta = vconcepto_propuesta



   ,fechavto_propuesta = vfechavto_propuesta



   ,estado_propuesta = vestado_propuesta



   ,activa = vactiva



   WHERE id_propuesta = vid_propuesta;



  else



   insert into propuestas (



   contactos_id_contacto



   ,cuentas_id_cta



   ,fecha_propuesta



   ,concepto_propuesta



   ,fechavto_propuesta



   ,estado_propuesta



   ,activa



   ) VALUES (



   vid_contacto



   ,vid_cta



   ,vfecha_propuesta



   ,vconcepto_propuesta



   ,vfechavto_propuesta



   ,vestado_propuesta



   ,vactiva);



  end if;



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_AM_SUBCLIENTES` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_AM_SUBCLIENTES`(IN `vmatricula` CHAR(50), IN `vid_subcli` INT, IN `vnombre_subcli` CHAR(100), IN `vdecuento_subcli` CHAR(254), IN `vporccomi_subcli` DECIMAL(10,2), IN `vporcquita_subcli` DECIMAL(10,2), IN `vporcact_subcli` DECIMAL(10,2), IN `vplazogestion_subcli` INT, IN `vactivo_subcli` CHAR(1))
BEGIN



	IF (vid_subcli <> 0) THEN



   update subclientes SET



   id_subcli = vid_subcli



   ,entidades_matricula_ent = vmatricula



   ,nombre_subcli = vnombre_subcli



   ,decuento_subcli = vdecuento_subcli



   ,porccomi_subcli = vporccomi_subcli



   ,porcquita_subcli = vporcquita_subcli



   ,porcact_subcli = vporcact_subcli



   ,plazogestion_subcli = vplazogestion_subcli



   ,activo_subcli = vactivo_subcli



   WHERE id_subcli = vid_subcli;



  ELSE



   insert into subclientes (



   entidades_matricula_ent



   ,nombre_subcli



   ,decuento_subcli



   ,porccomi_subcli



   ,porcquita_subcli



   ,porcact_subcli



   ,plazogestion_subcli



   ,activo_subcli



   ) VALUES (vmatricula



   ,vnombre_subcli



   ,vdecuento_subcli



   ,vporccomi_subcli



   ,vporcquita_subcli



   ,vporcact_subcli



   ,vplazogestion_subcli



   ,vactivo_subcli);



  END IF;



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_AM_TELEFONO` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_AM_TELEFONO`(IN `vid_tel` INT, IN `vmatricula` CHAR(50), IN `vtipo_tel` CHAR(50), IN `vcod_area_tel` CHAR(20), IN `vnumero_tel` CHAR(50), IN `vobservaciones` CHAR(250), IN `vactivo` CHAR(1))
BEGIN



	IF (vid_tel <> 0) THEN



   update telefonos SET



    entidades_matricula_ent = vmatricula



    ,tipo_tel = vtipo_tel



    ,codigo_area_tel=vcod_area_tel



    ,numero_tel = vnumero_tel



    ,observaciones_tel= vobservaciones



    ,activo_tel = vactivo



   WHERE id_tel = vid_tel;



  ELSE



   insert into telefonos (



   entidades_matricula_ent



   ,tipo_tel



   ,codigo_area_tel



   ,numero_tel



   ,observaciones_tel



   ,activo_tel



   ) VALUES (



   vmatricula



   ,vtipo_tel



   ,vcod_area_tel



   ,vnumero_tel



   ,vobservaciones



   ,vactivo



   );



  END IF;



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_AM_USUARIO` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_AM_USUARIO`(IN `vid_usuario` INT, IN `vid_privilegio` INT, IN `vnom_usuario` CHAR(200), IN `vcargo_usuario` CHAR(100), IN `vdireccion_usuario` CHAR(254), IN `vtelefono_usuario` CHAR(50), IN `vmail_usuario` CHAR(254), IN `vloguin_usuario` CHAR(50), IN `vpass_usuario` CHAR(254), IN `vactivo` CHAR(1))
BEGIN



	IF (vid_usuario <> 0) THEN



   UPDATE usuarios SET



   privilegios_id_privilegio = vid_privilegio



   ,nom_usuario = vnom_usuario



   ,cargo_usuario = vcargo_usuario



   ,direccion_usuario = vdireccion_usuario



   ,telefono_usuario = vtelefono_usuario



   ,mail_usuario = vmail_usuario



   ,loguin_usuario = vloguin_usuario



   ,pass_usuario = vpass_usuario



   ,activo = vactivo



   WHERE id_usuario = vid_usuario;



  ELSE



   INSERT INTO usuarios (



   privilegios_id_privilegio



   ,nom_usuario



   ,cargo_usuario



   ,direccion_usuario



   ,telefono_usuario



   ,mail_usuario



   ,loguin_usuario



   ,pass_usuario



   ,activo



   ) VALUES (



   vid_privilegio



   ,vnom_usuario



   ,vcargo_usuario



   ,vdireccion_usuario



   ,vtelefono_usuario



   ,vmail_usuario



   ,vloguin_usuario



   ,vpass_usuario



   ,vactivo);



  END IF;



  



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_ANULA_COBRO` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_ANULA_COBRO`(IN `vid_mov` INT)
BEGIN



DECLARE vid_convenio int;



DECLARE vid_cobro int;



DECLARE vimporte decimal(10,2);







 if(vid_mov<>'') then



	#Se reestablece el importe cobrado y se elimina el cobro



  SET vid_convenio=(select convenios.id_convenios



                    FROM cobros inner join convenios on convenios.id_convenios= cobros.convenios_id_convenios



                    where cobros.movimientos_id_mov=vid_mov and cobros.rendido='N' and convenios.activo='S'



                    );



  SET vid_cobro=(select cobros.id_cobros



                 FROM cobros inner join convenios on convenios.id_convenios= cobros.convenios_id_convenios



                 where cobros.movimientos_id_mov=vid_mov and cobros.rendido='N' and convenios.activo='S'



                 );                  



  SET vimporte= (select importe FROM cobros inner join convenios 



                 on convenios.id_convenios= cobros.convenios_id_convenios



                 where cobros.movimientos_id_mov=vid_mov and cobros.rendido='N' and convenios.activo='S'



                 );







  UPDATE convenios SET cuotas_pagadas = (cuotas_pagadas + 1),saldo_convenio = (saldo_convenio + vimporte)



  WHERE id_convenios = vid_convenio;



  



  delete from cobros where id_cobros=vid_cobro;



  



  #Se anula el movimiento  



    UPDATE movimientos SET anulado_mov = 'S' WHERE id_mov = vid_mov;



    



  END IF;



  



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_ASIGNAR_CTA_MASIVA` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_ASIGNAR_CTA_MASIVA`(IN `vusuario` INT)
BEGIN



	if(vusuario <> '') then



   UPDATE cuentas, ctas_tmp SET ejecutivo = vusuario



   WHERE cuentas.id_cta = ctas_tmp.cuenta; 



   delete from ctas_tmp;



  end if;



  



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_CARGA_GASTO` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_CARGA_GASTO`(IN `vid_mov` INT, IN `vfcha_gasto` DATE, IN `vdesc_gasto` CHAR(254), IN `vimporte_gasto` DECIMAL(10,2), IN `vactivo` CHAR(1))
BEGIN



	insert into gastos (



  movimientos_id_mov



  ,fcha_gasto



  ,desc_gasto



  ,importe_gasto



  ,activo



) VALUES (



   vid_mov



  ,vfcha_gasto



  ,vdesc_gasto



  ,vimporte_gasto



  ,vactivo



);



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_CARGA_GASTO_JUDICIAL` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_CARGA_GASTO_JUDICIAL`(IN `vbono_profesional` DECIMAL(10,2), IN `vtasa_judial` INT, IN `vmonto_tasa_judial` DECIMAL(10,2), IN `vplanilla_fiscal` DECIMAL(10,2), IN `vmovilidad` DECIMAL(10,2), IN `vfotocopias` DECIMAL(10,2), IN `vsellado` DECIMAL(10,2), IN `vdiligencias` DECIMAL(10,2), IN `votros` DECIMAL(10,2), IN `vobservaciones` CHAR(250), IN `vcuentas_id_cta` INT, IN `vfecha` DATE)
BEGIN



	INSERT INTO gastos_judiciales (



   bono_profesional



  ,tasa_judicial

  

  ,monto_tasa_judicial



  ,planilla_fiscal



  ,movilidad



  ,fotocopias



  ,sellado



  ,diligencias



  ,otros



  ,observaciones



  ,cuentas_id_cta



  ,fecha



) VALUES (vbono_profesional



  ,vtasa_judial

  ,vmonto_tasa_judial



  ,vplanilla_fiscal



  ,vmovilidad



  ,vfotocopias



  ,vsellado



  ,vdiligencias



  ,votros



  ,vobservaciones



  ,vcuentas_id_cta



  ,vfecha



);



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_CARGA_MASIVA_CTAS` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_CARGA_MASIVA_CTAS`()
BEGIN







DECLARE ent_rep DOUBLE DEFAULT 0;



DECLARE cta_rep DOUBLE DEFAULT 0;







#FORMATEO FECHA PARA CARGAR



update carga_masiva_ctas set fecha_asignacion= CONCAT(SUBSTRING(fecha_asignacion,7,4),'-',SUBSTRING(fecha_asignacion,4,2),'-',SUBSTRING(fecha_asignacion,1,2)),







                               fecha_deuda= CONCAT(SUBSTRING(fecha_deuda,7,4),'-',SUBSTRING(fecha_deuda,4,2),'-',SUBSTRING(fecha_deuda,1,2)),



                               ent_actualizada='N',cta_actualzada='N';







#CHEQUEO SI YA EXISTE LA ENTIDAD



set ent_rep= (SELECT COUNT(matricula_ent) FROM entidades INNER JOIN carga_masiva_ctas







           ON carga_masiva_ctas.matricula= entidades.matricula_ent 



           );















#ACTUALIZA ENTIDADES EXISTENTES







if(ent_rep > 0) then  







  UPDATE entidades, carga_masiva_ctas SET







       razon_social_ent = carga_masiva_ctas.nombre







       ,contacto_ent = carga_masiva_ctas.contacto







       ,carga_masiva_ctas.ent_actualizada = 'S'







  WHERE matricula_ent =  carga_masiva_ctas.matricula;  



END IF;



   #CARGA ENTDADES NUEVAS







 INSERT INTO entidades (razon_social_ent,matricula_ent,contacto_ent) 



 SELECT nombre, matricula,contacto FROM carga_masiva_ctas where ent_actualizada='N' group by matricula;           















#CHEQUEO SI YA EXISTE LA CUENTA



set cta_rep= (SELECT COUNT(carga_masiva_ctas.cuenta_cliente) FROM cuentas INNER JOIN carga_masiva_ctas



           ON (BINARY carga_masiva_ctas.cuenta_cliente = BINARY cuentas.cuenta_cliente) AND (carga_masiva_ctas.matricula= cuentas.entidades_matricula_ent AND carga_masiva_ctas.id_sub_cliente= cuentas.subclientes_id_subcli)



           );







if(cta_rep > 0) then  







#ACTUALIZA CTAS EXISTENTES



  UPDATE cuentas, carga_masiva_ctas SET 







  deudatrans_cta = carga_masiva_ctas.monto_deuda







  ,empleador_cta = carga_masiva_ctas.empleador







  ,observacion_cta = carga_masiva_ctas.observacion







  ,fecha_asignacion_cta= carga_masiva_ctas.fecha_asignacion







  ,fecha_padron_cta= carga_masiva_ctas.fecha_deuda

  

  ,subclientes_id_subcli = carga_masiva_ctas.id_sub_cliente







  ,carga_masiva_ctas.cta_actualzada = 'S'







  WHERE (BINARY carga_masiva_ctas.cuenta_cliente = BINARY cuentas.cuenta_cliente) AND (carga_masiva_ctas.matricula= cuentas.entidades_matricula_ent AND carga_masiva_ctas.id_sub_cliente= cuentas.subclientes_id_subcli); 



END IF;



  #CARGA CUENTAS NUEVAS







 INSERT INTO cuentas (entidades_matricula_ent,cuentas.cuenta_cliente,subclientes_id_subcli,deudatrans_cta,







                      fechaingreso_cta,fecha_padron_cta,fecha_asignacion_cta,empleador_cta,observacion_cta)







        SELECT matricula,cuenta_cliente,id_sub_cliente,monto_deuda,NOW(),fecha_deuda,fecha_asignacion,







        empleador,observacion FROM carga_masiva_ctas WHERE cta_actualzada='N' group by cuenta_cliente;



        











 #SE BORRAN LOS DATOS DE LA TABLA DE CARGA







 DELETE FROM carga_masiva_ctas;







END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_CARGA_MASIVA_DEMANDAS` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_CARGA_MASIVA_DEMANDAS`()
BEGIN







DECLARE ent_rep DOUBLE DEFAULT 0;



DECLARE cta_rep DOUBLE DEFAULT 0;



DECLARE demanda_rep DOUBLE DEFAULT 0;





#FORMATEO FECHA PARA CARGAR



update carga_masiva_demandas set fecha_asignacion= CONCAT(SUBSTRING(fecha_asignacion,7,4),'-',SUBSTRING(fecha_asignacion,4,2),'-',SUBSTRING(fecha_asignacion,1,2)),

                                 fecha_mora= CONCAT(SUBSTRING(fecha_mora,7,4),'-',SUBSTRING(fecha_mora,4,2),'-',SUBSTRING(fecha_mora,1,2)),  

                                 fecha_deuda= CONCAT(SUBSTRING(fecha_deuda,7,4),'-',SUBSTRING(fecha_deuda,4,2),'-',SUBSTRING(fecha_deuda,1,2)),

                                 fecha_inicio_demanda= CONCAT(SUBSTRING(fecha_inicio_demanda,7,4),'-',SUBSTRING(fecha_inicio_demanda,4,2),'-',SUBSTRING(fecha_inicio_demanda,1,2)),

                                 fecha_inicio_caducidad= CONCAT(SUBSTRING(fecha_inicio_caducidad,7,4),'-',SUBSTRING(fecha_inicio_caducidad,4,2),'-',SUBSTRING(fecha_inicio_caducidad,1,2)),

                                 ent_actualizada='N',cta_actualzada='N',demanda_actualizada='N';



#CARGA DE ID_CTA EN TABLA MASIVA DE DEMANDAS

UPDATE cuentas, carga_masiva_demandas SET

  carga_masiva_demandas.id_cuenta = cuentas.id_cta

WHERE (cuentas.entidades_matricula_ent =  carga_masiva_demandas.matricula) and (cuentas.activa_cta='S') and (BINARY carga_masiva_demandas.cuenta_cliente = BINARY cuentas.cuenta_cliente);  



#CHEQUEO SI YA EXISTE LA ENTIDAD



set ent_rep= (SELECT COUNT(matricula_ent) FROM entidades INNER JOIN carga_masiva_demandas

               ON carga_masiva_demandas.matricula= entidades.matricula_ent);



#ACTUALIZA ENTIDADES EXISTENTES



if(ent_rep > 0) then  



  UPDATE entidades, carga_masiva_demandas SET

  razon_social_ent = carga_masiva_demandas.nombre

  ,carga_masiva_demandas.ent_actualizada = 'S'

  WHERE matricula_ent =  carga_masiva_demandas.matricula;  



END IF;



   #CARGA ENTDADES NUEVAS



 INSERT INTO entidades (razon_social_ent,matricula_ent) 

 SELECT nombre, matricula FROM carga_masiva_demandas 

 where ent_actualizada='N' group by matricula;           



#CHEQUEO SI YA EXISTE LA CUENTA



set cta_rep= (SELECT COUNT(carga_masiva_demandas.cuenta_cliente) 

FROM cuentas INNER JOIN carga_masiva_demandas

ON (BINARY carga_masiva_demandas.cuenta_cliente = BINARY cuentas.cuenta_cliente) AND (carga_masiva_demandas.matricula= cuentas.entidades_matricula_ent AND carga_masiva_demandas.id_sub_cliente= cuentas.subclientes_id_subcli));



#CONTROLO CTAS EXISTENTES

if(cta_rep > 0) then  



  UPDATE cuentas, carga_masiva_demandas SET 

  carga_masiva_demandas.cta_actualzada = 'S',

  cuentas.judicial = 'S'

WHERE (BINARY carga_masiva_demandas.cuenta_cliente = BINARY cuentas.cuenta_cliente) AND (carga_masiva_demandas.matricula= cuentas.entidades_matricula_ent AND carga_masiva_demandas.id_sub_cliente= cuentas.subclientes_id_subcli); 



UPDATE cuentas, carga_masiva_demandas SET 

   cuentas.deudatrans_cta = carga_masiva_demandas.monto_deuda

  WHERE (BINARY carga_masiva_demandas.cuenta_cliente = BINARY cuentas.cuenta_cliente) AND (carga_masiva_demandas.matricula= cuentas.entidades_matricula_ent AND carga_masiva_demandas.id_sub_cliente= cuentas.subclientes_id_subcli) and (carga_masiva_demandas.monto_deuda IS NOT NULL); 

  

UPDATE cuentas, carga_masiva_demandas SET 

   cuentas.fecha_asignacion_cta = carga_masiva_demandas.fecha_asignacion

WHERE (BINARY carga_masiva_demandas.cuenta_cliente = BINARY cuentas.cuenta_cliente) AND (carga_masiva_demandas.matricula= cuentas.entidades_matricula_ent AND carga_masiva_demandas.id_sub_cliente= cuentas.subclientes_id_subcli) and (carga_masiva_demandas.fecha_asignacion IS NOT NULL); 



UPDATE cuentas, carga_masiva_demandas SET 

   cuentas.fecha_padron_cta = carga_masiva_demandas.fecha_mora

WHERE (BINARY carga_masiva_demandas.cuenta_cliente = BINARY cuentas.cuenta_cliente) AND (carga_masiva_demandas.matricula= cuentas.entidades_matricula_ent AND carga_masiva_demandas.id_sub_cliente= cuentas.subclientes_id_subcli) and (carga_masiva_demandas.fecha_mora IS NOT NULL); 



UPDATE cuentas, carga_masiva_demandas SET 

   cuentas.empleador_cta = carga_masiva_demandas.empleador

WHERE (BINARY carga_masiva_demandas.cuenta_cliente = BINARY cuentas.cuenta_cliente) AND (carga_masiva_demandas.matricula= cuentas.entidades_matricula_ent AND carga_masiva_demandas.id_sub_cliente= cuentas.subclientes_id_subcli) and (carga_masiva_demandas.empleador IS NOT NULL); 



UPDATE cuentas, carga_masiva_demandas SET 

   cuentas.observacion_cta = carga_masiva_demandas.observacion

WHERE (BINARY carga_masiva_demandas.cuenta_cliente = BINARY cuentas.cuenta_cliente) AND (carga_masiva_demandas.matricula= cuentas.entidades_matricula_ent AND carga_masiva_demandas.id_sub_cliente= cuentas.subclientes_id_subcli) and (carga_masiva_demandas.observacion IS NOT NULL); 





END IF;



  #CARGA CUENTAS NUEVAS



 INSERT INTO cuentas (entidades_matricula_ent,cuentas.cuenta_cliente,subclientes_id_subcli,deudatrans_cta,

 fechaingreso_cta,fecha_padron_cta,fecha_asignacion_cta,empleador_cta,observacion_cta,judicial)

 SELECT matricula,cuenta_cliente,id_sub_cliente,monto_deuda,NOW(),fecha_deuda,fecha_asignacion,empleador,observacion, 'S' 

 FROM carga_masiva_demandas 

 WHERE cta_actualzada='N' group by cuenta_cliente;



  #CONTROLO SI EXISTEN LAS DEMANDAS

  

  set demanda_rep= (SELECT COUNT(carga_masiva_demandas.expediente) 

FROM demandas INNER JOIN carga_masiva_demandas

ON (carga_masiva_demandas.expediente = demandas.expediente) AND (carga_masiva_demandas.id_cuenta= demandas.cuentas_id_cta)); 



  if(demanda_rep > 0) then  



  UPDATE demandas, carga_masiva_demandas SET 

  carga_masiva_demandas.demanda_actualizada = 'S'

  WHERE (carga_masiva_demandas.expediente = demandas.expediente) AND (carga_masiva_demandas.id_cuenta= demandas.cuentas_id_cta); 

  

  UPDATE demandas, carga_masiva_demandas SET 

  demandas.apoderado = carga_masiva_demandas.apoderado

  WHERE (carga_masiva_demandas.apoderado is NOT NULL); 

  

  UPDATE demandas, carga_masiva_demandas SET 

  demandas.caratula = carga_masiva_demandas.caratula

  WHERE (carga_masiva_demandas.caratula is NOT NULL); 

  

  UPDATE demandas, carga_masiva_demandas SET 

  demandas.secretarias_id_secretaria = carga_masiva_demandas.secretaria

  WHERE (carga_masiva_demandas.secretaria is NOT NULL); 

  

  UPDATE demandas, carga_masiva_demandas SET 

  demandas.juzgados_id_juzgado = carga_masiva_demandas.juzgado

  WHERE (carga_masiva_demandas.juzgado is NOT NULL); 



END IF;



  #CARGA DE DEMANDAS

  

insert into demandas (caratula,expediente,secretarias_id_secretaria,

juzgados_id_juzgado,monto_demanda,apoderado,fecha_inicio_demanda,

fecha_mora,cuentas_id_cta,fecha_inicio_caducidad,activa

) select caratula, expediente, secretaria, juzgado,

monto_demanda, apoderado, fecha_inicio_demanda, fecha_mora, 

id_cuenta,fecha_inicio_caducidad, 'S'

FROM carga_masiva_demandas

WHERE demanda_actualizada='N' group by cuenta_cliente;

  

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_CARGA_MASIVA_DIR_TEL_MAIL` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_CARGA_MASIVA_DIR_TEL_MAIL`()
BEGIN



	DECLARE cant_dir DOUBLE DEFAULT 0;



  DECLARE cant_tel DOUBLE DEFAULT 0;



  DECLARE cant_mail DOUBLE DEFAULT 0;







set cant_dir= (SELECT COUNT(entidades_matricula_ent) FROM direcciones INNER JOIN carga_masiva_dir



ON carga_masiva_dir.tipo_dir= direcciones.tipo_dir AND carga_masiva_dir.matricula= direcciones.entidades_matricula_ent);







#ACTUALIZA DIRECCIONES EXISTENTES



if(cant_dir > 0) then  



  



  update direcciones,carga_masiva_dir SET



  direcciones.calle_dir = carga_masiva_dir.calle_dir



  ,direcciones.nro_dir = carga_masiva_dir.nro_dir



  ,direcciones.piso_dir = carga_masiva_dir.piso_dir



  ,direcciones.dpto_dir = carga_masiva_dir.dpto_dir



  ,direcciones.casa_dir = carga_masiva_dir.casa_dir



  ,direcciones.manzana_dir = carga_masiva_dir.manzana_dir



  ,direcciones.barrio_dir = carga_masiva_dir.barrio_dir



  ,direcciones.CP_dir = carga_masiva_dir.CP_dir



  ,direcciones.localidad_dir = carga_masiva_dir.localidad_dir



  ,direcciones.departamento_dir = carga_masiva_dir.departamento_dir



  ,direcciones.provincia_dir = carga_masiva_dir.provincia_dir



  ,direcciones.seccional_dir = carga_masiva_dir.seccional_dir



  ,direcciones.tipo_dir = carga_masiva_dir.tipo_dir



  ,direcciones.observacion_dir = carga_masiva_dir.observacion_dir



  ,carga_masiva_dir.dir_actualizada= 'S'  



  WHERE carga_masiva_dir.matricula=direcciones.entidades_matricula_ent and direcciones.tipo_dir= carga_masiva_dir.tipo_dir;



   



 END IF;



 



 #CARGA DIRECCIONES NUEVAS



INSERT INTO direcciones (entidades_matricula_ent,calle_dir,nro_dir,piso_dir,dpto_dir,casa_dir,



manzana_dir,barrio_dir,CP_dir,localidad_dir,departamento_dir,provincia_dir,seccional_dir,tipo_dir,



observacion_dir)



SELECT matricula, calle_dir, nro_dir, piso_dir, dpto_dir, casa_dir, manzana_dir, barrio_dir,



CP_dir, localidad_dir, departamento_dir, provincia_dir, seccional_dir, tipo_dir, observacion_dir



FROM carga_masiva_dir WHERE dir_actualizada='N';



  



  #SE BORRAN LOS DATOS DE LA TABLA DE CARGA



  DELETE FROM carga_masiva_dir;



#-------------------------------------------------------------------------------------------------







  #CARGA MASIVA DE TELEFONOS



  SET cant_tel= (SELECT COUNT(entidades_matricula_ent) FROM telefonos INNER JOIN carga_masiva_tel



  ON telefonos.entidades_matricula_ent= carga_masiva_tel.matricula AND carga_masiva_tel.tipo= telefonos.tipo_tel);







  if(cant_tel > 0) THEN



   UPDATE telefonos,carga_masiva_tel SET 



   codigo_area_tel = carga_masiva_tel.codigo_area



   ,telefonos.numero_tel = carga_masiva_tel.numero_tel



   ,telefonos.observaciones_tel = carga_masiva_tel.observaciones



   ,carga_masiva_tel.tel_actualizado='S'



   WHERE entidades_matricula_ent = carga_masiva_tel.matricula and telefonos.tipo_tel= carga_masiva_tel.tipo;



  END IF;



  



  insert into telefonos (entidades_matricula_ent,tipo_tel,codigo_area_tel,numero_tel,observaciones_tel)



  select matricula, tipo, codigo_area, numero_tel, observaciones FROM carga_masiva_tel where tel_actualizado='N';



  



  #BLANQUEAR TABLA DE CARGA DE TELEFONOS



  DELETE FROM carga_masiva_tel;



  



#----------------------------------------------------------------------------------------------------------------







#CARGA MASIVA DE MAILS







SET cant_mail = (select COUNT(entidades_matricula_ent) FROM mails inner join carga_masiva_mails



on carga_masiva_mails.matricula= mails.entidades_matricula_ent and carga_masiva_mails.tipo_mail= mails.tipo_mail);







IF (cant_mail > 0) THEN



#ACTUALIZA MAILS CARGADOS



 UPDATE mails, carga_masiva_mails SET



   mails.mail = carga_masiva_mails.mail,



   carga_masiva_mails.mail_actualizado= 'S'



 WHERE carga_masiva_mails.tipo_mail= mails.tipo_mail and carga_masiva_mails.matricula= mails.entidades_matricula_ent;



END IF;







#SE INSERTA LOS NUEVOS MAILS



INSERT INTO mails (entidades_matricula_ent,mail,tipo_mail)



SELECT matricula, mail, tipo_mail FROM carga_masiva_mails WHERE mail_actualizado='N';



  



#SE LIMPIA LA TABLA DE CARGA DE MAIL



DELETE FROM carga_masiva_mails;



#---------------------------------------------------------------------------------------







END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_COND_IVA` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_COND_IVA`(IN `vid_cond_iva` INT, IN `vdetalle` CHAR(254), IN `vporcentaje` DECIMAL(10,2))
BEGIN



	if(id_cond_iva <> 0) then



   update condicion_iva SET



   detalle = vdetalle



   ,porcentaje = vporcentaje



   WHERE id_cond_iva = vid_cond_iva;



  else



   insert into condicion_iva (



   detalle



   ,porcentaje



   ) VALUES (



   vdetalle



   ,vporcentaje); 







end if;



  



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_GASTO` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_GASTO`(IN `vfcha_gasto` DATE, IN `vdesc_gasto` CHAR(250), IN `vimporte_gasto` DECIMAL(10,2), IN `vactivo` CHAR(1))
BEGIN







call sp_mov(0,vimporte_gasto,vfcha_gasto,vdesc_gasto,'N',vid_mov); #vid_mov es un parametro de salida del SP







	INSERT INTO gastos (



   movimientos_id_mov



  ,fcha_gasto



  ,desc_gasto



  ,importe_gasto



  ,activo



) VALUES (



   vid_mov



  ,vfcha_gasto



  ,vdesc_gasto



  ,vimporte_gasto



  ,vactivo



);



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_MOV` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_MOV`(IN `vimporte_ingreso_mov` DECIMAL(10,2), IN `vimporte_egreso_mov` DECIMAL(10,2), IN `vfecha_mov` DATE, IN `vdesc_mov` CHAR(254), IN `vanulado_mov` CHAR(1))
BEGIN



	INSERT INTO movimientos (



  importe_ingreso_mov



  ,importe_egreso_mov



  ,fecha_mov



  ,desc_mov



  ,anulado_mov



  ) VALUES (



  vimporte_ingreso_mov



  ,vimporte_egreso_mov



  ,vfecha_mov



  ,vdesc_mov



  ,vanulado_mov



);







END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_PAGO_COMISIONES` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_PAGO_COMISIONES`(IN `vid_subcli` INT, IN `vimporte_comision` DECIMAL(10,2), IN `vfecha_pago_comision` DATE, IN `vmes_de_comision` CHAR(20))
BEGIN







call sp_mov(vimporte,0,vfecha_pago_comision,'PAGO COMISION','N',vid_mov); #vid_mov es un parametro de salida del SP







	INSERT INTO pago_comisiones (



  movimientos_id_mov



  ,subclientes_id_subcli



  ,importe_comision



  ,fecha_pago_comision



  ,mes_de_comision



) VALUES (



  vid_mov



  ,vid_subcli



  ,vimporte_comision



  ,vfecha_pago_comision



  ,vmes_de_comision



);



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_PAGO_EFECTIVO` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_PAGO_EFECTIVO`(IN `vid_concepto` INT, IN `vconcepto_cobro` INT, IN `vid_cta` INT, IN `vid_convenios` INT, IN `vfecha_cobro` DATE, IN `vdesc_cobro` CHAR(250), IN `vcuota` INT, IN `vimporte` DECIMAL(10,2), IN `vrendido` CHAR(1), IN `vsaldo` DECIMAL(10,2), IN `vimporte_total_conv` DECIMAL(10,2), IN `vcant_ctas` INT, IN `vctas_pagadas` INT)
BEGIN



DECLARE vid_mov int;



DECLARE vconcepto char(30);







call sp_mov(vimporte,0,vfecha_cobro,vdesc_cobro,'N');



set vid_mov = (select MAX(id_mov) from movimientos);















	insert into cobros (



   movimientos_id_mov



  ,CONCEPTOS_id_concepto

  

  ,concepto_cobro



  ,cuentas_id_cta



  ,convenios_id_convenios



  ,fcha_cobro



  ,desc_cobro



  ,cuota



  ,importe



  ,rendido



) VALUES (



  vid_mov



  ,vid_concepto

  

  ,vconcepto_cobro



  ,vid_cta



  ,vid_convenios



  ,vfecha_cobro



  ,vdesc_cobro



  ,vcuota



  ,vimporte



  ,vrendido



);







 



 if(vsaldo <> vimporte_total_conv) THEN



 



  UPDATE convenios SET cuotas_pagadas = (cuotas_pagadas + 1),



          saldo_convenio = (saldo_convenio-vimporte)



  WHERE id_convenios = vid_convenios;



 ELSE 



  if(vsaldo = vimporte_total_conv) THEN 



    UPDATE convenios SET  saldo_convenio = (saldo_convenio-vimporte)



    WHERE id_convenios = vid_convenios;



  END IF;



 



 END IF;



 



 if(vcant_ctas = vctas_pagadas) THEN



   UPDATE convenios SET  cancelado = 'S' WHERE id_convenios = vid_convenios;



 END IF;



 



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_PAGO_JUDICIAL` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_PAGO_JUDICIAL`(IN `vid_concepto` INT, IN `vconcepto_cobro` INT, IN `vid_cta` INT, IN `vid_convenios` INT, IN `vfecha_cobro` DATE, IN `vdesc_cobro` CHAR(250), IN `vcuota` INT, IN `vimporte` DECIMAL(10,2), IN `vrendido` CHAR(1), IN `vsaldo` DECIMAL(10,2), IN `vimporte_total_conv` DECIMAL(10,2), IN `vcant_ctas` INT, IN `vctas_pagadas` INT, IN `vgastos_pendientes` DECIMAL(10,2))
BEGIN



DECLARE vid_mov int;



DECLARE vcancela char(1);







call sp_mov(vimporte,0,vfecha_cobro,vdesc_cobro,'N');



set vid_mov = (select MAX(id_mov) from movimientos);





if(vgastos_pendientes = vimporte) THEN



 SET vcancela = 'S';



ELSE



  SET vcancela = 'N';



END IF;



  insert into pagos_judiciales (

   importe

  ,detalle

  ,gastos_pendientes

  ,fecha

  ,cuentas_id_cta

  ,id_mov

  ,id_concepto

  ,concepto_cobro

  ,cuota

) VALUES (

   vimporte

  ,vdesc_cobro

  ,vgastos_pendientes

  ,vfecha_cobro

  ,vid_cta

  ,vid_mov

  ,vid_concepto

  ,vconcepto_cobro

  ,vcuota);

  

  if(vsaldo <> vimporte_total_conv) THEN

    UPDATE convenios_judiciales SET cuotas_pagadas = (cuotas_pagadas + 1),

          saldo_convenio = (saldo_convenio-vimporte)

    WHERE id_convenios_judiciales = vid_convenios;

  ELSE 

    if(vsaldo = vimporte_total_conv) THEN

      UPDATE convenios SET  saldo_convenio = (saldo_convenio-vimporte)

      WHERE id_convenios = vid_convenios;

    END IF; 

  END IF; 



  if(vcant_ctas = vctas_pagadas) THEN

    UPDATE convenios_judiciales SET  cancelado = 'S' WHERE id_convenios_judiciales = vid_convenios;

  END IF;

  

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_RENDIR_PAGO` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_RENDIR_PAGO`(IN `vid_subcli` INT, IN `vid_cobros` INT, IN `vfecha_rendido` DATE, IN `vimporte_rendido` DECIMAL(10,2), IN `vperiodo_rendido` CHAR(50))
BEGIN







call sp_mov(0,vimporte_rendido,vfecha_rendido,'RENDICI?N','N',vid_mov); #vid_mov es un parametro de salida del SP







	INSERT INTO rendidos (



   movimientos_id_mov



  ,subclientes_id_subcli



  ,cobros_id_cobros



  ,fecha_rendido



  ,importe_rendido



  ,periodo_rendido



) VALUES (



  vid_mov



  ,vid_subcli



  ,vid_cobros



  ,vfecha_rendido



  ,vimporte_rendido



  ,vperiodo_rendido



);







update cobros SET rendido = 'S' WHERE id_cobros = vid_cobros;







END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_TIPO_MAT` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_unicode_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
CREATE DEFINER=`mng`@`%` PROCEDURE `SP_TIPO_MAT`(IN `vid_tipomatricula` INT, IN `detalle_tipomatricula` CHAR(254))
BEGIN



 if (vid_tipomatricula <> 0) then



  UPDATE tipo_matricula SET



  id_tipomatricula = vid_tipomatricula



  ,detalle_tipomatricula = vdetalle_tipomatricula 



  WHERE id_tipomatricula = vid_tipomatricula;



 else



  insert into tipo_matricula (



  detalle_tipomatricula



  ) VALUES (vdetalle_tipomatricula);



  



 end if;



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;


-- Modificaciones rápidas al dump original para habilitar caducidad en productos
-- Añade la columna 'caducidad' a la tabla ventas_producto y actualiza el producto id=1
-- Fecha generada automáticamente para que aparezca en el rango de 7 días (ajusta si es necesario)

ALTER TABLE `ventas_producto`
  ADD COLUMN `caducidad` DATE DEFAULT NULL;

-- Actualiza el producto existente (id=1) con una fecha de caducidad cercana
UPDATE `ventas_producto` SET `caducidad` = '2025-12-14' WHERE `id` = 1;

-- Si la tabla no existe (importando en una base vacía), crea la columna al crear la tabla
-- A continuación se muestra la definición completa alternativa para crear la tabla con caducidad:
--
-- DROP TABLE IF EXISTS `ventas_producto`;
-- CREATE TABLE IF NOT EXISTS `ventas_producto` (
--   `id` bigint NOT NULL AUTO_INCREMENT,
--   `nombre` varchar(100) NOT NULL,
--   `precio` decimal(10,2) NOT NULL,
--   `stock` int UNSIGNED NOT NULL,
--   `categoria` varchar(20) NOT NULL,
--   `imagen` varchar(100) DEFAULT NULL,
--   `caducidad` date DEFAULT NULL,
--   PRIMARY KEY (`id`)
-- ) ;

COMMIT;

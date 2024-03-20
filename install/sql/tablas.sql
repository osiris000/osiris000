#SQL Tables


#Tabla para articulos

CREATE TABLE `edit_files` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT(10) NOT NULL,
  `file_id` VARCHAR(64) NOT NULL,
  `filecode` VARCHAR(128) NOT NULL,
  `format` VARCHAR(6) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
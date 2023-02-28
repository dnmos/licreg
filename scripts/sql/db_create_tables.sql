-- CREATE TABLE IF NOT EXISTS `federal_area` (
--   `id` INT NOT NULL AUTO_INCREMENT,
--   `name` VARCHAR(96) NOT NULL,
--   `created_at` TIMESTAMP DEFAULT current_timestamp NOT NULL,
--   PRIMARY KEY (`id`),
--   constraint `uc_name` unique (`name`) 
-- )
-- ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- CREATE TABLE IF NOT EXISTS `license_status` (
--   `id` INT NOT NULL AUTO_INCREMENT,
--   `name` VARCHAR(48) NOT NULL,
--   `created_at` TIMESTAMP DEFAULT current_timestamp NOT NULL,
--   PRIMARY KEY (`id`),
--   constraint `uc_name` unique (`name`) 
-- )
-- ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

CREATE TABLE IF NOT EXISTS `plot_status` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP DEFAULT current_timestamp NOT NULL,
  PRIMARY KEY (`id`),
  constraint `uc_name` unique (`name`) 
)
ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

CREATE TABLE IF NOT EXISTS `russian_regions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(96) NOT NULL,
  `created_at` TIMESTAMP DEFAULT current_timestamp NOT NULL,
  PRIMARY KEY (`id`),
  constraint `uc_name` unique (`name`) 
)
ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

CREATE TABLE IF NOT EXISTS `type_of_minerals` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(2048) NOT NULL,
  `created_at` TIMESTAMP DEFAULT current_timestamp NOT NULL,
  PRIMARY KEY (`id`)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- CREATE TABLE IF NOT EXISTS `type_of_work` (
--   `id` INT NOT NULL AUTO_INCREMENT,
--   `name` VARCHAR(2048) NOT NULL,
--   `created_at` TIMESTAMP DEFAULT current_timestamp NOT NULL,
--   PRIMARY KEY (`id`)
-- )
-- ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

CREATE TABLE IF NOT EXISTS `licenses_registry` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `link_to_card` VARCHAR(96) NOT NULL,
  `reg_number` VARCHAR(24) NOT NULL,
  `el_image` BOOLEAN NOT NULL,
  `reg_date` DATE NOT NULL,
  `license_purpose` VARCHAR(1024),
  `type_of_minerals` INT NOT NULL,
  `plot_name` VARCHAR(1024),
  `russian_region` INT NOT NULL,
  `geo` VARCHAR(1024),
  `plot_status` INT,
  `inn` VARCHAR(12),
  `gov_agency` VARCHAR(128),
  `base_doc` VARCHAR(128),
  `license_changes` VARCHAR(256),
  `license_renewal` VARCHAR(256),
  `order_details` VARCHAR(256),
  `termination_date` VARCHAR(128),
  `restriction` VARCHAR(256),
  `end_date` DATE,
  `previous_licenses` VARCHAR(256),
  `created_at` TIMESTAMP DEFAULT current_timestamp NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY(`type_of_minerals`) REFERENCES `type_of_minerals`(id),
  FOREIGN KEY(`russian_region`) REFERENCES `russian_regions`(id),
  FOREIGN KEY(`plot_status`) REFERENCES `plot_status`(id)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
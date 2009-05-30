from dmigrations.mysql import migrations as m
import datetime
migration = m.Migration(sql_up=["""
    CREATE TABLE `structure_college` (
        `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
        `name` varchar(100) NOT NULL,
        `abbreviation` varchar(10) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    ;
""", """
    CREATE TABLE `structure_department` (
        `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
        `name` varchar(100) NOT NULL,
        `college_id` integer NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    ;
""", """
    ALTER TABLE `structure_department` ADD CONSTRAINT `college_id_refs_id_14d570ff` FOREIGN KEY (`college_id`) REFERENCES `structure_college` (`id`);
""", """
    CREATE TABLE `structure_program` (
        `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
        `name` varchar(100) NOT NULL,
        `department_id` integer NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    ;
""", """
    ALTER TABLE `structure_program` ADD CONSTRAINT `department_id_refs_id_7f983350` FOREIGN KEY (`department_id`) REFERENCES `structure_department` (`id`);
""", """
    CREATE TABLE `structure_campus` (
        `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
        `name` varchar(50) NOT NULL,
        `address` varchar(100) NOT NULL,
        `city` varchar(100) NOT NULL,
        `state` varchar(2) NOT NULL,
        `zip_code` varchar(9) NOT NULL,
        `country` varchar(50) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    ;
""", """
    CREATE TABLE `structure_building` (
        `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
        `name` varchar(100) NOT NULL,
        `campus_id` integer NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    ;
""", """
    ALTER TABLE `structure_building` ADD CONSTRAINT `campus_id_refs_id_2a87f470` FOREIGN KEY (`campus_id`) REFERENCES `structure_campus` (`id`);
""", """
    CREATE TABLE `structure_location` (
        `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
        `building_id` integer NOT NULL,
        `room_number` varchar(10) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    ;
""", """
    ALTER TABLE `structure_location` ADD CONSTRAINT `building_id_refs_id_3049c18a` FOREIGN KEY (`building_id`) REFERENCES `structure_building` (`id`);
"""], sql_down=["""
    DROP TABLE `structure_location`;
""", """
    DROP TABLE `structure_building`;
""", """
    DROP TABLE `structure_campus`;
""", """
    DROP TABLE `structure_program`;
""", """
    DROP TABLE `structure_department`;
""", """
    DROP TABLE `structure_college`;
"""])

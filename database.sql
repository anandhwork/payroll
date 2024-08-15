CREATE TABLE `employee` (
  `employee_id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `dob` date NOT NULL,
  `nationality` varchar(255) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `ni_number` varchar(255) DEFAULT NULL,
  `telephone` int(11) DEFAULT NULL,
  `email_address` varchar(255) DEFAULT NULL,
  `status` int(11) NOT NULL DEFAULT 0,
  `created_on` datetime NOT NULL,
  `updated_on` datetime NOT NULL,
  PRIMARY KEY (`employee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `employee_emergency` (
  `employee_emergency_id` int(11) NOT NULL AUTO_INCREMENT,
  `employee_id` int(11) NOT NULL,
  `emergency_contact_person` varchar(255) DEFAULT NULL,
  `emergency_contact_number` int(11) DEFAULT NULL,
  `emergency_contact_relationship` varchar(255) DEFAULT NULL,
  `emergency_contact_email_address` varchar(255) DEFAULT NULL,
  `emergency_contact_home_address` text DEFAULT NULL,
  PRIMARY KEY (`employee_emergency_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
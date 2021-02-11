CREATE TABLE user_data (
    id SMALLINT UNSIGNED NOT NULL auto_increment,
    first_name VARCHAR(20) NOT NULL,
    second_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    email VARCHAR(20) NOT NULL,
    address VARCHAR(20) NOT NULL,
    telephone VARCHAR(20) NOT NULL,
    passwd VARCHAR(20) NOT NULL,
    primary key (id)
) ENGINE = InnoDB;

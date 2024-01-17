
CREATE TABLE IF NOT EXISTS customers (
    id int PRIMARY KEY,
    names varchar(50) NOT NULL,
    surnames varchar(50) NOT NULL,
    email varchar(100) NOT NULL,
    phone_number varchar(20) NOT NULL
);


CREATE TABLE IF NOT EXISTS transactions (
    id int NOT NULL,
    trans_date Date,
    float amount,
    PRIMARY KEY (id)
);

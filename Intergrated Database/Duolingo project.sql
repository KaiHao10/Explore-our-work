
-- Location Table --
CREATE TABLE Location (
    location_id serial PRIMARY KEY,
    country VARCHAR(255) NOT NULL,
    alpha_two_code VARCHAR(255)
);

-- Institutions Table --
CREATE TABLE Institutions (
    institution_id serial PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    domains VARCHAR(255),
    web_pages VARCHAR(255),
    contact VARCHAR(255),
    location_id INT NOT NULL,
    FOREIGN KEY (location_id) REFERENCES Location(location_id) ON DELETE CASCADE
);

-- DET Acceptance Table --
CREATE TABLE DET_Acceptance (
    det_id serial PRIMARY KEY,
    institution_id INT NOT NULL,
    accepts_det BOOLEAN NOT NULL,
    official_cooperation BOOLEAN,
    minimum_score_undergraduate INT NULL,
    minimum_score_graduate INT NULL,
    FOREIGN KEY (institution_id) REFERENCES Institutions(institution_id) ON DELETE CASCADE
);

-- Users Table --
CREATE TABLE Users (
    user_id serial PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    location_id INT NOT NULL,
    test_count INT DEFAULT 0,
    last_test_date timestamp NULL,
    FOREIGN KEY (location_id) REFERENCES Location(location_id) ON DELETE CASCADE
);

-- Test History Table --
CREATE TABLE Test_History (
    test_id serial PRIMARY KEY,
    user_id INT NOT NULL,
    test_date timestamp NOT NULL,
    score INT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Favorite Table --
CREATE TABLE Favorites (
    favorite_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    institution_id INT NOT NULL,
    user_location_id INT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (institution_id) REFERENCES Institutions(institution_id) ON DELETE CASCADE,
    FOREIGN KEY (user_location_id) REFERENCES Location(location_id) ON DELETE CASCADE
);

-- Favorite Summary Table --
CREATE TABLE Favorites_Summary (
    summary_id serial PRIMARY KEY,
    institution_id INT NOT NULL,
    location_id INT NOT NULL,
    quarter VARCHAR(10) NOT NULL,
    favorite_count INT DEFAULT 0,
    FOREIGN KEY (institution_id) REFERENCES Institutions(institution_id) ON DELETE CASCADE,
    FOREIGN KEY (location_id) REFERENCES Location(location_id) ON DELETE CASCADE,
    UNIQUE (institution_id, location_id, quarter)
);

--Location Table--
INSERT INTO location(
    country,
    alpha_two_code
)
values
('Australia', 'AU'),
('India',	'IN'),
('United Kingdom',	'GB'),
('United States',	'US'),
('Denmark',	'DK'),
('Finland',	'FI'),
('Hong Kong',	'HK'),
('Israel',	'IL'),
('Netherlands',	'NL'),
('New Zealand',	'NZ'),
('Qatar',	'QA'),
('Singapore',	'SG'),
('Sweden',	'SE');

--Institution Table--
COPY Institutions (name, domains, web_pages,contact, location_id)
FROM 'institusions.csv'
WITH (
  FORMAT CSV,
  HEADER true,
  DELIMITER ','
);
SELECT * FROM Institutions;

--DET_Acceptance Table--
COPY DET_Acceptance (institution_id, accepts_det)
FROM 'det_acceptance.csv'
WITH (
  FORMAT CSV,
  HEADER true,
  DELIMITER ','
);
SELECT * FROM DET_Acceptance;
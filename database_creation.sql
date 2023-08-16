
CREATE SCHEMA IF NOT EXISTS totem;

CREATE TABLE totem.photo(
	photoName VARCHAR(255),
	localPath VARCHAR(255),
	downloaded BOOLEAN DEFAULT FALSE,
	digest VARCHAR(255) NOT NULL,
	receivedTime TIMESTAMP,
	PRIMARY KEY (photoName)
);

CREATE TABLE totem.downloadtime(
	id SERIAL NOT NULL,
	photoName VARCHAR(255),
	downloadTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT fk_photo
		FOREIGN KEY(photoName) 
			REFERENCES totem.photo(photoName)
);
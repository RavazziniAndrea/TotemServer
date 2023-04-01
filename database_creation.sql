
CREATE TABLE Photo(
	photoName VARCHAR(255),
	localPath VARCHAR(255),
	downloaded BOOLEAN DEFAULT FALSE,
	digested VARCHAR(255) NOT NULL,
	sentTime TIMESTAMP,
	PRIMARY KEY (photoName)
);

CREATE TABLE DownloadTime(
	id SERIAL NOT NULL,
	photoName VARCHAR(255),
	downloadTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT fk_photo
		FOREIGN KEY(photoName) 
			REFERENCES Photo(photoName)
);
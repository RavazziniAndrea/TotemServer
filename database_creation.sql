
CREATE TABLE Photo(
	id SERIAL,
	localPath VARCHAR(255),
	downloaded BOOLEAN DEFAULT FALSE,
	digested VARCHAR(255) NOT NULL,
	sentTime TIMESTAMP,
	PRIMARY KEY (localpath)
);

CREATE TABLE DownloadTime(
	id SERIAL NOT NULL,
	localPath VARCHAR(255),
	downloadTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT fk_photo
		FOREIGN KEY(localPath) 
			REFERENCES Photo(localPath)
);
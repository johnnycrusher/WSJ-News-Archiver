-- This small SQLite script creates the table for the event_log.db
-- database.  However, you shouldn't need to use it because a copy
-- of the database itself has already been provided.

CREATE TABLE `Event_Log` (
	`Event_Number`	INTEGER,
	`Description`	TEXT,
	PRIMARY KEY(`Event_Number`)
);

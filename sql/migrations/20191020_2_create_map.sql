CREATE TABLE "map" (
  map_id INTEGER PRIMARY KEY AUTOINCREMENT,
  code VARCHAR(20) not null ,
  libelle VARCHAR(20) not null ,
  lon FLOAT not null,
  lat FLOAT not null);

CREATE TABLE "map_marker_link" (
  `map_id` INTEGER not null,
  `marker_id` INTEGER not null,
   FOREIGN KEY (map_id)
       REFERENCES map (map_id) ,
   FOREIGN KEY (marker_id)
       REFERENCES markers (marker_id) );
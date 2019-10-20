CREATE TABLE "markers" (
  marker_id INTEGER PRIMARY KEY AUTOINCREMENT,
  lon FLOAT not null,
  lat FLOAT not null,
	name TEXT, 
	description TEXT, 
	energy TEXT, 
	house_type TEXT, 
	logement_count TEXT, 
	p_panel_count FLOAT, 
	w_panel_count FLOAT, 
	north_azimut FLOAT, 
	roof_shape FLOAT, 
	sunchine FLOAT, 
	validation TEXT, 
	comment TEXT);
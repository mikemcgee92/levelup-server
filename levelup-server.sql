SELECT * FROM levelupapi_gametype;
SELECT * FROM levelupapi_gamer;
SELECT * FROM levelupapi_game;
SELECT * FROM levelupapi_event;

DELETE FROM levelupapi_gamer WHERE Id = 2;

DELETE FROM levelupapi_eventgamer WHERE gamer_id = 3;

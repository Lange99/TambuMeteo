# Introduction
A Telegram bot sending reminders when it rains given a location.

# Initialization
Persistency is achieved through a sqlite database file called locations.db.
The DB is composed by a single table "locations". Structure is very simple:
```sql
CREATE TABLE locations(
    chat_id PRIMARY KEY,
    lat,
    lon
);
``` 

# Execution
Highly recommend to run inside Docker.
Suggested command is:
```sh
docker run -e TELEGRAM_TOKEN="XXX" -e OPENWEATHER_APPID="XXX" -v absolute_local_path:absolute_docker_path tag
```

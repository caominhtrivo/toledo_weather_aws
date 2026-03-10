-- 1. Create a View for Analytics
-- This view transforms raw Fahrenheit to Celsius and localizes UTC time to Ohio (EST)
CREATE OR REPLACE VIEW toledo_weather_db.v_toledo_weather_report AS
SELECT
    name AS city,
    main.temp AS temp_f,
    round((main.temp - 32) * 5 / 9, 2) AS temp_c,
    from_unixtime(dt) - interval '4' hour AS toledo_time,
    main.humidity AS humidity,
    wind.speed AS wind_speed,
    wind.gust AS wind_gust,
    weather[1].description AS sky_condition,
    year,
    month,
    day
FROM "toledo_weather_db"."raw_data";

-- 2. Querying the View
-- Use this to retrieve the latest 10 weather records for Toledo
SELECT * FROM "toledo_weather_db"."v_toledo_weather_report"
ORDER BY toledo_time DESC
LIMIT 10;
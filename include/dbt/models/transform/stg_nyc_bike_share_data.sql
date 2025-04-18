{{
    config(
        materialized='view'
    )
}}

with nyc_bike_share_data as 
(
  select * from {{ source('staging','NYC_BIKE_SHARE_data_external') }}

)
select
    
    cast(ride_id as string) as ride_id,
    cast(rideable_type as string)as bike_type,
    FORMAT_TIMESTAMP('%Y-%m',started_at) as year_month,
    EXTRACT(DAYOFWEEK FROM started_at) AS day_of_week,
    cast(started_at as timestamp) as ride_start_time,
    cast(ended_at as timestamp) as ride_end_time,
    TIMESTAMP_DIFF(ended_at, started_at, MINUTE) AS total_trip_duration_minutes,
    start_station_name,
    start_station_id,
    end_station_name,
    end_station_id,
    cast(start_lat as FLOAT64) as start_latitude,
    cast(start_lng as FLOAT64) as start_longitude,
    cast(end_lat as FLOAT64) as end_latitude,
    cast(end_lng as FLOAT64) as end_longitude,
    -- Distance in miles (Haversine, fixed RADIANS)
   3959 * 2 * ASIN(
    SQRT(
      POW(SIN((CAST(end_lat AS FLOAT64) - CAST(start_lat AS FLOAT64)) * 3.141592653589793 / 180 / 2), 2) +
      COS(CAST(start_lat AS FLOAT64) * 3.141592653589793 / 180) * COS(CAST(end_lat AS FLOAT64) * 3.141592653589793 / 180) *
      POW(SIN((CAST(end_lng AS FLOAT64) - CAST(start_lng AS FLOAT64)) * 3.141592653589793 / 180 / 2), 2)
    )
    ) AS total_distance_miles,
    cast(member_casual as string) as member_type
from nyc_bike_share_data
where end_station_id is not null 
or start_station_id is not null
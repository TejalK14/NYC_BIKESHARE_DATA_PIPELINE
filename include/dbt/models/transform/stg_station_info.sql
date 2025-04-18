{{
    config(
        materialized='table'
    )
}}

with nyc_stn_info_data as 
(
  select * from {{ source('staging','station_info') }}

)
select
    
    station_id as stn_id,
    short_name as stn_short_name,
    capacity as stn_capacity,
    lon as stn_longitude,
    lat as stn_latitude,
    name as stn_name,
    region_id
from nyc_stn_info_data
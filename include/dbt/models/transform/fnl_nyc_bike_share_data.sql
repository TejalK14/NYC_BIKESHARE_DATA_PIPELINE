{{
    config(
        materialized='table',
        partition_by={
            "field": "year_month",
            "data_type": "string"
        }
    )
}}

with nyc_bike_share_data as (
    select *
    from {{ ref('stg_nyc_bike_share_data') }}
), 
station_info as (
    select * 
    from {{ ref('stg_station_info') }}
),
dim_region_lookup as (
    select * from {{ ref('dim_region_lookup') }}
)
select a.* ,
start_stn_info.region_id as start_region_id,
start_rgn.region_name as start_region_name,
end_stn_info.region_id as end_region_id,
end_rgn.region_name as end_region_name
from nyc_bike_share_data a
join station_info start_stn_info on a.start_station_id = start_stn_info.stn_short_name
join station_info end_stn_info on a.end_station_id = end_stn_info.stn_short_name
join dim_region_lookup start_rgn on start_rgn.region_id = start_stn_info.region_id
join dim_region_lookup end_rgn on end_rgn.region_id = end_stn_info.region_id
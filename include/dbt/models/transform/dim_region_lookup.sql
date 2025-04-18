{{
    config(
        materialized='table'
    )
}}

with nyc_region_lookup as 
(
  select * from {{ source('staging','region_lookup') }}

)
select 
    name as region_name, 
    region_id
from nyc_region_lookup

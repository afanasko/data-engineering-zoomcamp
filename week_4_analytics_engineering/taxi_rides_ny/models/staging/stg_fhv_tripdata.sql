{{ config(materialized='view') }}

with tripdata as 
(
  select *
  from {{ source('staging','external_fhv_tripdata') }}
)
select
    -- identifiers
    {{ dbt_utils.generate_surrogate_key(['pickup_datetime', 'PUlocationID']) }} as tripid,
    dispatching_base_num as dispatching_base_num,
    cast(pulocationid as integer) as pickup_locationid,
    cast(dolocationid as integer) as dropoff_locationid,
    
    -- timestamps
    cast(pickup_datetime as timestamp) as pickup_datetime,
    cast(dropOff_datetime as timestamp) as dropoff_datetime,
    
    -- trip info
    cast(sr_flag as integer) as sr_flag,
    Affiliated_base_number as affiliated_base_number
    
from tripdata


-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}

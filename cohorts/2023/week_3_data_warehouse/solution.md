
<b>SETUP:</b></br>
Create an external table using the fhv 2019 data. </br>
Create a table in BQ using the fhv 2019 data (do not partition or cluster this table). </br>
Data can be found here: https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/fhv </p>

```sql
-- Creating external table referring to gcs path
CREATE OR REPLACE external TABLE `de-zoomcamp-2023-375809.nytaxi.external_fhv_tripdata`

OPTIONS (
  format = 'csv',
  uris = ['gs://de-zoomcamp-bucket/data/fhv/fhv_tripdata_2019-*.csv.gz']

);

-- Creating table from external
CREATE TABLE `de-zoomcamp-2023-375809.nytaxi.fhv_tripdata`
AS SELECT * FROM `de-zoomcamp-2023-375809.nytaxi.external_fhv_tripdata`;
```

## Question 1:
What is the count for fhv vehicle records for year 2019?

```sql
-- count distinct affiliated_base_number
SELECT COUNT(DISTINCT affiliated_base_number) FROM `de-zoomcamp-2023-375809.nytaxi.external_fhv_tripdata`;
```

## Question 2:
Write a query to count the distinct number of affiliated_base_number for the entire dataset on both the tables.</br> 
What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?
```sql
-- count distinct affiliated_base_number in materilized table
SELECT COUNT(DISTINCT affiliated_base_number) FROM `de-zoomcamp-2023-375809.nytaxi.fhv_tripdata`;
```


## Question 3:
How many records have both a blank (null) PUlocationID and DOlocationID in the entire dataset?
```sql
-- How many records have both a blank (null) PUlocationID and DOlocationID in the entire dataset?
SELECT COUNT(*) FROM `nytaxi.fhv_tripdata` WHERE PUlocationID is NULL AND DOlocationID is NULL;
```

## Question 4:
What is the best strategy to optimize the table if query always filter by pickup_datetime and order by affiliated_base_number?
```sql
-- create partinioned and clustered table
CREATE TABLE `de-zoomcamp-2023-375809.nytaxi.fhv_tripdata_part`
PARTITION BY DATE(pickup_datetime)
CLUSTER BY affiliated_base_number
AS SELECT * FROM `de-zoomcamp-2023-375809.nytaxi.fhv_tripdata`;
```

## Question 5:
Implement the optimized solution you chose for question 4. Write a query to retrieve the distinct affiliated_base_number between pickup_datetime 2019/03/01 and 2019/03/31 (inclusive).</br> 
Use the BQ table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. What are these values? Choose the answer which most closely matches.
```sql
-- Write a query to retrieve the distinct affiliated_base_number between pickup_datetime 03/01/2019 and 03/31/2019 (inclusive)
SELECT DISTINCT(affiliated_base_number) FROM `nytaxi.fhv_tripdata` WHERE pickup_datetime BETWEEN '2019-03-01 00:00:00' AND '2019-03-31 23:59:59';

SELECT DISTINCT(affiliated_base_number) FROM `nytaxi.fhv_tripdata_part` WHERE pickup_datetime BETWEEN '2019-03-01 00:00:00' AND '2019-03-31 23:59:59';
```


import os
from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint


@task()
def write_gcs(path: Path) -> None:
    """Upload local file to GCS"""
    gcs_block = GcsBucket.load("de-zoom-bucket")
    gcs_block.upload_from_path(from_path=path, to_path=path)
    return


@flow()
def etl_web_to_gcs(color: str, year: int, month: int) -> None:
    """The main ETL function"""
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    file_name = f"data/{color}/{dataset_file}.csv.gz"
    os.system(f"wget {dataset_url} -O {file_name}")
    path = Path(file_name)
    write_gcs(path)

@flow()
def etl_parent_flow(color: str = "fhv", year: int = 2019, months: list[int] = range(1,13)):
    """Entry point for perfect flow"""
    for month in months:
        etl_web_to_gcs(color, year, month)


if __name__ == "__main__":
    color = "fhv"
    year = 2019
    month = 1
    etl_web_to_gcs(color, year, month)

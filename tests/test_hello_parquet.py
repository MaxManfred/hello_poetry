from tempfile import gettempdir

import pytest
from pyspark.sql import DataFrame

from hello_poetry.hello_parquet import create_people_dataframe, write_to_partitioned_parquet_file, \
    read_from_partitioned_parquet_file, compute_total_salary


@pytest.mark.parametrize(
    'parquet_file_url, gender, temporary_view_name',
    [
        (f'{gettempdir()}/people.parquet', 'M', 'people'),
        (f'{gettempdir()}/people.parquet', 'F', 'people'),
    ]
)
def test_compute_total_salary(parquet_file_url: str, gender: str, temporary_view_name: str):
    people_df: DataFrame = create_people_dataframe()

    write_to_partitioned_parquet_file(people_df, parquet_file_url)
    people_by_gender_df = read_from_partitioned_parquet_file(gender, parquet_file_url, temporary_view_name)

    assert people_df.count() > people_by_gender_df.count()

    compute_total_salary(temporary_view_name)

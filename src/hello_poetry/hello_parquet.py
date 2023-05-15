import pyspark.sql.functions as fn
from pyspark.sql import DataFrame
from pyspark.sql.functions import col

from hello_poetry.hello_pyspark import _create_spark_session


def create_people_dataframe() -> DataFrame:
    data = [
        ('James ', '', 'Smith', '36636', 'M', 3000),
        ('Michael ', 'Rose', '', '40288', 'M', 4000),
        ('Robert ', '', 'Williams', '42114', 'M', 4000),
        ('Maria ', 'Anne', 'Jones', '39192', 'F', 4000),
        ('Jen', 'Mary', 'Brown', '', 'F', -1)
    ]
    columns = ['firstname', 'middlename', 'lastname', 'dob', 'gender', 'salary']

    print('People dataframe created!')

    return _create_spark_session().createDataFrame(data, columns)


def write_to_partitioned_parquet_file(df: DataFrame, parquet_file_url: str is not None) -> None:
    df \
        .write \
        .partitionBy('gender', 'salary') \
        .mode('overwrite') \
        .parquet(parquet_file_url)

    print(f'Dataframe {df.schema} written to partitioned parquet file {parquet_file_url}!')


def read_from_partitioned_parquet_file(gender: str is not None, parquet_file_url: str is not None,
                                       temporary_view_name: str is not None) -> DataFrame:
    df = _create_spark_session() \
        .read \
        .parquet(f'{parquet_file_url}/gender={gender}')

    print(f'Dataframe {df.schema} read from partitioned parquet file {parquet_file_url}!')

    df.createOrReplaceTempView(temporary_view_name)

    print(f'Temporary view {temporary_view_name} created!')

    return df


def compute_total_salary(temporary_view_name: str is not None) -> None:
    df = _create_spark_session().sql(f'select * from {temporary_view_name} where salary > 0')
    df.select([fn.sum(col('salary')).alias('Total salary')]).show(truncate=False)

import sys

from pyspark.sql import DataFrame

from hello_poetry.hello_parquet import create_people_dataframe, write_to_partitioned_parquet_file, \
    read_from_partitioned_parquet_file, compute_total_salary

if __name__ == '__main__':
    print(sys.argv[1:])

    parquet_file_url = sys.argv[1].split('=')[1]
    print(f'parquet_file_url: {parquet_file_url}')

    temporary_view = sys.argv[2].split('=')[1]
    print(f'temporary_view: {temporary_view}')

    gender = sys.argv[3].split('=')[1]
    print(f'gender: {gender}')

    people_df: DataFrame = create_people_dataframe()
    write_to_partitioned_parquet_file(people_df, parquet_file_url)
    people_by_gender_df = read_from_partitioned_parquet_file(gender, parquet_file_url, temporary_view)
    compute_total_salary(temporary_view)

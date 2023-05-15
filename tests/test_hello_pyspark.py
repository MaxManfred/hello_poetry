from typing import List

import pytest
from pyspark.sql import DataFrame

from hello_poetry.hello_pyspark import create_dataframe_with_implicit_schema, _create_rdd, _create_spark_session, \
    create_dataframe_with_explicit_schema, create_dataframe_with_struct_schema


def _print_and_assert(df: DataFrame, expected_count: int, expected_column_names: List[str]) -> None:
    print('\n')
    df.printSchema()
    df.show(truncate=False)

    assert df.count() == expected_count
    assert list(map(lambda f: f.name, df.schema.fields)) == expected_column_names


@pytest.mark.parametrize(
    'input_rdd, expected_count, expected_column_names',
    [
        (None, 4, ['_1', '_2']),
        (_create_rdd(), 4, ['_1', '_2'])
    ]
)
def test_create_dataframe_with_implicit_schema(input_rdd, expected_count, expected_column_names):
    df: DataFrame = create_dataframe_with_implicit_schema(input_rdd)
    _print_and_assert(df, expected_count, expected_column_names)


@pytest.mark.parametrize(
    'input_rdd, input_spark_session, expected_count, expected_column_names',
    [
        (None, None, 4, ['dept_name', 'dept_id']),
        (_create_rdd(), None, 4, ['dept_name', 'dept_id']),
        (None, _create_spark_session(), 4, ['dept_name', 'dept_id']),
        (_create_rdd(), _create_spark_session(), 4, ['dept_name', 'dept_id']),
    ]
)
def test_create_dataframe_with_explicit_schema(input_rdd, input_spark_session, expected_count, expected_column_names):
    df: DataFrame = create_dataframe_with_explicit_schema(input_rdd, input_spark_session)
    _print_and_assert(df, expected_count, expected_column_names)

@pytest.mark.parametrize(
    'input_rdd, input_spark_session, expected_count, expected_column_names',
    [
        (None, None, 4, ['dept_name_struct', 'dept_id_struct']),
        (_create_rdd(), None, 4, ['dept_name_struct', 'dept_id_struct']),
        (None, _create_spark_session(), 4, ['dept_name_struct', 'dept_id_struct']),
        (_create_rdd(), _create_spark_session(), 4, ['dept_name_struct', 'dept_id_struct']),
    ]
)
def test_create_dataframe_with_struct_schema(input_rdd, input_spark_session, expected_count, expected_column_names):
    df: DataFrame = create_dataframe_with_struct_schema(input_rdd, input_spark_session)
    _print_and_assert(df, expected_count, expected_column_names)
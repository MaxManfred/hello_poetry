from typing import Optional

from pyspark import RDD
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType, StructField, StringType


def _create_spark_session() -> SparkSession:
    # return \
    # SparkSession \
    #     .builder \
    #     .appName('SparkByExamples.com') \
    #     .master('local[*]') \
    #     .getOrCreate()
    return SparkSession.builder.appName('SparkByExamples.com').getOrCreate()


def _create_rdd() -> RDD:
    data = [
        ('Finance', 10),
        ('Marketing', 20),
        ('Sales', 30),
        ('IT', 40)
    ]

    # create a Spark RDD on data
    return _create_spark_session().sparkContext.parallelize(data)


def create_dataframe_with_implicit_schema(rdd: Optional[RDD] = None) -> DataFrame:
    return rdd.toDF() if rdd else _create_rdd().toDF()


def create_dataframe_with_explicit_schema(rdd: Optional[RDD] = None,
                                          spark_session: Optional[SparkSession] = None) -> DataFrame:
    column_names = ['dept_name', 'dept_id']

    if not rdd:
        rdd = _create_rdd()

    if spark_session:
        df = spark_session.createDataFrame(rdd, schema=column_names)
    else:
        df = rdd.toDF(column_names)

    return df


def create_dataframe_with_struct_schema(rdd: Optional[RDD] = None,
                                        spark_session: Optional[SparkSession] = None) -> DataFrame:
    if not spark_session:
        spark_session = _create_spark_session()

    if not rdd:
        rdd = _create_rdd()

    struct_schema = StructType([
        StructField('dept_name_struct', StringType(), True),
        StructField('dept_id_struct', StringType(), True)
    ])

    return spark_session.createDataFrame(rdd, schema=struct_schema)

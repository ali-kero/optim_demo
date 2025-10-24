# Databricks notebook source
# MAGIC %md
# MAGIC <table>
# MAGIC   <tr>
# MAGIC     <td></td>
# MAGIC     <td>VM</td>
# MAGIC     <td>Quantity</td>
# MAGIC     <td>Total Cores</td>
# MAGIC     <td>Total RAM</td>
# MAGIC   </tr>
# MAGIC   <tr>
# MAGIC     <td>Driver:</td>
# MAGIC     <td>**i3.xlarge**</td>
# MAGIC     <td>**1**</td>
# MAGIC     <td>**4 cores**</td>
# MAGIC     <td>**30.5 GB**</td>
# MAGIC   </tr>
# MAGIC   <tr>
# MAGIC     <td>Workers:</td>
# MAGIC     <td>**i3.xlarge**</td>
# MAGIC     <td>**2**</td>
# MAGIC     <td>**8 cores**</td>
# MAGIC     <td>**61 GB**</td>
# MAGIC   </tr>
# MAGIC </table>

# COMMAND ----------

# Create widgets for catalog and schema
dbutils.widgets.text("catalog", "ali_karaouzene", "Catalog")
dbutils.widgets.text("schema", "sparkuisim", "Schema")

# Get widget values
catalog_name = dbutils.widgets.get("catalog")
schema_name = dbutils.widgets.get("schema")

# COMMAND ----------

# spark.conf.set("spark.sql.shuffle.partitions", 832)
# spark.conf.set("spark.databricks.io.cache.enabled", False)
transaction_table = f"{catalog_name}.{schema_name}.2011_to_2018_100gb"
cities_table = f"{catalog_name}.{schema_name}.all"

# COMMAND ----------

# How skewed is our data?
visualizeDF = (
    spark.read
    .table(transaction_table)
    .groupBy("city_id").count()
    .orderBy("count")
)

display(visualizeDF)

# COMMAND ----------


# Ensure that AQE is disabled
# spark.conf.set("spark.sql.adaptive.enabled", False)
# spark.conf.set("spark.sql.adaptive.skewedJoin.enabled", False)

ctyDF = spark.read.table(cities_table)  # Load the city table
trxDF = spark.read.table(transaction_table)  # Load the transactions table

(
    trxDF.join(ctyDF, ctyDF["city_id"] == trxDF["city_id"])
    .write.format("noop").mode("overwrite").save()
)

# COMMAND ----------

# DBTITLE 1,Join with skew hint

# Ensure that AQE is disabled
spark.conf.set("spark.sql.adaptive.enabled", False)
spark.conf.set("spark.sql.adaptive.skewedJoin.enabled", False)

ctyDF = spark.read.table(cities_table)  # Load the city table
trxDF = (
    spark.read.table(transaction_table)      # Load the transactions table
    .hint("skew", "city_id")                      # Required to avoid Executor-OOM and/or Spill
)

(
    trxDF.join(ctyDF, ctyDF["city_id"] == trxDF["city_id"])
    .write.format("noop").mode("overwrite").save()
)

# COMMAND ----------

# DBTITLE 1,Join with AQE
# Join with AQE

spark.conf.set("spark.sql.adaptive.enabled", true)
spark.conf.set("spark.sql.adaptive.skewedJoin.enabled", true)

# The default is 64 MB, but in this case we want to maintain 128m partitions
spark.conf.set("spark.sql.adaptive.advisoryPartitionSizeInBytes", "128m")

ctyDF = spark.read.table(cities_table)  # Load the city table
trxDF = (
    spark.read.table(transaction_table)      # Load the transactions table
  # .hint("skew", "city_id")                          // Not required with AQE's spark.sql.adaptive.skewedJoin
)

(
    trxDF.join(ctyDF, ctyDF["city_id"] == trxDF["city_id"])
    .write.format("noop").mode("overwrite").save()
)

# COMMAND ----------

sc.setJobDescription("Step F-1: Salted-Skew, saltDF")

spark.conf.set("spark.sql.adaptive.enabled", False)
spark.conf.set("spark.sql.adaptive.skewedJoin.enabled", False)

# Too large - unnecessary overhead in the join and crossjoin
# Too small - skewed partition is not split up enough
# This value was selected after much experimentation
skewFactor = 7

saltDF = spark.range(skewFactor).toDF("salt")

# COMMAND ----------

import math
from pyspark.sql import functions as F

sc.setJobDescription("Step F-2: Salted-Skew, ctySaltedDF")

# Post cross-join, we will be at ~865 MB (experimentation - see exchange data size)
# 128 MB is Spark's safe, default partition size.
partitions = int(math.ceil(865 / 128))
ctyDF = spark.read.table(cities_table)  # Load the city table

ctySaltedDF = (
    ctyDF.repartition(partitions)                           # Pre-emptively avoiding spill post cross-join
    .crossJoin(saltDF)                                      # Cross join with saltDF
    .withColumn("salted_city_id",                           # Add the new column "salted_city_id"
                F.concat(F.col("city_id"), F.lit("_"), F.col("salt"))) # Concatenate "city_id" and "salt"
    .drop("salt")                                           # Drop the now unused column "salt"
)

ctySaltedDF.printSchema()

# COMMAND ----------

# sc.setJobDescription("Step F-3: Salted-Skew, trxSaltedDF")

from pyspark.sql.functions import lit, rand, col, concat

trxSaltedDF = (
    spark.read.table(transaction_table)                         # Load the delta table
    .withColumn("salt", (lit(skewFactor) * rand()).cast("int"))      # Create a random "salt" column
    .withColumn("salted_city_id",                                    # Add the new column "salted_city_id"
                concat(col("city_id"), lit("_"), col("salt")))       # Concatenate "city_id" and "salt"
    .drop("salt")                                                    # Drop the now unused column "salt"
)

trxSaltedDF.printSchema()

# COMMAND ----------

# sc.setJobDescription("Step F-4: Salted-Skew, the join")

(
    trxSaltedDF
    .join(ctySaltedDF, ctySaltedDF["salted_city_id"] == trxSaltedDF["salted_city_id"])  # Join by salted_city_id
    .write.format("noop").mode("overwrite").save()                                      # Execute a noop write to test
)

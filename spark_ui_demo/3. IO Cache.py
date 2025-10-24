# Databricks notebook source
dbutils.widgets.text("catalog", "ali_karaouzene", "Catalog")
dbutils.widgets.text("schema", "sparkuisim", "Schema")

catalog_name = dbutils.widgets.get("catalog")
schema_name = dbutils.widgets.get("schema")

# COMMAND ----------

transaction_table = f"{catalog_name}.{schema_name}.2011_to_2018_100gb"
cities_table = f"{catalog_name}.{schema_name}.all"



# COMMAND ----------

# "Step B: Establish a baseline"

# Ensure that the IO Cache is disabled to start with
spark.conf.set("spark.databricks.io.cache.enabled", False)

(spark
  .read.table(transaction_table)            # Load the delta table
  .write.format("noop").mode("overwrite").save() # Execute a noop write to test
)

# COMMAND ----------

# "Step C: Materialize the IO Cache"

# Ensure that the IO Cache is enabled
spark.conf.set("spark.databricks.io.cache.enabled", True)

# Materialize the cache...
(spark.read.table(transaction_table)            # Load the delta table
     .write.format("noop").mode("overwrite").save()) # Execute a noop write to materialize

# COMMAND ----------

# "Step D: Test #1"

(spark.read.table(transaction_table)            # Load the delta table
     .write.format("noop").mode("overwrite").save()) # Execute a noop write to materialize

# COMMAND ----------

# MAGIC %scala
# MAGIC sc.setJobDescription("Step E: Test #2")
# MAGIC
# MAGIC spark.read.format("delta").load(trxPath)            // Load the delta table
# MAGIC      .write.format("noop").mode("overwrite").save() // Execute a noop write to test

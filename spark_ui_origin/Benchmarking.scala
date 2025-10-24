// Databricks notebook source
// MAGIC %md
// MAGIC <table>
// MAGIC   <tr>
// MAGIC     <td></td>
// MAGIC     <td>VM</td>
// MAGIC     <td>Quantity</td>
// MAGIC     <td>Total Cores</td>
// MAGIC     <td>Total RAM</td>
// MAGIC   </tr>
// MAGIC   <tr>
// MAGIC     <td>Driver:</td>
// MAGIC     <td>**i3.xlarge**</td>
// MAGIC     <td>**1**</td>
// MAGIC     <td>**4 cores**</td>
// MAGIC     <td>**30.5 GB**</td>
// MAGIC   </tr>
// MAGIC   <tr>
// MAGIC     <td>Workers:</td>
// MAGIC     <td>**i3.xlarge**</td>
// MAGIC     <td>**2**</td>
// MAGIC     <td>**8 cores**</td>
// MAGIC     <td>**61 GB**</td>
// MAGIC   </tr>
// MAGIC </table>

// COMMAND ----------

sc.setJobDescription("Step A-S: Basic initialization")

// Disabled to avoid side effects
spark.conf.set("spark.databricks.io.cache.enabled", false) 

// Path to our dataset
val trxPath = "dbfs:/mnt/training/global-sales/transactions/2011-to-2018-100gb.parquet"

// The schema for our dataset
val schema = "transacted_at timestamp, trx_id string, retailer_id integer, description string, amount decimal(38,2), city_id integer"

// COMMAND ----------

// MAGIC %python
// MAGIC sc.setJobDescription("Step A-P: Basic initialization")
// MAGIC
// MAGIC # Disabled to avoid side effects
// MAGIC spark.conf.set("spark.databricks.io.cache.enabled", False) 
// MAGIC
// MAGIC # Path to our dataset
// MAGIC trxPath = "dbfs:/mnt/training/global-sales/transactions/2011-to-2018-100gb.parquet"
// MAGIC
// MAGIC # The schema for our dataset
// MAGIC schema = "transacted_at timestamp, trx_id string, retailer_id integer, description string, amount decimal(38,2), city_id integer"

// COMMAND ----------

sc.setJobDescription("Step B-1: count")

spark
  .read.parquet(trxPath) // Load the transactions table
  .count()               // Use the count action to establish a benchmark

// COMMAND ----------

sc.setJobDescription("Step B-2: count")

spark
  .read.parquet(trxPath) // Load the transactions table
  .count()               // Use the count action to establish a benchmark

// COMMAND ----------

sc.setJobDescription("Step C-S: count")

spark
  .read.schema(schema) // Specify the schema to avoid side effects
  .parquet(trxPath)    // Load the transactions table
  .count()             // Use the count action to establish a benchmark

// COMMAND ----------

// MAGIC %python
// MAGIC sc.setJobDescription("Step C-P: count")
// MAGIC
// MAGIC (spark
// MAGIC   .read.schema(schema) # Specify the schema to avoid side effects
// MAGIC   .parquet(trxPath)    # Load the transactions table
// MAGIC   .count()             # Use the count action to establish a benchmark
// MAGIC ) 

// COMMAND ----------

sc.setJobDescription("Step D-S: foreach")

spark
  .read.schema(schema) // Specify the schema to avoid side effects
  .parquet(trxPath)    // Load the transactions table
  .foreach(_=>())      // Use a do-nothing foreach action to establish a benchmark

// COMMAND ----------

// MAGIC %python
// MAGIC sc.setJobDescription("Step D-P: foreach")
// MAGIC
// MAGIC (spark
// MAGIC   .read.schema(schema)      # Specify the schema to avoid side effects
// MAGIC   .parquet(trxPath)         # Load the transactions table
// MAGIC   .foreach(lambda x : None) # Use a do-nothing foreach action to establish a benchmark
// MAGIC ) 

// COMMAND ----------

sc.setJobDescription("Step E-S: noop write")

spark
  .read.schema(schema)                           // Specify the schema to avoid side effects
  .parquet(trxPath)                              // Load the transactions table
  .write.format("noop").mode("overwrite").save() // Use a noop write to establish a benchmark

// COMMAND ----------

// MAGIC %python
// MAGIC sc.setJobDescription("Step E-P: noop write")
// MAGIC
// MAGIC (spark
// MAGIC   .read.schema(schema)                           # Specify the schema to avoid side effects
// MAGIC   .parquet(trxPath)                              # Load the transactions table
// MAGIC   .write.format("noop").mode("overwrite").save() # Use a noop write to establish a benchmark
// MAGIC )

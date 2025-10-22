# Databricks notebook source
# MAGIC %md
# MAGIC # Sample Databricks Notebook
# MAGIC 
# MAGIC This notebook demonstrates basic Databricks functionality including:
# MAGIC - Data loading and manipulation with Spark
# MAGIC - Data visualization
# MAGIC - Basic analytics

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup and Configuration

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, sum, when
import pandas as pd

# Display current Spark configuration
print(f"Spark Version: {spark.version}")
print(f"Application Name: {spark.sparkContext.appName}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Sample Data Creation

# COMMAND ----------

# Create sample data
data = [
    ("Alice", "Engineering", 95000, "2020-01-15"),
    ("Bob", "Sales", 75000, "2019-06-20"),
    ("Charlie", "Engineering", 105000, "2018-03-10"),
    ("Diana", "Marketing", 80000, "2021-02-28"),
    ("Eve", "Sales", 85000, "2020-07-12"),
    ("Frank", "Engineering", 98000, "2019-11-05"),
    ("Grace", "Marketing", 82000, "2021-09-17"),
    ("Henry", "Sales", 78000, "2020-04-22")
]

columns = ["name", "department", "salary", "hire_date"]

# Create DataFrame
df = spark.createDataFrame(data, columns)
df = df.withColumn("hire_date", col("hire_date").cast("date"))

# Display the data
display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Data Analysis

# COMMAND ----------

# Calculate average salary by department
avg_salary_by_dept = df.groupBy("department") \
    .agg(
        avg("salary").alias("avg_salary"),
        count("name").alias("employee_count")
    ) \
    .orderBy(col("avg_salary").desc())

display(avg_salary_by_dept)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Data Visualization

# COMMAND ----------

# Convert to Pandas for visualization
pdf = avg_salary_by_dept.toPandas()

# Display as visualization (Databricks will automatically create a chart)
display(pdf)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Advanced Analytics

# COMMAND ----------

# Add salary classification
df_classified = df.withColumn(
    "salary_band",
    when(col("salary") < 80000, "Low")
    .when((col("salary") >= 80000) & (col("salary") < 95000), "Medium")
    .otherwise("High")
)

# Show distribution
salary_distribution = df_classified.groupBy("salary_band") \
    .agg(count("name").alias("count")) \
    .orderBy("salary_band")

display(salary_distribution)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Summary Statistics

# COMMAND ----------

# Calculate summary statistics
summary = df.select("salary").summary()
display(summary)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Export Results (Optional)

# COMMAND ----------

# Uncomment to save results to DBFS
# output_path = "/dbfs/tmp/employee_analysis"
# avg_salary_by_dept.write.mode("overwrite").parquet(output_path)
# print(f"Results saved to {output_path}")


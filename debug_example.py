# Databricks notebook source
# MAGIC %md
# MAGIC # Debugging Example Notebook
# MAGIC 
# MAGIC This notebook demonstrates how to debug Databricks code locally in VS Code.
# MAGIC 
# MAGIC ## How to Debug:
# MAGIC 1. Open this file in VS Code
# MAGIC 2. Set breakpoints by clicking left of line numbers
# MAGIC 3. Press F5 or use "Run → Start Debugging"
# MAGIC 4. Code executes on your Databricks cluster with full debugging!

# COMMAND ----------

# MAGIC %md
# MAGIC ## Simple Example with Breakpoint

# COMMAND ----------

def calculate_statistics(numbers):
    """
    Calculate basic statistics for a list of numbers.
    Set a breakpoint here to inspect values!
    """
    total = sum(numbers)  # <- Set breakpoint here
    count = len(numbers)
    average = total / count
    
    # Find min and max
    minimum = min(numbers)  # <- Or set breakpoint here
    maximum = max(numbers)
    
    return {
        "total": total,
        "count": count,
        "average": average,
        "min": minimum,
        "max": maximum
    }

# Test the function
test_numbers = [10, 20, 30, 40, 50]
stats = calculate_statistics(test_numbers)
print(f"Statistics: {stats}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Spark DataFrame Example

# COMMAND ----------

from pyspark.sql import functions as F

# Create a simple dataset
data = [
    ("Alice", 25, "Engineering", 90000),
    ("Bob", 30, "Sales", 75000),
    ("Charlie", 35, "Engineering", 105000),
    ("Diana", 28, "Marketing", 80000),
    ("Eve", 32, "Sales", 85000)
]

df = spark.createDataFrame(data, ["name", "age", "department", "salary"])

# Set a breakpoint on the next line to inspect the DataFrame
print(f"Total rows: {df.count()}")
df.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Complex Transformation with Debugging

# COMMAND ----------

def process_employee_data(df):
    """
    Process employee data with transformations.
    Set breakpoints to see intermediate results!
    """
    # Step 1: Add salary band
    df_with_band = df.withColumn(
        "salary_band",
        F.when(F.col("salary") < 80000, "Low")
         .when(F.col("salary") < 95000, "Medium")
         .otherwise("High")
    )
    
    # Step 2: Calculate age groups
    df_with_groups = df_with_band.withColumn(
        "age_group",
        F.when(F.col("age") < 30, "Young")
         .when(F.col("age") < 35, "Mid")
         .otherwise("Senior")
    )
    
    # Step 3: Add department statistics
    # Set breakpoint here to see the transformation
    dept_stats = df_with_groups.groupBy("department").agg(
        F.avg("salary").alias("avg_salary"),
        F.count("name").alias("employee_count")
    )
    
    # Join back to original
    result = df_with_groups.join(
        dept_stats.withColumnRenamed("department", "dept_key"),
        df_with_groups.department == dept_stats.dept_key,
        "left"
    ).drop("dept_key")
    
    return result  # <- Set breakpoint here to inspect final result

# Process the data
processed_df = process_employee_data(df)
processed_df.show(truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Error Handling Example

# COMMAND ----------

def divide_numbers(a, b):
    """
    Example function that might raise an exception.
    Set a breakpoint to catch errors before they happen!
    """
    try:
        result = a / b  # <- Set breakpoint here
        print(f"{a} / {b} = {result}")
        return result
    except ZeroDivisionError as e:
        print(f"Error: Cannot divide by zero! {e}")  # <- Or here
        return None

# Test with valid input
divide_numbers(10, 2)

# Test with invalid input (will catch the error)
divide_numbers(10, 0)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Interactive Variables Inspection

# COMMAND ----------

# When debugging, you can inspect these variables in the VS Code debug panel
employee_names = [row.name for row in df.collect()]
total_payroll = df.agg(F.sum("salary")).collect()[0][0]
avg_age = df.agg(F.avg("age")).collect()[0][0]

print(f"Employees: {employee_names}")
print(f"Total payroll: ${total_payroll:,}")
print(f"Average age: {avg_age:.1f}")

# Set a breakpoint on the next line to inspect all variables
print("Debug checkpoint - inspect variables in VS Code!")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Tips for Effective Debugging
# MAGIC 
# MAGIC 1. **Use Breakpoints**: Click left of line numbers to set breakpoints
# MAGIC 2. **Step Through Code**: Use F10 (step over) and F11 (step into)
# MAGIC 3. **Watch Variables**: Add variables to the Watch panel
# MAGIC 4. **Evaluate Expressions**: Use the Debug Console to run code
# MAGIC 5. **Conditional Breakpoints**: Right-click breakpoint for conditions
# MAGIC 6. **Log Points**: Add log messages without modifying code
# MAGIC 
# MAGIC ## Keyboard Shortcuts
# MAGIC - `F5`: Start debugging
# MAGIC - `F9`: Toggle breakpoint
# MAGIC - `F10`: Step over
# MAGIC - `F11`: Step into
# MAGIC - `Shift+F11`: Step out
# MAGIC - `Shift+F5`: Stop debugging


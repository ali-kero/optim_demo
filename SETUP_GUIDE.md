# Databricks Development Setup Guide

This guide will help you set up your local development environment to run and debug Databricks notebooks cell by cell.

## Prerequisites

- **VS Code** installed on your machine
- **Python 3.8+** installed
- Access to a **Databricks workspace**
- A **Databricks cluster** (can be shared or personal)

## Setup Steps

### 1. Install VS Code Extensions

Open VS Code and install these essential extensions:

1. **Databricks** (by Databricks)
   - Provides cell-by-cell execution
   - Remote debugging on Databricks clusters
   - Sync with Databricks workspace

2. **Python** (by Microsoft)
   - Python language support
   - IntelliSense and debugging

3. **Jupyter** (by Microsoft)
   - Notebook support in VS Code
   - Interactive cell execution

To install, press `Cmd+Shift+X` (Mac) or `Ctrl+Shift+X` (Windows/Linux) and search for each extension.

### 2. Create Virtual Environment

```bash
# Navigate to your project directory
cd /Users/ali.karaouzene/workspace/demos/meetup/optim_demo

# Create a virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate  # Mac/Linux
# or
.venv\Scripts\activate  # Windows

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install Databricks Connect (matches your cluster's Databricks Runtime)
# For DBR 13.x (Spark 3.4.x)
pip install databricks-connect==13.3.0

# For DBR 14.x (Spark 3.5.x)
# pip install databricks-connect==14.3.0
```

### 3. Configure Databricks Authentication

#### Option A: Using Databricks CLI (Recommended)

```bash
# Install Databricks CLI
pip install databricks-cli

# Configure authentication
databricks configure --token

# You'll be prompted to enter:
# - Databricks Host: https://your-workspace.cloud.databricks.com
# - Token: Your personal access token
```

#### Option B: Using Environment Variables

```bash
# Copy the template
cp env.template .env

# Edit .env with your values
# DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
# DATABRICKS_TOKEN=your-token-here
# DATABRICKS_CLUSTER_ID=your-cluster-id
```

### 4. Get Your Personal Access Token

1. Go to your Databricks workspace
2. Click on your profile icon (top right)
3. Select **Settings** → **Developer** → **Access tokens**
4. Click **Generate new token**
5. Give it a name (e.g., "VS Code Development")
6. Set expiration (90 days recommended)
7. Click **Generate**
8. **Copy the token** (you won't be able to see it again!)

### 5. Find Your Cluster ID

```bash
# List all clusters
databricks clusters list

# Or find it in the Databricks UI:
# 1. Go to Compute page
# 2. Click on your cluster
# 3. The cluster ID is in the URL: /compute/clusters/<cluster-id>
```

### 6. Configure VS Code Databricks Extension

1. Open VS Code
2. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
3. Type "Databricks: Configure"
4. Select your authentication method
5. Enter your workspace URL and token

### 7. Connect to Your Cluster

1. Open `sample_notebook.py`
2. Look at the bottom right of VS Code
3. Click on the kernel selector
4. Choose "Databricks" as the kernel
5. Select your cluster

## Usage

### Running Cells Interactively

1. **Open a Python file** with Databricks notebook format (cells separated by `# COMMAND ----------`)
2. **Click "Run Cell"** or use shortcuts:
   - `Shift+Enter`: Run current cell and move to next
   - `Ctrl+Enter`: Run current cell
   - `Alt+Enter`: Run current cell and insert below

### Debugging

1. **Set breakpoints** by clicking left of line numbers
2. **Start debugging**:
   - Press `F5` or
   - Click "Run" → "Start Debugging" or
   - Select "Databricks: Debug Python File on Cluster" from debug menu
3. **Debug on remote cluster**: Your code runs on Databricks with full debugging capabilities!

### Syncing with Databricks Workspace

The Databricks extension can sync your local files to your workspace:

```bash
# Push local changes to Databricks
# Command Palette → "Databricks: Sync Workspace"
```

Alternatively, use **Databricks Repos** for Git integration:
1. In Databricks workspace, go to Repos
2. Click "Add Repo"
3. Connect your GitHub repository
4. Your changes will sync automatically!

## Alternative: Databricks Connect Configuration

If you want to run PySpark code locally that executes on a remote Databricks cluster:

```python
# Create a config file: ~/.databrickscfg
# Or configure programmatically:

from databricks.connect import DatabricksSession

spark = DatabricksSession.builder \
    .remote(
        host="https://your-workspace.cloud.databricks.com",
        token="your-token",
        cluster_id="your-cluster-id"
    ) \
    .getOrCreate()

# Now you can run Spark code locally that executes remotely!
df = spark.sql("SELECT * FROM my_table")
df.show()
```

## Troubleshooting

### Issue: "Cannot connect to cluster"
- Verify cluster is running
- Check cluster ID is correct
- Ensure token has not expired

### Issue: "Module not found"
- Install packages on your cluster: `%pip install package-name`
- Or add to cluster libraries in Databricks UI

### Issue: "Authentication failed"
- Regenerate your personal access token
- Update your `.env` file or `~/.databrickscfg`

### Issue: "Cells not recognized"
- Ensure cells are separated by `# COMMAND ----------`
- Install Jupyter extension in VS Code

## Best Practices

1. **Use Git branches** for different features
2. **Test locally** with small datasets before running on cluster
3. **Use %pip and %conda** magic commands for package management
4. **Set up CI/CD** with Databricks Asset Bundles
5. **Use secrets** instead of hardcoding credentials
6. **Version your notebooks** with Git

## Resources

- [Databricks VS Code Extension Docs](https://docs.databricks.com/dev-tools/vscode-ext.html)
- [Databricks Connect Docs](https://docs.databricks.com/dev-tools/databricks-connect.html)
- [Databricks Asset Bundles](https://docs.databricks.com/dev-tools/bundles/index.html)

## Quick Reference Commands

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure Databricks CLI
databricks configure --token

# List clusters
databricks clusters list

# Deploy with Databricks Asset Bundles
databricks bundle deploy

# Run bundle
databricks bundle run
```

## Need Help?

- Check the [Databricks Community](https://community.databricks.com/)
- Review [VS Code Extension Changelog](https://marketplace.visualstudio.com/items?itemName=databricks.databricks)
- Contact your Databricks administrator

Happy coding! 🚀


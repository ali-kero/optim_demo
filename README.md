# Databricks Optimization Demo

This repository contains Databricks notebooks and resources for demonstrating optimization techniques with **local development and debugging support**.

## 🚀 Quick Start

### For Local Development with Debugging

**See the [SETUP_GUIDE.md](SETUP_GUIDE.md) for complete instructions!**

Quick setup:
```bash
# 1. Install VS Code extensions: Databricks, Python, Jupyter
# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure Databricks
databricks configure --token
```

### For Databricks Workspace Only

1. Import the notebook into your Databricks workspace
2. Attach it to a running cluster
3. Run the cells sequentially

## Contents

- `sample_notebook.py` - A sample Databricks notebook demonstrating basic Spark operations, data analysis, and visualization
- `SETUP_GUIDE.md` - **Complete guide for setting up local development with debugging**
- `.vscode/` - VS Code configuration for Databricks development
- `databricks.yml` - Databricks Asset Bundle configuration

## Prerequisites

- Databricks workspace
- Access to a Databricks cluster
- Python 3.8+
- VS Code (recommended for local development)

## Notebook Structure

The sample notebook includes:

- **Setup and Configuration**: Initialize Spark and display configuration
- **Sample Data Creation**: Create a sample employee dataset
- **Data Analysis**: Perform aggregations and calculations
- **Data Visualization**: Create visual representations of the data
- **Advanced Analytics**: Apply classification and categorization
- **Summary Statistics**: Generate statistical summaries

## Development

To make changes to the notebooks:

1. Clone this repository
2. Make your changes
3. Commit and push to the repository
4. Sync with your Databricks workspace

## License

MIT License


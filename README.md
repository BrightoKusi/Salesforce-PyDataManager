# salesforce-data-manipulation
demo on the extraction and manipulation of data of salesforce object data using simple-salesforce REST API

# Salesforce Data Management Scripts

## Introduction

These Python scripts are designed to interact with Salesforce to perform various data management tasks such as querying metadata, exploring Salesforce instance attributes, and exporting data to CSV files.

## Scripts

1. `index.py`: This script connects to Salesforce, queries account information, explores Salesforce instance attributes, retrieves metadata, and writes metadata and account information to CSV files.

2. `data_manipulation.py`: This script connects to Salesforce, reads lead information, inserts new lead records, updates email addresses for existing leads, and deletes specified lead records.

## Requirements

- Python 3.x
- `simple_salesforce` library (install via `pip install simple-salesforce`)
- `pandas` library (install via `pip install pandas`)

## Usage

1. Ensure Python and required libraries are installed on your system.
2. Create a `.env` file in the same directory as the scripts and add Salesforce login information in the following format:

    ```
    [SfLoginInfo]
    username = YourSalesforceUsername
    password = YourSalesforcePassword
    security_token = YourSalesforceSecurityToken
    ```

3. Run the scripts using Python. For example:

    ```
    python salesforce_data_query.py
    ```

4. The scripts will perform the specified operations and generate output files as described in the script comments.

## Notes

- These scripts are intended for demonstration and educational purposes. Use them responsibly and ensure compliance with Salesforce API usage policies.
- Error handling is included, but further customization may be required for production use.
- Feel free to modify the scripts to suit your specific Salesforce data management needs.


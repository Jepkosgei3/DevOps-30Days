# NBA Data Lake Setup with AWS S3, Glue, and Athena

This project demonstrates how to create a data lake in AWS for NBA sports analytics using several AWS services, including S3, Glue, and Athena. The goal is to set up an automated pipeline that fetches NBA data, stores it in S3, registers the data in AWS Glue, and enables querying via Athena.

## Features

- **S3 Bucket**: Store NBA data as JSON files.
- **AWS Glue**: Create a Glue database and tables to organize the data.
- **Athena**: Set up Athena to query the NBA data using SQL.
- **Data Fetching**: Fetch NBA player data from the SportsData.io API.

## Prerequisites

Before running the script, you need to set up the following:

1. **AWS Account**:
   - AWS S3 Bucket.
   - AWS Glue database and tables.
   - AWS Athena setup.
   
2. **Python Packages**:
   Install the required Python packages using `pip`:
   ```bash
   pip install boto3 requests python-dotenv
3. **Environment Variables:**:
   Create a .env file in the root directory of your project and add the following variables:
   '''SPORTS_DATA_API_KEY=your_sportsdata_api_key
   NBA_ENDPOINT=https://api.sportsdata.io/v3/nba/scores/json/Players'''
4. **IAM Role**:
   Ensure the IAM role used has the following permissions:

    * s3:DeleteObject, s3:DeleteBucket
    * glue:DeleteTable, glue:DeleteDatabase
    * athena:StartQueryExecution, athena:GetQueryResults
Setup
1. Create S3 Bucket
The create_s3_bucket() function will create an S3 bucket to store raw NBA player data. The bucket is named "sports-analytics-data-lake" by default, but you can change it in the script.

2. Fetch NBA Data
The script uses the SportsData.io API to fetch NBA player data. The data is saved in a line-delimited JSON format.

3. Store Data in S3
After fetching the NBA data, the script uploads it to the S3 bucket created earlier under the key raw-data/nba_player_data.jsonl.

4. Create Glue Database and Table
The create_glue_database() and create_glue_table() functions set up a Glue database and table for organizing the NBA data.

5. Configure Athena
The configure_athena() function configures Athena to query the data stored in the S3 bucket by specifying an output location for query results.

6. Running the Script
'''python3 nba_data_lake.py'''
This will create the S3 bucket, fetch the NBA data, upload it to S3, and configure the Glue and Athena resources.
Cleanup
The delete_all.py script provides functionality to delete the created resources:

Delete S3 Bucket and its contents.
Delete Glue Database and its tables.
Delete Athena query results stored in the S3 bucket.
Run the script using:

'''python3 delete_all.py'''



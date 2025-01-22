# Event-Driven Architecture with EventBridge: Automating Golf Tournament Data Fetching

Event-driven architecture (EDA) has revolutionized the way modern applications handle data. By reacting to events as they occur, EDA enables seamless integration and automation across services. In this blog, we’ll explore how to build an event-driven architecture using AWS EventBridge to automate the fetching of upcoming golf tournament data via an API. The data will be processed and published using AWS Lambda and Amazon SNS.

---

## Step-by-Step Guide

### 1. Create an SNS Topic

#### Purpose:
The SNS topic will distribute the golf tournament updates to all subscribers.

#### Steps:
1. Navigate to the **Amazon SNS** console.
2. Create a new topic:
   - Name: `GolfTournamentUpdates`
   - Type: **Standard**.
3. Add subscriptions:
   - Choose the subscription protocol (e.g., Email, SMS).
   - Example: Add your email address to receive updates.

### 2. Create an IAM Policy to Access the SNS Topic

#### Purpose:
Allow the Lambda function to publish messages to the SNS topic.

#### Steps:
1. Go to the **IAM** console.
2. Create a new policy:
   - Use the JSON editor to define the policy:
     ```json
     {
       "Version": "2012-10-17",
       "Statement": [
         {
           "Effect": "Allow",
           "Action": "sns:Publish",
           "Resource": "arn:aws:sns:REGION:ACCOUNT_ID:GolfTournamentUpdates"
         }
       ]
     }
     ```
   - Replace `REGION` and `ACCOUNT_ID` with your AWS region and account ID.
3. Save the policy with a descriptive name, e.g., `SNSPublishPolicy`.

### 3. Create a Lambda Role and Attach Policies

#### Purpose:
The role grants the Lambda function permissions to execute and access SNS.

#### Steps:
1. Navigate to the **IAM** console.
2. Create a new role:
   - Use case: **AWS Lambda**.
3. Attach the following policies to the role:
   - `AWSLambdaBasicExecutionRole`
   - The `SNSPublishPolicy` created earlier.
4. Save the role with a descriptive name, e.g., `LambdaSNSRole`.

### 4. Create a Lambda Function

#### Purpose:
Fetch, process, and publish golf tournament data.

#### Steps:
1. Go to the **AWS Lambda** console.
2. Create a new function:
   - Runtime: Python 3.x.
   - Handler: `lambda_function.lambda_handler`.
3. Set environment variables:
   - `GOLF_API_KEY`: Your API key.
   - `SNS_TOPIC_ARN`: ARN of the SNS topic created earlier.
4. Use the following Lambda function code:

```python
import os
import json
import urllib.request
import boto3
from datetime import datetime

def lambda_handler(event, context):
    # Get environment variables
    api_key = os.getenv("GOLF_API_KEY")
    sns_topic_arn = os.getenv("SNS_TOPIC_ARN")
    sns_client = boto3.client("sns")

    # Fetch data from the API
    api_url = f"https://api.sportsdata.io/v3/golf/scores/json/Tournaments?key={api_key}"
    try:
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching data: {e}")
        return {"statusCode": 500, "body": "Error fetching data"}

    # Filter tournaments for 2025
    tournaments_2025 = [
        t for t in data
        if t.get("StartDate", "").startswith("2025") or t.get("EndDate", "").startswith("2025")
    ]

    if not tournaments_2025:
        print("No tournaments found for 2025.")
        return {"statusCode": 200, "body": "No tournaments for 2025."}

    # Format the data
    messages = [
        f"Tournament: {t['Name']}\nStart Date: {t['StartDate']}\nEnd Date: {t['EndDate']}\nVenue: {t.get('Venue', 'Unknown')}\nLocation: {t.get('Location', 'Unknown')}\n"
        for t in tournaments_2025
    ]
    final_message = "\n---\n".join(messages)

    # Publish to SNS
    try:
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=final_message,
            Subject="Upcoming Golf Tournaments for 2025"
        )
        print("Message published to SNS successfully.")
    except Exception as e:
        print(f"Error publishing to SNS: {e}")
        return {"statusCode": 500, "body": "Error publishing to SNS"}

    return {"statusCode": 200, "body": "Data processed and sent to SNS"}
```

5. Deploy the code.

### 5. Create an EventBridge Rule

#### Purpose:
Schedule the Lambda function to run once a month to fetch upcoming tournaments.

#### Steps:
1. Navigate to the **Amazon EventBridge** console.
2. Create a new rule:
   - Name: `fetch-golf-tournaments`.
   - Event Source: **Schedule**.
   - Schedule Expression: `cron(0 0 1 * ? *)` (runs at midnight UTC on the 1st day of every month).
3. Target:
   - Select **Lambda function**.
   - Choose the Lambda function you created.

---

## Benefits of Event-Driven Architecture

1. **Automation**: By using EventBridge, the process is entirely automated, requiring no manual intervention.
2. **Scalability**: AWS services like Lambda and SNS handle scaling automatically.
3. **Cost-Efficiency**: You only pay for what you use, with no need to maintain servers.
4. **Decoupling**: Event-driven systems reduce tight coupling between components, making the system more modular and easier to maintain.

---

## Conclusion

By leveraging AWS EventBridge, Lambda, and SNS, we’ve built a robust and automated event-driven architecture for fetching and distributing golf tournament data. This approach not only ensures timely updates but also highlights the power of modern serverless technologies in simplifying complex workflows.

Feel free to try this architecture in your projects and modify it to suit your specific needs. Happy coding!


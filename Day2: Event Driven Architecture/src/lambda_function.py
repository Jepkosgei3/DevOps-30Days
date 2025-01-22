import os
import json
import urllib.request
import boto3
from datetime import datetime, timezone

def format_course_data(course):
    tournament_id = course.get("TournamentID", "Unknown")
    name = course.get("Name", "Unknown")
    start_date = course.get("StartDate", "Unknown")
    end_date = course.get("EndDate", "Unknown")
    venue = course.get("Venue", "Unknown")
    location = course.get("Location", "Unknown")
    par = course.get("Par", "N/A")
    yards = course.get("Yards", "N/A")
    purse = course.get("Purse", "N/A")
    city = course.get("City", "Unknown")
    state = course.get("State", "Unknown")
    zip_code = course.get("ZipCode", "Unknown")
    country = course.get("Country", "Unknown")
    time_zone = course.get("TimeZone", "Unknown")
    format_ = course.get("Format", "Unknown")

    return (
        f"Tournament: {name} (ID: {tournament_id})\n"
        f"Venue: {venue}, {location}\n"
        f"Dates: {start_date} to {end_date}\n"
        f"Par: {par}, Yards: {yards}, Purse: ${purse}\n"
        f"City: {city}, State: {state}, Zip Code: {zip_code}, Country: {country}\n"
        f"Time Zone: {time_zone}, Format: {format_}\n"
    )

def lambda_handler(event, context):
    # Get environment variables
    api_key = os.getenv("GOLF_API_KEY") #stored in env variables
    sns_topic_arn = os.getenv("SNS_TOPIC_ARN") #stored in env variables
    sns_client = boto3.client("sns")
    
    # Current date in UTC
    utc_now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"Fetching golf courses for date: {utc_now}")
    
    # Fetch data from the API
    api_url = f"https://api.sportsdata.io/golf/v2/json/Courses?key={api_key}"
    
    try:
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read().decode())
            print(json.dumps(data, indent=4))  # Debugging: log the raw data
    except Exception as e:
        print(f"Error fetching data from API: {e}")
        return {"statusCode": 500, "body": "Error fetching data"}
    
    # Filter tournaments for dates in 2025
    tournaments_2025 = [
        course for course in data 
        if (course.get("StartDate", "").startswith("2025") or course.get("EndDate", "").startswith("2025"))
    ]
    
    if not tournaments_2025:
        print("No tournaments found for 2025.")
        return {"statusCode": 200, "body": "No tournaments available for 2025."}
    
    # Format the data
    messages = [format_course_data(course) for course in tournaments_2025]
    final_message = "\n---\n".join(messages)
    
    # Publish to SNS
    try:
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=final_message,
            Subject="Golf Tournament Updates for 2025"
        )
        print("Message published to SNS successfully.")
    except Exception as e:
        print(f"Error publishing to SNS: {e}")
        return {"statusCode": 500, "body": "Error publishing to SNS"}
    
    return {"statusCode": 200, "body": "Data processed and sent to SNS"}

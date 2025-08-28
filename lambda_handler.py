import json
import requests
import random

def post_req(url, data, headers=None):
    """
    Helper function to make POST requests
    
    Args:
        url (str): The URL to send the POST request to
        data (dict): The data to send in the request
        headers (dict, optional): Headers to include in the request
        
    Returns:
        dict: The JSON response from the request
    """
    try:
        if headers:
            response = requests.post(url, json=data, headers=headers)
        else:
            response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        print(f"Error making request to {url}: {str(e)}")
        return {"error": str(e)}

def lambda_handler(event, context):
    """
    Lambda function that handles API Gateway requests.
    Processes the payload and sends data to webhooks.
    
    Args:
        event (dict): The event payload from API Gateway
        context (object): Lambda context object
        
    Returns:
        dict: API Gateway response with 200 status code
    """
    # Print the received payload
    print(f"Received payload: {json.dumps(event)}")
    
    try:
        # Parse the body if it's a string
        if isinstance(event.get('body'), str):
            body_data = json.loads(event.get('body', '{}'))
        else:
            body_data = event.get('body', {})
        
        log = body_data.get('log')
        # Extract data from the request body
        data = {
            "summary": body_data.get("extractions", {}).get("summary", "No summary available"),
            "callback": body_data.get("callback", "False"),
            "disposition_id": body_data.get("extractions", {}).get("disposition_id", "0"),
            "first_name": body_data.get("extractions", {}).get("first_name", "Unknown"),
            "last_name": body_data.get("extractions", {}).get("last_name", "Unknown"),
            "phone_number": body_data.get("from_number", "Unknown"),
            "vehicle_year": body_data.get("extractions", {}).get("vehicle_year", "Unknown"),
            "vehicle_model": body_data.get("extractions", {}).get("vehicle_model", "Unknown"),
            "vechicle_make": body_data.get("extractions", {}).get("vehicle_make", "Unknown"),
            "recording": body_data.get("recording_url", ""),
            "transcript": body_data.get("transcript", ""),
            "call_status": body_data.get("extractions", {}).get("call_status", "completed"),
            "call_id": body_data.get("log_id", ""),
            "start_time": body_data.get("start_timestamp", ""),
            "end_time": body_data.get("end_timestamp", ""),
            "sentiment": body_data.get("extractions", {}).get("sentiment", "Unknown"),
            "email_address": "Unknown",
            "vehicle_make": body_data.get("extractions", {}).get("vehicle_make", "Unknown"),
            "appointment_date": "Unknown",
            "disposition": body_data.get("extractions", {}).get("disposition_name", "Unknown"),
            "transportation_type": "Unknown",
            "callback_time": "Unknown",
            "has_multiple_accounts": "False",
            "book_appointment_error": "None",
            "campaign_id": body_data.get("extractions", {}).get("campaign_id", "Unknown"),
            "dealer_id": body_data.get("extractions", {}).get("dealer_id", "Unknown"),
        }
        
        # Make the first webhook request
        lucy_webhook_res = post_req(
            url="https://apps.dgaauto.com/lucyWebhookAlert/webhook", 
            data={
                "campaign_id": data['campaign_id'], 
                "agent_comments": data['summary'], 
                "call_back": data['callback'], 
                "call_disposition_id": data["disposition_id"], 
                "advisor": "", 
                "dealer_id": data['dealer_id'], 
                "first_name": data['first_name'], 
                "last_name": data["last_name"], 
                "phone": data["phone_number"], 
                "vehicle_year": data['vehicle_year'], 
                "vehicle_model": data["vehicle_model"], 
                "vehicle_make": data['vechicle_make']
            }
        )
        print("LUCY WEBHOOK Data: ", {
                "campaign_id": data['campaign_id'], 
                "agent_comments": data['summary'], 
                "call_back": data['callback'], 
                "call_disposition_id": data["disposition_id"], 
                "advisor": "", 
                "dealer_id": data['dealer_id'], 
                "first_name": data['first_name'], 
                "last_name": data["last_name"], 
                "phone": data["phone_number"], 
                "vehicle_year": data['vehicle_year'], 
                "vehicle_model": data["vehicle_model"], 
                "vehicle_make": data['vechicle_make']
            })
        # Make the second webhook request
        row_id = str(random.randint(10000000, 99999999))
        obj = {"functions": json.dumps(event.get("requestContext", {}))}
        
        reporting_res = post_req(
            url="https://apps.dgaauto.com/virtualAgentDataImport/webhook", 
            headers={"x-api-key": "$2a$11$5GHNF.BbEILij03XRr163eV0lrbRGu6Rq.jlycXAvB.fddAZkO5GK"}, 
            data={
                "id": row_id, 
                "api_logs": log,
                "campaign_id": data['campaign_id'],  
                "recording": data["recording"], 
                "api_logs": obj['functions'],
                "transcript": data['transcript'], 
                "call_status": data['call_status'], 
                "call_id": data['call_id'], 
                "start_time": data['start_time'], 
                "end_time": data['end_time'], 
                "first_name": data["first_name"], 
                "last_name": data["last_name"], 
                "phone_number": data["phone_number"], 
                "sentiment": data["sentiment"], 
                "email_address": data["email_address"], 
                "vehicle_make": data["vehicle_make"], 
                "vehicle_model": data["vehicle_model"], 
                "vehicle_year": data["vehicle_year"], 
                "appointment_date": data["appointment_date"], 
                "summary": data["summary"], 
                "disposition": data["disposition"], 
                "disposition_id": data["disposition_id"], 
                "transportation_type": data["transportation_type"], 
                "callback_time": data["callback_time"], 
                "callback": data["callback"], 
                "has_multiple_accounts": data["has_multiple_accounts"], 
                "book_appointment_error": data["book_appointment_error"]
            }
        )
        print("REPORTING WEBHOOK DATA: ", {
                "id": row_id, 
                "campaign_id": data['campaign_id'],  
                "recording": data["recording"], 
                "api_logs": obj['functions'],
                "transcript": data['transcript'], 
                "call_status": data['call_status'], 
                "call_id": data['call_id'], 
                "start_time": data['start_time'], 
                "end_time": data['end_time'], 
                "first_name": data["first_name"], 
                "last_name": data["last_name"], 
                "phone_number": data["phone_number"], 
                "sentiment": data["sentiment"], 
                "email_address": data["email_address"], 
                "vehicle_make": data["vehicle_make"], 
                "vehicle_model": data["vehicle_model"], 
                "vehicle_year": data["vehicle_year"], 
                "appointment_date": data["appointment_date"], 
                "summary": data["summary"], 
                "disposition": data["disposition"], 
                "disposition_id": data["disposition_id"], 
                "transportation_type": data["transportation_type"], 
                "callback_time": data["callback_time"], 
                "callback": data["callback"], 
                "has_multiple_accounts": data["has_multiple_accounts"], 
                "book_appointment_error": data["book_appointment_error"]
            })
        
        # Log the response
        print(f"Lucy webhook response: {json.dumps(lucy_webhook_res)}")
        print(f"Reporting webhook response: {json.dumps(reporting_res)}")
        
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": str(e)
            })
        }
    
    # Return a successful response
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "message": "Request processed successfully",
            "lucy_webhook_status": "sent",
            "reporting_webhook_status": "sent"
        })
    } 
## Brainbase Version 2 Webhook Tutorial

Webhooks in Version 2 work similar to many other providers.


### Setting a Custom Webhook

#### Setting a Custom Webhook via API

Via our API, you can set up a custom webhook using the following `curl` request:

```bash
curl --location 'https://brainbase-monorepo-api.onrender.com/api/workers/{WORKER_ID}/deployments/{DEPLOYMENT_ID}/voice/customWebhooks' \
--header 'Content-Type: application/json' \
--header 'x-api-key: {YOUR_API_KEY}' \
--data '{
  "name": "Webhook for data",
  "url": "{YOUR_WEBHOOK_API_ENDPOINT}",
  "method": "POST",
  "fields": "recording_url,transcript,duration_ms,sentiment,start_timestamp,end_timestamp,from_number,summary,callback,last_name,first_name,disposition_id,disposition_name"
}'
```

You can find your WORKER_ID and DEPLOYMENT_ID in the URL of your worker deployment you are referencing, for example:

https://beta.usebrainbase.com/dashboard/workers/worker_XXX/deployments/deploy_XXXXX

or under the settings tab of the worker overview at the very top.

You can find or generate your api keys under the settings tab on the home page: https://beta.usebrainbase.com/dashboard/settings

Your WEBHOOK_API_ENDPOINT is the endpoint you wish to recieve the webhook at. 

The **fields** parameter is where you define the fields you wish to recieve in the webhook. 

These fields can be the name of your extraction AND/OR any of the following:

* 

#### Setting a Custom Webhook via Client

COMING SOON

### Example Payload You May Receive

```json
{
  "recording_url": "https://dxc03zgurdly9.cloudfront.net/716024c3fd8937709a1810791764c3073d2f4b18df064a3734568bcc61e95020/recording.wav",
  "transcript": "Agent: Thank you for calling Warsaw Autoplex, my name is Chloe. Please note, this call is being recorded to ensure you are having an excellent customer experience. What can I help you with today?\nUser: Parts department.\nAgent: Just to confirm, would you like me to transfer you to the Parts Department?\nUser: Yes.\nAgent: Please hold while I transfer you to the Parts Department.\n",
  "duration_ms": 30216,
  "sentiment": "0.5",
  "start_timestamp": 1748520331698,
  "end_timestamp": 1748520361914,
  "from_number": "+15747734624",
  "summary": "The caller requested to be transferred to the Parts Department at Warsaw Autoplex. The agent confirmed the request and proceeded with the transfer to the Parts Department.",
  "callback": "False",
  "disposition_id": "168",
  "disposition_name": "Transferred to Dealer - Parts Department",
  "webhook_id": "cmawyhb770000s831e7up51jz",
  "log_id": "log_36b1fd87-ec3c-4890-a080-37d55fc5a0bf",
  "deployment_id": "deploy_b0f49ed6-5dcc-4dad-99dd-0ca18c829f8d"
}
```

## DGA Specific Deployment Instructions

To integrate your existing webhook endpoints with our system, you have one of two options:

1. Merge all of the API endpoints into a single endpoint that can recieve the above payload

2. Deploy this repo on an AWS Lambda to use as a middleman to route the correct data to the correct endpoint, then deploy via API Gateway and use that Url as the YOUR_WEBHOOK_API_ENDPOINT

We are currently doing option 2 for you. 

Here is how you can deploy this and own this yourself.

Step 1: Fork this repo. Ensure you have Docker installed and setup on your computer. You can also zip this file and deploy it manually to AWS Lambda

Step 2: Create an ECR repo of any name and add it to the `deploy.sh` file. Also add your account ID and region:

```bash
AWS_ACCOUNT_ID="<YOUR_AWS_ACCOUNT_ID_HERE>"
AWS_REGION="<YOUR_REGION_HERE>"
ECR_REPO_NAME="<YOUR_ECR_REPO_NAME_HERE>"
IMAGE_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:latest"
```

Step 3: run `chmod +x deploy.sh` in your terminal (while navigated to this repo)

Step 4: run `./deploy.sh`

Step 5: Navigate to AWS ECR and locate the repo you created in Step 2. Find the latest Image, with a size greater than 0 (and NOT an Image Index). Remember the first 3-4 letters/numbers after its SHA. For example, `sha256:e968`

Step 6: Create a new Lambda function from a container image. When creating, click Browse Image and search for your ECR repo name. Then, select the image with the SHA from before (`sha256:e968`)

Step 7: After creating the image, select `Add Trigger +` on the Lambda, and add an Open, new HTTP API Gateway connection.

Step 8: Locate the API Gateway instance and copy this URL.

Now you can use this URL as the webhook URL. 
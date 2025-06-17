# Use the official AWS Lambda Python 3.9 base image
FROM public.ecr.aws/lambda/python:3.9

# Install dependencies
RUN pip install requests

# Copy function code
COPY lambda_handler.py ./

# Set the command to your handler name (i.e., file_name.function_name)
CMD [ "lambda_handler.lambda_handler" ]

# Face Recognition using Lambda

## Team -  DADCloud
- [@Dhairya Dudhatra](https://github.com/Dhairya-Dudhatra)
- [@Arush Patel](https://github.com/arushPatel10)
- [@Dirgh Patel](https://github.com/DIRGH712)

## Project Understandings
We tried to implement a face recognition application using AWS Lambda and AWS S3 and S3 event notification.
From the workload generator users upload videos in the S3 and event notifications trigger the lambda function which was created from the docker image stored in the AWS ECR.
Lambda handler detects the face using face recognition libraries and return the result in another S3 bucket. 


## Architecture
![Arch Image](https://github.com/Dhairya-Dudhatra/FaceRecognition-Lambda-S3/blob/main/arch.png)

## S3 Bucket Names
- Input Bucket name -  'input-bucket-project2'
- Output Bucket name - 'output-bucket-project2'

## DynamoDB Table Name
- Table Name - 'People_data'

import boto3
import uuid
import json

def lambda_handler(event, context):
    try:
        #Pulling data about the object that was placed into the bucket like the bucket name and the file name
        record = event['Records'][0]
        s3bucket = record['s3']['bucket']['name']
        s3object = record['s3']['object']['key']
        
        #Ensuring that the file contains some video format extension in the name
        if (not('.mp4' in s3object or '.mp3' in s3object or '.m4a' in s3object)):
            print(s3object + ' is not a video') 
            return
        
        
        #Generating the URI for the file 
        s3Path = "s3://" + s3bucket + "/" + s3object
        #Because the files are uploaded to uploads/<file-name>, this will remove the uploads/ prefix and only give the file name.
        jobName = s3object.split('/')[-1]
        
        
        #Setting up a transcribe client to request the job
        client = boto3.client('transcribe')
        
        #Requesting the transcription job using information gathered above and sending that to the output bucket in the /json directory.
        response = client.start_transcription_job(
            TranscriptionJobName=jobName,
            LanguageCode='en-US',
            MediaFormat='mp4'or'm4a'or 'mp3',
            Media={
                'MediaFileUri': s3Path
            },
            OutputBucketName = "capstone-transcribe-output",
            OutputKey = "json/"
        )
        
        
        
        return {
            
            'TranscriptionJobName': response['TranscriptionJob']['TranscriptionJobName']
        }
    #try except block will try to run the entire program, and if any exception is faced, the exception is printed(to cloudwatch logs). Otherwise, job is completed successfully.
    except Exception as e:
        print(e)
        return
import json
import boto3

def lambda_handler(event, context):
    try:
        #Setting up a client to access S3. 
        s3Client = boto3.client('s3')
        #Gathering information about the object placed in the bucket
        record = event['Records'][0]
        s3bucket = record['s3']['bucket']['name']
        s3object = record['s3']['object']['key'] #.split('/')[-1]
        
        print(s3object)
        #Printing out the object to be pulled from the specific S3 bucket
        print('Bucket = ' + s3bucket + ' ' + 'Key = ' + s3object)
        
        #Response from S3 containing information about the downloaded object
        s3Response = s3Client.get_object(Bucket=s3bucket , Key=s3object )
        
        #Loading the 'Body' of the repsonse into a json file. The body is the file itself. In this case, the JSON transcription. 
        #Note: 'Body' is formatted in bytes by default. By using method read(), we are able to translate the bytes to a string. The string(in JSON Format) is then loaded into a JSON object.
        responseJSON = json.loads(s3Response['Body'].read())
        
        #From the file, pulling out the transcription
        
        output = responseJSON['results']['transcripts'][0]['transcript']

        #filename will be the same as the jobname, only appending .html to the end
        filename = 'transcriptions/' + s3object[5:-5] + '.html'
        
        print(filename)
        print(output)
        
        #Building html string
        htmlFile = '<html>' + output + '</html>'
    
        #Gathering the response data from the put_object commmand.        
        putObjectResponse = s3Client.put_object ( 
                                                Bucket= s3bucket , 
                                                Key=filename, 
                                                Body=htmlFile.encode(), #Encode will translate the html string to bytes, the required format for 'Body' 
                                                ACL= 'public-read',
                                                ContentType='text/html' 
                                                #Because we encoded the body to be in bytes, we need to specify that even though it's bytes, it should be read as an html file.
        )
        
        
    except Exception as e:
        print(e)
        return

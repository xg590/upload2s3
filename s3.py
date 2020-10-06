#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import cgi, cgitb; cgitb.enable()
form = cgi.FieldStorage()
Key         = form['Key'].value
ExpiresIn   = form['ExpiresIn'].value
region_name = form['region_name'].value
Bucket      = form['Bucket'].value

import csv
with open('access_key.csv') as f:
    aws_access_key_id, aws_secret_access_key = [i for i in csv.reader(f)][1]

import sys
sys.path.append('/var/www/module_for_cgi')
import boto3
from botocore.config import Config
session = boto3.Session(region_name           = region_name          ,
                        aws_access_key_id     = aws_access_key_id    ,
                        aws_secret_access_key = aws_secret_access_key)
client = session.client(service_name = 's3',
                        config       = Config(signature_version='s3v4'))
download_link = client.generate_presigned_url(ClientMethod = 'get_object',
                                              Params       = {'Bucket': Bucket, 'Key': Key},
                                              ExpiresIn    = int(ExpiresIn) * 60)
upload_link   = client.generate_presigned_post(Bucket      = Bucket,
                                               Key         = Key,
                                               ExpiresIn   = int(ExpiresIn) * 60)

input_field = ''.join([f'<input type="hidden" name="{i}" value="{j}" />' for i, j in upload_link['fields'].items()])
 
print(f'''Content-type:text/html

<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  </head>
  <body>
    <form action="{upload_link['url']}" method="post" enctype="multipart/form-data">
      {input_field}
      <input type="file"   name="file" style="height: 200px; width: 400px"/> <br />
      <input type="submit" name="submit" value="Upload to Amazon S3" style="height: 200px; width: 400px"/>
    </form>
  <br>Upload your file then you can share the following link so everyone can download it.<br>
  <a href="{download_link}">{download_link}</a>
  </body>
</html>''')

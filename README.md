# upload2s3 
* This web app should run on a seperate host, and it can guide the user upload file to AWS S3 via any browser.
* The web app host retains no file but signs upload and download urls. 
## Architecture
1. A static webpage contains a form of parameters (key, bucket, region, expire) for generating presign urls.
2. Fill the form and submit it to the back-end python via any browser.
3. Python signs urls for upload and download according to parameters.
4. Python return a generated upload webpage that uses the upload url and display the download url.
5. Upload file to AWS S3 via the upload webpage directly.
## Screenshot
![alt text](https://github.com/xg590/upload2s3/raw/main/screenshot.png "s3") 
## Usage
1. Create a private bucket on AWS S3. 
```python
region_name    = 'ap-northeast-2'
Bucket         = 'mybucketname2077'   # Only alphanumericals
access_key_csv = 'access_key.csv'     # Path to Your Key File

import csv, boto3
with open(access_key_csv) as f: aws_access_key_id, aws_secret_access_key = [i for i in csv.reader(f)][1] 
from botocore.config import Config
session = boto3.Session(region_name = region_name , aws_access_key_id = aws_access_key_id , aws_secret_access_key = aws_secret_access_key)
client = session.client(service_name = 's3', config = Config(signature_version='s3v4'))
_ = client.create_bucket(Bucket=Bucket, CreateBucketConfiguration={ 'LocationConstraint': region_name }, )
_ = client.put_public_access_block(Bucket=Bucket, PublicAccessBlockConfiguration={ 'BlockPublicAcls': True, 'IgnorePublicAcls': True, 'BlockPublicPolicy': True, 'RestrictPublicBuckets': True })
```
2. Install apache2, boto3 python library on a host machine.
3. Enable cgid module of apache2 on the host. 
```shell
# As root
apt install -y apache2 python3 python3-pip
pip3 install --target /var/www/module_for_cgi boto3
a2enmod cgid
systemctl restart apache2
```
4. Put the s3.html in an apache2 dirctory /var/www/html 
```shell
# As root 
wget https://raw.githubusercontent.com/xg590/upload2s3/main/s3.html -O /var/www/html/s3.html
```
5. Put the s3.py in an cgi-bin dirctory /usr/lib/cgi-bin 
```python
# As root
wget https://raw.githubusercontent.com/xg590/upload2s3/main/s3.py -O /usr/lib/cgi-bin/s3.py 
chmod o+x /usr/lib/cgi-bin/s3.py
```
6. Put the aws access key in /usr/lib/cgi-bin too.   
```shell
# As root
cat << EOF > /usr/lib/cgi-bin/access_key.csv
Access key ID,Secret access key
AKIAJDWIOJDWBRKQW,im89hw31b89h24UEBGWD9
EOF
chown www-data:www-data /usr/lib/cgi-bin/access_key.csv
chmod 600 /usr/lib/cgi-bin/access_key.csv # ensure nobody except root or apache2 can access the secret 
```

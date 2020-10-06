# upload2s3 
* This web app should run on a seperate host, and it can guide the user upload file to AWS S3 via any browser.
* The web app host retains no file but signs upload and download urls. 
## Architecture
1. A static webpage contains a form of parameters (key, bucket, region, expire) for generating presign urls.
2. Fill the form and submit it to the python via any browser.
3. Python signs urls for upload and download according to parameters.
4. Python return a upload webpage that uses the upload url and display the download url.
5. Upload file to AWS S3 via the upload webpage directly.
## Screenshot
![alt text](https://github.com/xg590/upload2s3/raw/main/screenshot.png "s3") 
## Usage
TBC

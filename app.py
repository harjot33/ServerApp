from queue import Empty
from urllib import response
from flask import Flask, jsonify,render_template, request, redirect, url_for, session, logging,Response
import boto3
import os, requests
import datetime

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
s3 = boto3.resource(
    's3',
    region_name='us-east-1',
    aws_access_key_id="ASIA52YPANNBK7GJ35F4",
    aws_secret_access_key="7763hkM1BaXEm2ZdhzVIwWU77PB5euQbeH+bSiXi",
    aws_session_token="FwoGZXIvYXdzENz//////////wEaDHofZOMxcL6cLj8EkyLAAdsqBhEr8x4mQCXCPq9CP3YrA8Y5hz7IEY0vA09gBK8sW2J4oKuYvaSdlz5+oiNCOvemgeKiNuHkNFul98LweNl6iYn1je5jr3LJtYED/95vFggQOf/glx0MFOdyr1GwTQp9Ycls/iot/wfXoTV912CVmnFjoUhnlvlfSH3pgcdv4Y37B5gbyZnALHajJnuOsN7CEX1rILDCov5UIQM4We8tnFanKtL3KH1c/mE4LqxlKHQQUa5WY7uOuKVeyU56QSjP6P6QBjItKeA1U9SETKAOMPSylwQzfDdtn7L1RGvkrjkYV9RBoSJE8RnPVLIuPi9wyoJG"
)

initial = {
"banner": "<Replace with your Banner ID, e.g. B00123456>",
"ip": ""
}



@app.route('/storedata',methods=['POST'])
def sendword():
    if request.method == 'POST':
        content = request.get_json(force=True)
        data=content['data']
        res = s3.Object('cloudcomputinga2harjot', 'newfile.txt').put(Body=data,ACL='public-read')
        res1 = res['ResponseMetadata']
        if(res1['HTTPStatusCode']==200):
            resdict = { "s3uri": "s3://cloudcomputinga2harjot/newfile.txt"} 
            return resdict,200
        

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '80')
    app.run(debug=True, port=server_port, host='0.0.0.0')
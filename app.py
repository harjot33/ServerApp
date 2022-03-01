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
    aws_access_key_id="ASIA52YPANNBPZ4V4TAZ",
    aws_secret_access_key="g+aIsuiSSgtOziS4/npWCcnJmLRBM3e24vUD3d2E",
    aws_session_token="FwoGZXIvYXdzEMT//////////wEaDH1AzuPKb4R6hv2guyLAAS+2sy3NhTAs6+LykYOuTclyH3aV2upUhWe4bqEjQ3uEYEzLoMi4eUAqvRo2Shr+h+ai63z9A8g3kyb4Ss9mj8Gn4S+RZj1sliIOJ+nOt0U48N/8qNmz6vuOOdmnNPDa0EY6uflBd0SVU7OzWdQ/1ovnxQmtUuem0yh/ysZTkCzEmGpLTyBNUS3kUB+4K+/z7hLoCJPIQFtGK38qXtQhK7teRLYlVjlxbC7qesicq+swOVTdLyAOy649ov5hBoa/fyjxz/mQBjItVbjGjdT8xMOip1nXf2k+lfZ/HTmPu4zW/R3LBYm+Igjw8utc9VGbK/YcAmg5"
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
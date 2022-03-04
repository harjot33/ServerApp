from queue import Empty
from urllib import response, request
from flask import Flask, jsonify,render_template, request, redirect, url_for, session, logging,Response
import boto3
import os, requests
import datetime

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
s3 = boto3.resource(
    's3',
    region_name='us-east-1',
    aws_access_key_id="ASIA52YPANNBNACEDROM",
    aws_secret_access_key="nyUcYh3nsMZ4u4kxqqgOt12Mntkj57D/jzKqGfR6",
    aws_session_token="FwoGZXIvYXdzEAcaDNDPVhEOgkjFKg76sCLAAf4p55KivDzuFbAPKhJJFNxJGYoz+WnE/EmEOD2EFspMDfWPmJB1+6iZCqQ984o4vvECcuTDJdE54mb2kcPKyJ4+lKiIWJ8rxCztfhRY60nO7mujPL2ZYG13+pxhXfm9VlWcZgh9TkHpCCun0+vTwrdjT3Qe05Y2j1dXoI8iVzOV/dhc+p7ikBiLCL/xz7GZ41mwdu0gjIwADuk/XyIpn83y1Vbhxt3KshCDztBxouKCUp0VxegpBVrFk2Au90l0wyjMtIiRBjItWMygGb5xwmkkDf/9POfGJqxoGXgFj5bXrkPjFaH2lJciPrjECGRrR23bFljS"
)

initial = {
"banner": "B00872298",
"ip": "3.85.50.76"
}

res = requests.post('3.88.132.229/begin', json=initial)


@app.route('/storedata',methods=['POST'])
def sendword():
    if request.method == 'POST':
        content = request.get_json(force=True)
        data=content['data']
        res = s3.Object('cloudcomputinga2harjot', 'newfile.txt').put(Body=data,ACL='public-read')
        res1 = res['ResponseMetadata']
        if(res1['HTTPStatusCode']==200):
            resdict = { "s3uri": "https://cloudcomputinga2harjot.s3.amazonaws.com/newfile.txt"} 
            return resdict,200
        

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '80')
    app.run(debug=True, port=server_port, host='0.0.0.0')
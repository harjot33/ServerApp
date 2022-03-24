from queue import Empty
from urllib import response, request
from flask import Flask, jsonify,render_template, request, redirect, url_for, session, logging,Response
import boto3
import sqlalchemy
import base64
import ast
from sqlalchemy import exc
import os, requests
from botocore.exceptions import ClientError
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
host = ""
port = ""
username = ""
password = ""
database = ""

def get_secret():

    secret_name = "dbpass"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(    region_name='us-east-1',
    aws_access_key_id="ASIA52YPANNBLUZZD34W",
    aws_secret_access_key="WKYBpVFag+uiAhZw9cCKg8Fxm9yOSDFe2HwwG74G",
    aws_session_token="FwoGZXIvYXdzEOn//////////wEaDNDu5wpF/zRjPaAlkCLAAayvmlDt/yEEnxkPnZWQNOMdKshQpSLTmha1D/p5RHQznrLhdiuJYNZOCd25Mpq14eU9m7aF1YJBIMbbH/GNNZdQQXSV6aTj/iEb3Wx/bCcLEOwV5zklohxG4nP0oZl52D4PBmrw/529ZOMPOvs+bIkYSha5bBkPePPRu1c84F+2+zrk+61QLZBD7AYRIz1AisGQF1seLgBPTR0V8t0Oc6xm9h3n0hA4ZnxekdQTs8dwD1bOkzQnbKQidpUtbXfLISiblfKRBjItbLumVxEPEL7xwYBWwV6xmkH2zJn+lAaeDCD+WhemMiSiKCmAE8ZEb50YYSkN",
        service_name='secretsmanager',
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS key.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            
    secret_dict = ast.literal_eval(secret)
    return secret_dict


def init_db_connection():

    db_config = {
        
        'pool_size': 5,
        'max_overflow': 2,
        'pool_timeout': 30,
        'pool_recycle': 1800,
    }
    return init_unix_connection_engine(db_config)

def init_unix_connection_engine(db_config):
    secret = get_secret()
    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
        drivername="mysql+pymysql",
            host=secret.get("host"),
            port=secret.get("port"),
            username=secret.get("username"),
            password=secret.get("password"),
            database=secret.get("dbname"),
        ),
        **db_config
    )
    pool.dialect.description_encoding = None
    return pool

db = init_db_connection()

@app.route('/storestudents',methods=['POST'])
def sendword():
    if request.method == 'POST':
        content = request.get_json(force=True)
        data=content['students']
        print(data)
        students = {}
        if data is not None:
            for i in data:
                studict = i
                studentfname = studict["first_name"]
                studentlname = studict["last_name"]
                studentbanner = studict["banner"]
                try:
                    with db.connect() as conn:
                        conn.execute("insert into students (first_name, last_name, banner) values (%s, %s, %s);",(studentfname, studentlname,studentbanner))
                except exc.SQLAlchemyError as e:
                    error = str(e.orig)
                    print(error)
                    return error,400
        
        return Response(status=200)


@app.route('/liststudents',methods=['GET'])
def liststudents():
    if request.method == 'GET':
        try:
            with db.connect() as conn:
                    info = conn.execute("select * from students")
                    rows = info.fetchall()
                    return render_template('table.html', rows = rows)
        except exc.SQLAlchemyError as e:
            error = str(e.orig)
            return error,400


@app.route('/')
def begincall():
    get_secret()
    return "OK"

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '80')
    app.run(debug=True, port=server_port, host='0.0.0.0')
import sqlite3, dotenv, os, boto3


dotenv.load_dotenv()
config, session = {key: value for key, value in os.environ.items()}, boto3.session.Session()
print(config)
client = session.client(
    's3', region_name='nyc3',
    endpoint_url='https://nyc3.digitaloceanspaces.com',
    aws_access_key_id=config.get("DECAF"),
    aws_secret_access_key=config.get("SPACES_SECRET")
    )
client.download_file('degenerate-cafe', 'mlb.sqlite3', 'mlb.sqlite3')
DB=sqlite3.connect("mlb.sqlite3")

def upload_db():

    return client.upload_file('mlb.sqlite3', 'degenerate-cafe', 'mlb.sqlite3')
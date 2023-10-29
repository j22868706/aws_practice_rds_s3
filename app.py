from flask import *
import pymysql
import rds_db as db
import boto3
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__) 
app.secret_key = os.getenv("app.secret_key")
app.config['SESSION_TYPE'] = 'filesystem'
s3 = boto3.client("s3", aws_access_key_id=os.getenv("aws_access_key_id"), aws_secret_access_key=os.getenv("aws_secret_access_key"))
BUCKET_NAME = os.getenv("BUCKET_NAME")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/upload", methods=["POST"])
def upload():
    if 'user_file' not in request.files:
        flash('No user_file key in request.files')
        return redirect(url_for('index'))
    
    file = request.files['user_file']
    print(file)
    text = request.form['text']
    print(text)

    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        try:
            
            s3.upload_fileobj(file, BUCKET_NAME, file.filename)
            flash("Success upload")
            image_url = s3.generate_presigned_url("get_object", Params={"Bucket": BUCKET_NAME, "Key": file.filename},)
            db.insert_details(text, image_url)
            return redirect(url_for('index'))
        except Exception as e:
            flash("Unable to upload, try again")
    else:
        flash("File type not accepted, please try again")

    return redirect(url_for('index'))


@app.route("/get_details")
def details():
    details = db.get_details()
    details_as_json = [{'text': detail[0], 'image_url': detail[1]} for detail in details]
    return jsonify(details_as_json)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3500)
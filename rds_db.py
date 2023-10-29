import pymysql
from dotenv import load_dotenv
import os
load_dotenv()

def insert_details(text, image_url):
    conn = pymysql.connect(
    host= os.getenv("host"),
    port=3306,
    user= os.getenv("user"),
    password= os.getenv("password"),
    database= os.getenv("database")
)   
    cur = conn.cursor()
    cur.execute("INSERT INTO message (message, image_url) VALUES (%s, %s)", (text, image_url))
    conn.commit()
    cur.close()  

def get_details():
    conn = pymysql.connect(
    host= os.getenv("host"),
    port=3306,
    user= os.getenv("user"),
    password= os.getenv("password"),
    database= os.getenv("database")
)
    try:
        cur = conn.cursor()
        cur.execute("SELECT message, image_url FROM message ORDER BY id DESC")
        details = cur.fetchall()
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()
    
    return details

from flask import Flask,render_template,request,redirect
import mysql.connector as mysql
import string
import random

app = Flask(__name__)

db = mysql.connect(
    host="academia.c1mebdhdxytu.us-east-1.rds.amazonaws.com",
    user="p9",
    password="ALrUBIaLYcHR",
    database="p9"
)
cursor = db.cursor()
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/create", methods=["GET", "POST"])
def createShortener():
    
    length_of_string = 3
    
    short =(''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string)))
    if request.method == 'POST':
        url=request.form['dirUrl']
        
        sql= "INSERT INTO datos (short_url,large_url) VALUES (%s,%s)"
        val = (short,url)
        cursor.execute(sql,val)
        db.commit()

    return render_template("shorteners/create.html", url=url,short=short)

@app.get("/short/<shortened>")
def redirection(shortened):
    print(shortened)
    sql = "SELECT large_url FROM datos WHERE short_url = %(short_url)s"
    cursor.execute(sql,{'short_url':shortened})
    result = cursor.fetchone()
    print(result[0])
    return redirect(result[0])
app.run(debug=True)
from flask import Flask, request
from flask import render_template
import datetime
import smtplib
import json
import requests

#posts = requests.get("https://api.npoint.io/1d04317701f97c4c226d", verify=False).json()
app = Flask(__name__)
username = "test"
password = "test"
with open("blogdata.json", mode="r") as data_file:
    posts = json.load(data_file)

@app.route("/")
def home():
    current_year = datetime.datetime.now().year
    return render_template("index.html", year=current_year, all_posts=posts)

@app.route("/blogdetails/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("blogdetails.html", post=requested_post)

@app.route("/", methods=["GET", "POST"])
def receive_data():
    if request.method == "POST":
        data = request.form
        send_email(data["name"],data["email"],data["subject"],data["message"])
        return render_template("index.html", msg_sent=True)
    return render_template("index.html", msg_sent=False)

def send_email(name, email, subject, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nSubject: {subject}\nMessage:{message}"

    server = smtplib.SMTP("smtp.mail.yahoo.com",587)
    server.login(username,password)
    server.sendmail(username, username,email_message)
    server.quit()

if __name__ == "__main__":
    app.run(debug=True)
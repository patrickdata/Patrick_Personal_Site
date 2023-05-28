from flask import Flask, request
from flask import render_template
import datetime
import smtplib
import requests

posts = requests.get("https://api.npoint.io/1d04317701f97c4c226d", verify=False).json()
app = Flask(__name__)
OWN_EMAIL = "patricknguyen2507@gmail.com"
OWN_PASSWORD = "Kia@23921"

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
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)

if __name__ == "__main__":
    app.run(debug=True)
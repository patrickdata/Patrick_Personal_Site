from flask import Flask, request
from flask import render_template
import datetime
import smtplib

app = Flask(__name__)
OWN_EMAIL = "YOUR OWN EMAIL ADDRESS"
OWN_PASSWORD = "YOUR EMAIL ADDRESS PASSWORD"

@app.route("/")
def home():
    current_year = datetime.datetime.now().year
    return render_template("index.html", year=current_year)

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
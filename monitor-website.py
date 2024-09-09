import requests
import smtplib

response = requests.get("https://ndc.krones-deu.krones-group.com/")
if response.status_code == 200:
    print("Application is running successfully!")
else:
    print("Application Down. Fix it!")
    # send email to me
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login("user@email.com", )
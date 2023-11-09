import requests
import time
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

godaddy_api_key = 'your-api-key'
godaddy_api_secret = 'your-api-secret'
domain_to_check = 'domain-you-want-to-lookup'
recipient_email = 'your-email'
recepient_email2 = 'secondary-email' ## remove line if not needed

def is_domain_available(domain):
    url = f"https://api.godaddy.com/v1/domains/available?domain={domain}"
    headers = {"Authorization": f"sso-key {godaddy_api_key}:{godaddy_api_secret}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status() 
    return response.json()["available"]



def send_email_via_outlook(recipient, body):
    sender_email = os.environ.get('MY_EMAIL_ADDRESS') ##add sender email in .env file
    password = os.environ.get('MY_EMAIL_PASSWORD') ##add sender password in .env file

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = f'Domain Availability Notification'
    msg['From'] = sender_email
    msg['To'] = recipient

    smtp_server = 'smtp-mail.outlook.com'
    smtp_port = 587

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        print("Email sent successfully")

def main():
    try:
        while True:
            if is_domain_available(domain_to_check):
                send_email_via_outlook(recipient_email, f"The domain {domain_to_check} is available!")
                send_email_via_outlook(recepient_email2, f"The domain {domain_to_check} is available!") ## remove line if didnt add second recepient
                break
            else:
                print(f"The domain {domain_to_check} is not available. Checking again in 5 seconds.") ## keeps checking until stopped by user or found
                time.sleep(5) ##change time as needed, 1 = 1 second
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

if __name__ == "__main__":
    main()

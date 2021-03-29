
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from flask_mail import Message
import smtplib
from twilio.rest import Client
import random
from twilio.http.http_client import TwilioHttpClient
import os


#Your new Phone Number is +12074642648
def generateOTP(phno):
    try:
        proxy_client = TwilioHttpClient()
        #proxy_client.session.proxies = {'https': os.environ['https_proxy']}
        account_sid = os.environ.get('account_sid')
        auth_token = os.environ.get('auth_token')
        client = Client(account_sid, auth_token)
        n = random.randint(1000, 9999)
        client.messages.create(
            body='OTP is - ' + str(n),
            from_='+12074642648',
            to= '+91' + str(phno)
        )

        return n
    except(e):
        print('Error')
        print(e)


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email


def send_email(to, subject, template):
    email = os.environ.get('MY_EMAIL')
    password = os.environ.get('MY_PASS')
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(email, password)

        msg = f'Subject: {subject}\n\n{template}'
        smtp.sendmail(email, to, msg)

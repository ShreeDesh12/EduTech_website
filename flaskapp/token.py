
from itsdangerous import URLSafeTimedSerializer
from flaskapp import app
from flask_mail import Message
from flaskapp import app
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
        account_sid = 'ACdde6653e686d036a4b77ac5f402ad523'
        auth_token = '98a166c783bc1e1a94f86a3d26fd88dd'
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
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
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

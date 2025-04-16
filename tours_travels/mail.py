import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


def verification_mail(link, user):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()

    ei = "dedeexpeditions@gmail.com"
    password = "jzuy eqkw ovpu wcxv"

    # print(ei, password)

    

   
    s.login(ei, password)
    msg = MIMEMultipart()
    print(link, user.email, type(user.email))
    msg['From'] = "Dede Expeditions"
    msg['To'] = user.email
    msg['Subject'] = "Welcome to Dede Expeditions"
    message = f'Hi {user.username}, welcome to Dede Expeditions.<br>To activate your account, click the link below:<br>{link}<br><br>'

    # Add a new paragraph about the advantages of your travel agency in HTML
    directors_message = """
    <p> <strong> Directors message </strong></p>
    """

    advantages_message = """
    <p>We are delighted to have you as part of the Dede Expeditions community. Our goal is simple: We want every trip you take with us to be <strong>affordable</strong> and wonderfully <strong>memorable</strong>. Thats where we come in, we take care of all the little things to ensure your journey is smooth and effortless, creating moments you'll treasure forever.</p>    """

    msg.attach(MIMEText(message + directors_message + advantages_message, 'html'))
    s.send_message(msg)
    s.quit()

    


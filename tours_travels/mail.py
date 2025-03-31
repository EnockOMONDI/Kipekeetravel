import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


def verification_mail(link, user):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()

    ei = "novustellke@gmail.com"
    password = "jdxozdtmtoeljezk"

    # print(ei, password)

    

   
    s.login(ei, password)
    msg = MIMEMultipart()
    print(link, user.email, type(user.email))
    msg['From'] = "Novustell Travel"
    msg['To'] = user.email
    msg['Subject'] = "Welcome to Novustell Travel"
    message = f'Hi {user.username}, welcome to Novustell Travel.<br>To activate your account, click the link below:<br>{link}<br><br>'

    # Add a new paragraph about the advantages of your travel agency in HTML
    directors_message = """
    <p> <strong> Directors message </strong></p>
    """

    advantages_message = """
    <p>We are delighted to have you as part of the Novustell Travel community. Our goal is simple: We want every trip you take with us to be <strong>affordable</strong> and wonderfully <strong>memorable</strong>. Thats where we come in, we take care of all the little things to ensure your journey is smooth and effortless, creating moments you'll treasure forever.</p>    """

    msg.attach(MIMEText(message + directors_message + advantages_message, 'html'))
    s.send_message(msg)
    s.quit()

    


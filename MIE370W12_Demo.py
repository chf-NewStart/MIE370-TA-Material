import smtplib
from email.message import EmailMessage
import os
import ssl
import numpy as np


# Function to calculate performance
def check_performance(y_true, y_pred):
    mse = np.mean((y_true - y_pred) ** 2)
    print(f"Mean Squared Error: {mse}")
    return mse

# Original and new predictions
y_pred_original = np.array([5.0, 6.2, 4.9, 8.0])
y_true_original = np.array([5.1, 6.1, 4.8, 8.1])
y_pred_new = np.array([4.1, 6.2, 3.8, 8.1])


email_sender = 'houfuchen0702@gmail.com'
email_password = os.environ.get("EMAIL_PASSWORD")
if email_password is None:
    raise ValueError("Email password not set. Please check the environment variable.")
print("email_password: ", email_password) 
email_receiver = 'houfu.chen@mail.utoronto.ca'


# Function to send the email
def send_email(mse_new):
    # Create the email content
    em=EmailMessage()
    em['From']=email_sender
    em['To']=email_receiver
    em['Subject']='Alert'
    em.set_content(f"Alert: Model performance has degraded. MSE is now {mse_new}.")

    context = ssl.create_default_context() #for extra security!!!

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


# Check performance (as you've done already)
mse_original = check_performance(y_true_original, y_pred_original)
mse_new = check_performance(y_true_new, y_pred_new)

# Set a threshold for acceptable performance
threshold = mse_original * 1.2

# Alert if the new performance is below the threshold
if mse_new > threshold:
    print("Performance has degraded! Sending alert...")
    send_email(mse_new)

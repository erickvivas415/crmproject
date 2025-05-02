import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
load_dotenv()

# Make sure to replace 'your_actual_api_key' with the actual API key from your SendGrid account


message = Mail(
    from_email='membership@latinosinfinance.org',  # Replace with a verified email
    to_emails='erickvivas415@gmail.com',  # Replace with the recipient's email
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>'
)

try:
    # Get the API key from the environment variable
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    
    # Send the email
    response = sg.send(message)
    
    # Print the response details
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.body}")
    print(f"Response Headers: {response.headers}")
except Exception as e:
    print(f"Error: {str(e)}")
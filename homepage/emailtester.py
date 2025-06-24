
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import os
from django.contrib import messages
from django.shortcuts import render
# Load environment variables from .env file
load_dotenv()
# Function to send a personalized welcome email


# Personalized welcome HTML
html_content = f"""
                <div style="font-family: Arial, sans-serif; font-size:14px; line-height:1.6; color:#333;">
                <!-- Logo at the top -->
                <div style="text-align: left; margin-bottom: 20px;">
                <img src="https://images.squarespace-cdn.com/content/v1/52742948e4b0c2eac22b888e/1383594624830-QFRNTFEY4CJ8HY4I0QZQ/LIFi.jpg?format=1500w" alt="Latinos in Finance" style="width: 150px;">
                </div>

                <p><strong>Welcome to Latinos in Finance, Erick Vivas!</strong></p>
                <p>We’re excited to have you as part of our growing community of Latino professionals in finance.</p>
                <p>To access the full benefits of your membership — including networking opportunities, event invitations, and member-only resources — please take a moment to 
                                    <a href="https://crmproject-9f4q.onrender.com" target="_blank">update your profile</a>.
                                </p>
                                <p>This helps us personalize your experience and connect you with the right people and opportunities.</p>
                                <p>Bienvenidos — we look forward to growing with you!</p>
                                <br>
                                <p>Follow us:</p>
                                <!-- Social media links -->
                                <div style="margin-top: 30px; text-align: left;">
                                    <a href="https://instagram.com/latinosinfinance" target="_blank" style="margin-right: 10px;">
                                        <img src="https://cdn-icons-png.flaticon.com/512/1384/1384063.png" alt="Instagram" style="width: 24px; height: 24px;">
                                    </a>
                                    <a href="https://www.linkedin.com/company/latinos-in-finance" target="_blank" style="margin-right: 10px;">
                                        <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn" style="width: 24px; height: 24px;">
                                    </a>
                                    <a href="https://www.youtube.com/@LatinosInFinance" target="_blank">
                                        <img src="https://cdn-icons-png.flaticon.com/512/1384/1384060.png" alt="YouTube" style="width: 24px; height: 24px;">
                                    </a>
                                </div>
                            </div>
                        """

            # Send a welcome email
message = Mail(
                from_email='Latinos in Finance <membership@latinosinfinance.org>',  # Replace with a verified email
                to_emails='erickvivas415@gmail.com',  # Replace with the recipient's email
                subject='Welcome to Latinos in Finance',
                html_content=html_content,         
                )

try:
                # Get the API key from the environment variable
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY').strip())
                
                # Send the email
    response = sg.send(message)


        
except Exception as e:
                print(f"Error: {str(e)}")
                
            

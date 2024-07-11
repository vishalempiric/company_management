from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags


def send_custom_email(reset_link, recipient_list):
    # Send the email using Django's send_mail function

    html_message = f"""
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 20px;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: #ffffff;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }}
                    h1 {{
                        color: #333333;
                    }}
                    p {{
                        color: #666666;
                    }}
                    .button {{
                        display: inline-block;
                        background-color: #007bff;
                        color: #ffffff;
                        text-decoration: none;
                        padding: 10px 20px;
                        border-radius: 5px;
                        margin-top: 15px;
                    }}
                    a {{
                        color: #007bff;
                        text-decoration: none;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Password Reset Request</h1>
                    <p>Click the link below to reset your password:</p>
                    <a class="button" href="{reset_link}">Reset Password</a>
                </div>
            </body>
            </html>
        """
    
    # send_mail(
    #     'Password Reset Request',
    #     strip_tags(html_message), 
    #     settings.EMAIL_HOST_USER,
    #     recipient_list,
    #     html_message=html_message, 
    #     fail_silently=False,
    # )

    send_mail(
        'Password Reset Request',      # Subject of the email
        strip_tags(html_message),      # Plain text content of the email (generated from the HTML content)
        settings.EMAIL_HOST_USER,      # Sender's email address (from settings)
        recipient_list,                # List of recipient email addresses
        html_message=html_message,     # HTML content of the email
        fail_silently=False,           # Whether to raise exceptions if sending fails
    )

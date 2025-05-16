from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Gmail configuration
GMAIL_USER = os.environ.get('EMAIL_USER') 
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD') 
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
GMAIL_PORT = 587
GMAIL_SERVER = "smtp.gmail.com"

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET')  # Change this to a random string in production


def send_email(recipient, subject, body, sender=GMAIL_USER):
    """Send an email using Gmail SMTP"""
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    
    # Add message body
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # Connect to Gmail SMTP server
        server = smtplib.SMTP(GMAIL_SERVER, GMAIL_PORT)
        server.starttls()  # Secure the connection
        server.login(GMAIL_USER, EMAIL_PASSWORD)
        
        # Send email
        text = msg.as_string()
        server.sendmail(sender, recipient, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# Routes
@app.route('/')
def index():
    """Render the main portfolio page"""
    return render_template('index.html', title='Developer Portfolio')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    """Handle contact form submission and send email notification"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Prepare email content
        email_subject = f"Contact Form Submission: {subject}"
        email_body = f"""
        New contact form submission:
        
        Name: {name}
        Email: {email}
        Subject: {subject}
        
        Message:
        {message}
        """

         # Send email notification to admin
        admin_email = ADMIN_EMAIL # Replace with where you want to receive notifications
        email_sent = send_email(admin_email, email_subject, email_body)
        
         # Return appropriate response
        if email_sent:
            return jsonify({
                'status': 'success',
                'message': f'Thank you {name}, your message has been received!'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'There was an issue processing your request. Please try again later.'
            })

# Custom error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)  # Set debug=False in production
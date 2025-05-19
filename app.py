from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import resend

load_dotenv()

app = Flask(__name__)

# Gmail configuration
RESEND_API_KEY = os.environ.get('RESEND_API_KEY')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL') 

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET')  # Change this to a random string in production


resend.api_key = RESEND_API_KEY

def send_email(recipient, subject, body, sender=SENDER_EMAIL):
    """Send an email using Resend API"""
    try:
        response = resend.Emails.send({
            "from": sender,
            "to": [recipient],
            "subject": subject,
            "text": body
        })
        return True if response.get("id") else False
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
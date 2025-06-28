#!/usr/bin/env python3
"""
Test Gmail connection with your app password
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_gmail_connection():
    print("🔐 Testing Gmail Connection")
    print("=" * 30)
    
    email = "oxternal.0x@gmail.com"
    
    # You need to replace this with your actual app password
    app_password = "your-16-character-app-password-here"
    
    if app_password == "your-16-character-app-password-here":
        print("❌ Please update the app_password variable with your actual Gmail app password")
        print("   Edit this file and replace 'your-16-character-app-password-here'")
        print("   with your 16-character app password from Google")
        return False
    
    try:
        print(f"📧 Testing connection to {email}...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, app_password)
        server.quit()
        print("✅ Gmail connection successful!")
        
        # Send test email
        print("📤 Sending test email...")
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = email
        msg['Subject'] = "🚨 Trading Alert System Test"
        
        body = """
        <html>
        <body>
        <h2>🚨 Trading Alert Test Successful!</h2>
        <p>Your Gmail alert system is working perfectly.</p>
        <p>You will now receive trading alerts at this email address.</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, app_password)
        server.send_message(msg)
        server.quit()
        
        print("✅ Test email sent successfully!")
        print(f"📧 Check your inbox at {email}")
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n🔧 Common issues:")
        print("   - Make sure you're using the App Password, not your regular password")
        print("   - Ensure 2-factor authentication is enabled")
        print("   - Check that the app password is exactly 16 characters")
        return False

if __name__ == "__main__":
    test_gmail_connection()

#!/usr/bin/env python3
"""
Gmail Alert Setup Guide for oxternal.0x@gmail.com

This script shows you how to set up Gmail alerts step by step.
"""

def show_gmail_setup_instructions():
    """Show detailed Gmail setup instructions"""
    print("📧 Gmail Alert Setup for Trading Agents")
    print("=" * 50)
    print(f"📧 Your Email: oxternal.0x@gmail.com")
    print()
    
    print("📋 Complete Setup Steps:")
    print("=" * 30)
    
    print("\n🔐 Step 1: Enable 2-Factor Authentication")
    print("   1. Go to: https://myaccount.google.com/security")
    print("   2. Click 'Security' in the left menu")
    print("   3. Find '2-Step Verification' and turn it ON")
    print("   4. Follow the prompts to set up with your phone")
    
    print("\n🔑 Step 2: Generate App Password")
    print("   1. Still in Google Account Security page")
    print("   2. Look for 'App passwords' (may need to scroll)")
    print("   3. Click 'App passwords'")
    print("   4. Select 'Mail' from the dropdown")
    print("   5. Click 'Generate'")
    print("   6. Copy the 16-character password (example: abcd efgh ijkl mnop)")
    
    print("\n📝 Step 3: Update Configuration")
    print("   Your app password will look like: 'abcd efgh ijkl mnop' (16 chars)")
    print("   Replace 'your-app-password-here' in the config with this password")
    
    print("\n🧪 Step 4: Test Your Setup")
    print("   After getting your app password, test with:")
    print("   python3 test_gmail_connection.py")

def create_test_script():
    """Create a simple test script for Gmail connection"""
    test_script_content = '''#!/usr/bin/env python3
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
        print("\\n🔧 Common issues:")
        print("   - Make sure you're using the App Password, not your regular password")
        print("   - Ensure 2-factor authentication is enabled")
        print("   - Check that the app password is exactly 16 characters")
        return False

if __name__ == "__main__":
    test_gmail_connection()
'''
    
    try:
        with open('test_gmail_connection.py', 'w') as f:
            f.write(test_script_content)
        print("✅ Created test_gmail_connection.py")
        return True
    except Exception as e:
        print(f"❌ Failed to create test script: {e}")
        return False

def create_working_config_template():
    """Create a template for working configuration"""
    config_template = '''#!/usr/bin/env python3
"""
Working Gmail Alert Configuration Template
Update the app_password with your actual Gmail app password
"""

# Replace 'your-app-password-here' with your 16-character Gmail app password
GMAIL_APP_PASSWORD = "your-app-password-here"

# Your working Gmail alert configuration
GMAIL_ALERT_CONFIG = {
    "alerts_enabled": True,
    "alert_on_decisions": ["BUY", "SELL"],
    
    "notification_handlers": {
        "email": {
            "enabled": True,
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender_email": "oxternal.0x@gmail.com",
            "sender_password": GMAIL_APP_PASSWORD,
            "recipient_emails": ["oxternal.0x@gmail.com"],
            "use_tls": True,
        }
    }
}

# Multi-channel config (email + webhook)
FULL_ALERT_CONFIG = {
    "alerts_enabled": True,
    "alert_on_decisions": ["BUY", "SELL"],
    
    "notification_handlers": {
        "email": {
            "enabled": True,
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender_email": "oxternal.0x@gmail.com",
            "sender_password": GMAIL_APP_PASSWORD,
            "recipient_emails": ["oxternal.0x@gmail.com"],
            "use_tls": True,
        },
        "webhook": {
            "enabled": True,
            "url": "https://webhook.site/your-unique-url",  # Replace with your webhook URL
            "method": "POST",
            "headers": {
                "Authorization": "Bearer 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",
                "Content-Type": "application/json"
            }
        }
    }
}
'''
    
    try:
        with open('gmail_config_template.py', 'w') as f:
            f.write(config_template)
        print("✅ Created gmail_config_template.py")
        return True
    except Exception as e:
        print(f"❌ Failed to create config template: {e}")
        return False

def main():
    show_gmail_setup_instructions()
    
    print("\n📁 Creating Helper Files:")
    print("=" * 30)
    
    # Create test script
    create_test_script()
    
    # Create config template
    create_working_config_template()
    
    print("\n🎯 Quick Summary:")
    print("=" * 20)
    print("1. ✅ Go to Google Account Security")
    print("2. ✅ Enable 2-factor authentication")
    print("3. ✅ Generate App Password for Mail")
    print("4. ✅ Edit test_gmail_connection.py with your app password")
    print("5. ✅ Run: python3 test_gmail_connection.py")
    print("6. ✅ Edit gmail_config_template.py with your app password")
    print("7. ✅ Use the config in your trading system")
    
    print("\n🔗 Important Links:")
    print("   • Google Account Security: https://myaccount.google.com/security")
    print("   • App Passwords: https://myaccount.google.com/apppasswords")
    
    print("\n💡 Pro Tip:")
    print("   Save your app password securely - you'll need it for the trading system!")

if __name__ == "__main__":
    main()
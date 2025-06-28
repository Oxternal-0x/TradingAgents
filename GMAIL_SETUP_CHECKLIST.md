# 📧 Gmail Alert Setup Checklist

**Email:** oxternal.0x@gmail.com

## 📋 Setup Progress

### Phase 1: Google Account Setup
- [ ] **Go to Google Account Security**: https://myaccount.google.com/security
- [ ] **Enable 2-Factor Authentication** (if not already enabled)
- [ ] **Find "App passwords"** section
- [ ] **Generate App Password for Mail**
- [ ] **Copy the 16-character password** (save it securely!)

### Phase 2: Configure & Test
- [ ] **Edit `test_gmail_connection.py`**
  - Replace `"your-16-character-app-password-here"` with your actual app password
- [ ] **Run test**: `python3 test_gmail_connection.py`
- [ ] **Check your email** for the test message
- [ ] **Verify connection works** (should see "✅ Gmail connection successful!")

### Phase 3: Set Up Trading Alerts
- [ ] **Edit `gmail_config_template.py`**
  - Replace `"your-app-password-here"` with your actual app password
- [ ] **Test with trading system**: `python3 test_personal_alerts.py`
- [ ] **Run real trading analysis** with alerts enabled

## 🔑 Your App Password Format
```
Example: abcd efgh ijkl mnop
Length: Exactly 16 characters (with spaces removed: abcdefghijklmnop)
```

## ✅ Success Indicators
- Gmail connection test passes
- Test email received in your inbox
- Trading alert system sends notifications
- No authentication errors

## 🔧 Troubleshooting
- **"Authentication failed"**: Use App Password, not regular password
- **"App passwords not available"**: Enable 2-factor authentication first
- **"SMTP error"**: Check Gmail settings, verify app password

## 📞 Quick Links
- [Google Account Security](https://myaccount.google.com/security)
- [App Passwords Setup](https://myaccount.google.com/apppasswords)

---
*Once completed, you'll receive instant email alerts for all BUY/SELL trading signals!* 🚀
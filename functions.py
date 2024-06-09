import csv
import random
import string
import datetime
import unicodedata
from setup import smtp_server, smtp_port, smtp_password, sender_mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Get Formatted Time
def formatted_time():
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time

# Function for checking registrations
def get_registrations_count_csv():
    try:
        with open('registrations.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  # Přeskočení hlavičky
            return sum(1 for row in reader)
    except FileNotFoundError:
        return 0

# Generates unique code for unregistering from the event
def generate_unique_code(first, second):
    # Replace special characters in first and second strings
    first_clean = ''.join(replace_special_char(char) for char in first)
    second_clean = ''.join(replace_special_char(char) for char in second)
    
    # Get 3 first letters of the cleaned first and second part for the code
    code_prefix = (first_clean[:3] if len(first_clean) >= 3 else first_clean) + (second_clean[:3] if len(second_clean) >= 3 else second_clean)
    # Code suffix
    code_suffix = ''.join(random.choices(string.digits, k=3))

    unique_code = code_prefix + code_suffix
    return unique_code

def replace_special_char(char):
    # Replace special characters with their regular counterparts
    return unicodedata.normalize('NFD', char).encode('ascii', 'ignore').decode('utf-8')

# Extract ID
def extract_id(file_txt):
    with open(file_txt, 'r') as file:
        # Read the first line
        id = file.readline().strip()
        return id

# Find Data/Row in Google Sheet
def find_row(all_values, unsubscribe_code):
    found_data = None
    for index, row in enumerate(all_values):
        if unsubscribe_code in row:
            found_data = index + 1  # Rows start from 1, not 0
            break
    return found_data

def add_value_to_last_row(value, all_values, sheet):
    last_filled_row = len(all_values)
    next_column = len(all_values[0]) 
    sheet.update_cell(last_filled_row, next_column, value)

# Confiramtion email sending
def send_confirmation_email(receiver_email, subject, code): 
    smtp_server_fc = smtp_server  
    smtp_port_fc = smtp_port
    smtp_password_fc = smtp_password
    sender_email_fc = sender_mail

    # Set up the sender, receiver, subject, and body
    with open("templates/mail.html", 'r') as file:
        html_content = file.read()

    email = sender_email_fc  # Replace with actual contact email
    html_content = html_content.format(email=email, code=code)

    # Create message container
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email_fc
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach HTML content
    msg.attach(MIMEText(html_content, 'html'))

    # Initialize the server variable
    server = None

    try:
        # Start the SMTP session
        server = smtplib.SMTP(smtp_server_fc, smtp_port_fc)
        server.starttls()  # Secure the connection
        server.login(sender_mail, smtp_password_fc)
        server.sendmail(sender_email_fc, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP Authentication Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if server:
            server.quit()
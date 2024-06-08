import csv
import random
import string

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
    # Get 3 first letters of the first and secornd part for the code
    code_prefix = (first[:3] if len(first) >= 3 else first) + (second[:3] if len(second) >= 3 else second)
    # Code suffix
    code_suffix = ''.join(random.choices(string.digits, k=3))

    unique_code = code_prefix + code_suffix
    return unique_code

# Extract id
def extract_id(file_txt):
    with open(file_txt, 'r') as file:
        # Read the first line
        id = file.readline().strip()
        return id
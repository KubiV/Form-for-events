import csv
import random
import string
import unicodedata

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

# Extract id
def extract_id(file_txt):
    with open(file_txt, 'r') as file:
        # Read the first line
        id = file.readline().strip()
        return id
    
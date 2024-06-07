import os
from flask import Flask, render_template, redirect, url_for
#from flask_bootstrap import Bootstrap
import yaml
from forms import create_form  # Importujte create_form z forms.py
import csv
import random
import string

app = Flask(__name__)
app.secret_key = 'your_secret_key'
#Bootstrap(app)

# Load the YAML file
with open('survey.yaml', 'r', encoding='utf-8') as f:
    survey_data = yaml.safe_load(f)

# Creating DynamicForm from survey_data obtained from yaml
DynamicForm = create_form(survey_data)

# Function for checking registrations
def get_registrations_count():
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

@app.route('/')
def home():
    return render_template('index.html', title="Hlavní stránka")

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Checking registrations
    registrations = 29 #get_registrations_count()
    if registrations >= survey_data['survey']['limit']:
        return render_template("limit.html", tittle="Dotazník uzavřen")

    form = DynamicForm()

    # Submitting the form
    if form.validate_on_submit():
        # Getting the data
        form_data = {field.name: field.data for field in form}

        # Generating the code
        first_item = list(form_data.values())[0]
        second_item = list(form_data.values())[1]
        unique_code = generate_unique_code(first_item, second_item)

        # Saving to CSV
        with open('registrations.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Checking the CSV header
            if file.tell() == 0:
                header = ["Unique Code"] + [field['name'] for field in survey_data['survey']['fields']]
                writer.writerow(header)
            
            row_data = [unique_code] + [form_data[field['name']] for field in survey_data['survey']['fields']]
            writer.writerow(row_data)

        return redirect(url_for('home'))
    
    return render_template('register.html', title=survey_data['survey']['title'], form=form)

@app.route('/unsubscribe')
def unsubscribe():
    return render_template('unsubscribe.html', title="Odhlásit se")

if __name__ == '__main__':
    # Retrieve the port from the environment variable, defaulting to 4000 if not set
    port = int(os.environ.get("PORT", 4000))
    # Run the Flask app, binding to '0.0.0.0' for external access
    app.run(debug=True, host='0.0.0.0', port=port)
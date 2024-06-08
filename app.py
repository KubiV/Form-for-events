import os
from flask import Flask, render_template, redirect, url_for
#from flask_bootstrap import Bootstrap
import yaml
from forms import create_form
import functions as fc
import csv
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)
app.secret_key = 'your_secret_key'
#Bootstrap(app)

# Load the YAML file
with open('survey.yaml', 'r', encoding='utf-8') as f:
    survey_data = yaml.safe_load(f)

# Creating DynamicForm from survey_data obtained from yaml
DynamicForm = create_form(survey_data)

# Load google sheet
credentials_file = 'credentials.json'
sheet_id = str(fc.extract_id("info.txt"))

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(credentials_file, scopes=SCOPES)
gc = gspread.authorize(credentials)

@app.route('/')
def home():
    return render_template('index.html', title="Hlavní stránka")

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Checking registrations
    registrations = 29 #fc.get_registrations_count_csv()
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
        unique_code = fc.generate_unique_code(first_item, second_item)

        spreadsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/"+ sheet_id +"/edit")
        worksheet = spreadsheet.sheet1
        all_values = worksheet.get_all_values()

        header = ["Unique Code"] + [field['name'] for field in survey_data['survey']['fields']]
        if len(all_values) == 0:
            worksheet.append_row(header)
        elif all_values[0] != header:
            worksheet.insert_row(header, index=1)

        # Prepare the row data and append it
        row_data = [unique_code] + [form_data[field['name']] for field in survey_data['survey']['fields']]
        worksheet.append_row(row_data)

        """
        # Saving to CSV
        with open('registrations.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Checking the CSV header
            if file.tell() == 0:
                header = ["Unique Code"] + [field['name'] for field in survey_data['survey']['fields']]
                writer.writerow(header)
            
            row_data = [unique_code] + [form_data[field['name']] for field in survey_data['survey']['fields']]
            writer.writerow(row_data)
        """
        return render_template("sent.html", tittle="Úspěšně odesláno") # redirect(url_for('home'))
    
    return render_template('register.html', title=survey_data['survey']['title'], form=form)

@app.route('/unsubscribe')
def unsubscribe():
    return render_template('unsubscribe.html', title="Odhlásit se")

if __name__ == '__main__':
    # Retrieve the port from the environment variable, defaulting to 4000 if not set
    port = int(os.environ.get("PORT", 4000))
    # Run the Flask app, binding to '0.0.0.0' for external access
    app.run(debug=True, host='0.0.0.0', port=port)
# Form for events
## Setup
Into the root directory add theese files containing:

setup.py - information for Google Sheet to be edited and information for email sending
```
id = "your_google_sheet_id" # dont forget to add API email as an editor to the sheet something@form-event.iam.gserviceaccount.com
registration_list = "List 1"
unsubscribed_list = "List 2"

smtp_server = "smtp.serevr.com"
smtp_port = 587
smtp_password = "password"
sender_mail = "sender-email@mail.com"
```

credentials.json
from the Google Sheet API -  https://console.cloud.google.com/apis/api/sheets.googleapis.com/metrics?hl=cs&project=form-event

## Add from
edit the survey.yaml file

Format:
```
survey:
  title: "Dotaznik"
  limit: 30
  email: true
  fields:
    - name: "name"
      label: "Jméno"
      type: "text"
      required: true
    - name: "surname"
      label: "Příjmení"
      type: "text"
      required: true
    - name: "email"
      label: "Email"
      type: "email"
      required: true
    - name: "attending"
      label: "Půjdete na akci?"
      type: "select-one"
      options: ["Ano", "Ne"]
      required: true
    - name: "question"
      label: "Jaké máte očekávání od akce?"
      type: "text"
      required: false
```

You have for now 3 types of answering options ("type" in yaml): text, email, select-one

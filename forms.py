from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email
from markupsafe import Markup

def create_form(survey_data):
    class DynamicForm(FlaskForm):
        pass

    for field in survey_data['survey']['fields']:
        field_name = field['name']
        field_label = field['label']
        field_required = field['required']
        field_type = field['type']

        if field_required:
            field_label += Markup('<span style="color: red;">*</span>')

        if field_type == 'text':
            setattr(DynamicForm, field_name, StringField(field_label, 
                validators=[DataRequired()] if field_required else []))
        elif field_type == 'email':
            setattr(DynamicForm, field_name, StringField(field_label, 
                validators=[DataRequired(), Email()] if field_required else [Email()]))
        elif field_type == 'select-one':
            choices = [(option, option) for option in field['options']]
            setattr(DynamicForm, field_name, RadioField(field_label, 
                choices=choices, 
                validators=[DataRequired()] if field_required else [], 
                render_kw={'class': 'radio'}))
        elif field_type == 'select-multiple':
            choices = [(option, option) for option in field['options']]
            setattr(DynamicForm, field_name, SelectField(field_label, 
                choices=choices, 
                validators=[DataRequired()] if field_required else [], 
                render_kw={'class': 'select'}))

    setattr(DynamicForm, 'submit', SubmitField('Odeslat'))
    return DynamicForm

# Function to handle the form submission
def handle_form_submission(form):
    form_data = {field.name: field.data for field in form}
    for field_name, field in form._fields.items():
        if field_name == 'submit':
            continue
        
        if not form[field_name].data and not isinstance(form[field_name].data, bool):  # Check if field is empty
            form_data[field_name] = 'NA'  # Set to 'NA' if empty
        else:
            form_data[field_name] = form[field_name].data
    return form_data

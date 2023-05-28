from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import ValidationError
from wtforms import validators, StringField, SelectField,URLField,IntegerField, PasswordField
from models.key import verify_key


ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'webp']


class LinkForm(FlaskForm):
    link = URLField("Link", validators=[validators.Length(max=6000),validators.URL(False,"bruh"),validators.DataRequired()])
    name = StringField("Link Name", validators=[validators.Length(max=6000)])
    media = FileField("Pic", validators=[FileAllowed(ALLOWED_EXTENSIONS,"Allowed File Types:"+str(ALLOWED_EXTENSIONS))])
    header = SelectField("Header Choices",validators=[validators.DataRequired()])

class HeaderForm(FlaskForm): 
    name = StringField("Header Name", validators=[validators.Length(max=6000),validators.DataRequired()])

class RenameHeaderForm(FlaskForm):
    new_name = StringField("New Header Name", validators=[validators.Length(max=6000),validators.DataRequired()])

class MoveHeaderForm(FlaskForm):
    category = SelectField("Category Choice",validators=[validators.DataRequired()])

class MoveLinkForm(FlaskForm):
    header = SelectField("Header Choice",validators=[validators.DataRequired()])

class CategoryForm(FlaskForm):
    name = StringField("Category Name", validators=[validators.Length(max=6000),validators.DataRequired()])
    media = FileField("Category Pic", validators=[FileAllowed(ALLOWED_EXTENSIONS,"Allowed File Types:"+str(ALLOWED_EXTENSIONS))])

class SearchForm(FlaskForm):
    #category = SelectField("Category Choices",validators=[validators.DataRequired()])
    #header = SelectField("Header Choices",validators=[validators.DataRequired()])
    link_text = StringField("Link", validators=[validators.Length(max=6000)])
    name = StringField("Link Name", validators=[validators.Length(max=6000)])
    page = IntegerField("Page")

class DeleteCategoryForm(FlaskForm):
    category = SelectField("Category Choice",validators=[validators.DataRequired()])

def validate_key(form,field):   
    if verify_key(field.data) == False:
        raise ValidationError("Key not Valid")


class EnterKeyForm(FlaskForm):
    key = PasswordField("Key",validators=[validate_key,validators.length(max=6000),validators.DataRequired()])


class MakeKeyForm(FlaskForm):
    key = PasswordField("Key",validators=[validators.length(max=6000),validators.DataRequired()])

class ChangeKeyForm(FlaskForm):
    old_key = PasswordField("Old Key",validators=[validators.length(max=6000),validators.DataRequired(),validate_key])
    key = PasswordField("New Key",validators=[validators.length(max=6000),validators.DataRequired()])


#for accessing multiple forms
class Forms():
    def __init__(self,form_dict):
        self.forms = dict(form_dict)
    def add_form(self,name,form):
        self.forms[name] = form
    def add_forms(self,form_dict):
        for key,val in form_dict.items():
            self.forms[key] = val
    def del_form(self,form_name):
        return self.forms.pop(form_name)
    def get_form(self,form_name):
        return self.forms[form_name]


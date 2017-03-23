# app/user/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

class UserArticleForm(FlaskForm):
    """
    Form for user to add or edit an article
    """
    pmid = StringField('ID', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    abstract = TextField('Description or Abstract', validators=[DataRequired()], widget=TextArea())
    submit = SubmitField('Submit')
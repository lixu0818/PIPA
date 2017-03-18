# app/user/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_login import current_user

class UserArticleForm(FlaskForm):
    """
    Form for user to add or edit an article
    """
    pmid = StringField('PMID', validators=[DataRequired()])
    title = StringField('Title')
    abstract = StringField('Description or Abstract', validators=[DataRequired()])
    submit = SubmitField('Submit')
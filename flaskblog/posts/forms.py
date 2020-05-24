from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError
from flaskblog.models import Category



class PostForm(Form):
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=50)])
    link = StringField('Link to Listing (Allowed sites - Ebaymotors, Craigslist)', validators=[DataRequired(), Length(min=10, max=150)])
    content = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Post')
    
    def validate_link(self, link):
        allowed = ['craigslist', 'ebaymotors']
        prefixes = ["http://", "https:/"]
        if link.data[:7] not in prefixes:
            raise ValidationError("That is an invalid prefix")
        for s in allowed:
            if s in link.data:
                return True
        raise ValidationError('That is an invalid link. Please choose a different one.')

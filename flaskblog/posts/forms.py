from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError



class PostForm(Form):
    #title = StringField('Title', validators=[DataRequired()])
    link = StringField('Link to Listing (Allowed sites - ebaymotors, craigslist)', validators=[DataRequired(), Length(min=10, max=30)])
    content = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Post')
    
    def validate_link(self, link):
        allowed = ['craigslist', 'ebaymotors']
        prefixes = ["http://", "https://"]
        if link.data[:7] not in prefixes:
            raise ValidationError("That is an invalid prefix")
        for s in allowed:
            if s in link.data:
                return True
        raise ValidationError('That is an invalid link. Please choose a different one.')

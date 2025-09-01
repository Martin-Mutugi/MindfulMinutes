from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired

class JournalForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    mood = SelectField('Mood', choices=[
        ('happy', '😊 Happy'),
        ('sad', '😢 Sad'),
        ('anxious', '😟 Anxious'),
        ('calm', '😌 Calm')
    ])
    submit = SubmitField('Save Entry')

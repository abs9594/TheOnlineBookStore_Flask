from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired,ValidationError
from flask_wtf.file import FileField
from app.catalogue.models import Publication,Book

def publication_does_not_exist(form,field):
    pub = Publication.query.filter_by(id=field.data).first()
    if not pub:
        raise ValidationError("Publication ID Does Not Exist")

def book_already_exists(form,field):
    book = Book.query.filter_by(title=field.data).first()
    if book:
        raise ValidationError("Book Name Already Exists")

def book_image_already_exists(form,field):
    book = Book.query.filter_by(image=field.data.filename).first()
    if book:
        raise ValidationError("Book Image Already Exists")

def publication_already_exists(form,field):
    pub = Publication.query.filter_by(name=field.data).first()
    if pub:
        raise ValidationError("Publication Already Exists")

class EditBookForm(FlaskForm):

    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    avg_rating = FloatField('Rating', validators=[DataRequired()])
    format = StringField('Format', validators=[DataRequired()])
    num_pages = IntegerField('Pages', validators=[DataRequired()])
    pub_id = IntegerField('Publication ID', validators=[DataRequired(),publication_does_not_exist])
    submit = SubmitField('Update')


class CreateBookForm(FlaskForm):

    title = StringField('Title', validators=[DataRequired(),book_already_exists])
    author = StringField('Author', validators=[DataRequired()])
    avg_rating = FloatField('Rating', validators=[DataRequired()])
    format = StringField('Format', validators=[DataRequired()])
    img_url = FileField('Image', validators=[DataRequired(),book_image_already_exists])
    num_pages = IntegerField('Pages', validators=[DataRequired()])
    pub_id = IntegerField('Publication ID', validators=[DataRequired(),publication_does_not_exist])
    submit = SubmitField('Create')

class CreatePublicationForm(FlaskForm):

    name = StringField('Name',validators=[DataRequired(),publication_already_exists])
    submit = SubmitField('Create')
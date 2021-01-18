from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField,validators

class FoodReviewForm(FlaskForm):
	
	summary = TextAreaField("Enter your summary review ",[validators.DataRequired("This feild is required"),validators.InputRequired("This feild is required")])
	text = TextAreaField("Enter your detailed review",[validators.DataRequired("This feild is required"),validators.InputRequired("This feild is required")]) 
	submit = SubmitField("Submit")
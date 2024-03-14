from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, PasswordField, SelectField, DateField
from wtforms.fields import FileField
from wtforms.validators import DataRequired, URL


##WTForm


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")


class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    date = DateField("Date", validators=[DataRequired()])
    post_type = SelectField('Select an Option', choices=[('personal Story/Reflection', 'Personal Story/Reflection'),
                                                           ('social_impact', 'Social Impact'),
                                                           ('project_showcase', 'Project Showcase'),
                                                           ('tutorial_guide', 'Tutorial/Guide'), ('other', 'Other')])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    file_image = FileField('Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only JPG, JPEG, PNG, and GIF images are allowed.'),
        DataRequired('Please choose an image to upload.')
    ])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


class PostCommentForm(FlaskForm):
    comment_text = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Add Comment")


class CreateProjectForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    date = DateField("Date", validators=[DataRequired()])
    project_type = SelectField('Project Type', choices=[('Automation', 'Automation'),
                                                        ('IoT & Embedded Projects', 'IoT & Embedded Projects'),
                                                        ('Security & Ethical Hacking', 'Security & Ethical Hacking'),
                                                        ('Software Development', 'Software Development'),
                                                        ('Other', 'Other')])
    image = FileField('Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only JPG, JPEG, PNG, and GIF images are allowed.'),
        DataRequired('Please choose an image to upload.')
    ])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Project")


class ProjectCommentForm(FlaskForm):
    comment_text = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")

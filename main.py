from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from helper.form import CreatePostForm, CreateProjectForm, RegisterForm, LoginForm
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
db = SQLAlchemy(app)
ckeditor = CKEditor(app)
Bootstrap(app=app)
login_manager = LoginManager()
login_manager.init_app(app)


# SELECT * FROM amc_data LIMIT 1
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    posts = relationship("BlogPost", back_populates="author")
    post_comments = relationship("PostComment", back_populates="comment_author")
    project = relationship("Project", back_populates="author")
    project_comment = relationship("ProjectComment", back_populates="comment_author")


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    post_type = db.Column(db.String(30), nullable=False)
    body = db.Column(db.Text, nullable=False)
    image = db.Column(db.LargeBinary, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
    comments = relationship("PostComment", back_populates="parent_post")


class PostComment(db.Model):
    __tablename__ = "post_comments"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    parent_post = relationship("BlogPost", back_populates="comments")
    comment_author = relationship("User", back_populates="post_comments")
    text = db.Column(db.Text, nullable=False)


class Project(db.Model):
    __tablename__ = "project"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    image = db.Column(db.LargeBinary, nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    project_type = db.Column(db.String(30), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="project")
    comments = relationship("ProjectComment", back_populates="parent_project")


class ProjectComment(db.Model):
    __tablename__ = "project_comments"
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    parent_project = relationship("Project", back_populates="comments")
    comment_author = relationship("User", back_populates="project_comment")
    text = db.Column(db.Text, nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("basic-information/home.html", current_user=current_user)


@app.route("/about")
def about():
    return render_template("basic-information/about.html", current_user=current_user)


@app.route("/contact")
def contact():
    return render_template("basic-information/contact.html", current_user=current_user)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        if User.query.filter_by(email=form.email.data).first():
            print(User.query.filter_by(email=form.email.data).first())
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))

    return render_template("user_login/register.html", form=form, current_user=current_user)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        # Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template("user_login/login.html", form=form, current_user=current_user)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/blog/<category>")
def blog(category):
    if category != "all":
        blog = db.session.execute(db.Select(BlogPost).Where(BlogPost.post_type == category)).fetchall()
    else:
        blog = db.session.query(BlogPost)
    return render_template("blogs/blogs.html", current_user=current_user, blog=blog)


@app.route("/post/<int:post_id>")
def post_detail(post_id):
    post = None
    return render_template("blogs/post-detail.html", post)


@app.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = BlogPost(
            date = form.date.data,
            title = form.title.data,
            subtitle = form.subtitle.data,
            body = form.body.data,
            post_type = form.post_type.data,
            image = form.file_image.data.read(),
            author_id = current_user.id
        )
        db.session.add(post)
        db.session.commit()
    return render_template('blogs/create-post.html', form=form, current_user=current_user)


@app.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    pass


@app.route("/project/<category>")
def project(category):
    return render_template("projects/projects.html", current_user=current_user)


@app.route("/project-detail/<int:project_id>")
def project_detail(project_id):
    return render_template("projects/project-detail.html")


@app.route('/create-project', methods=['GET', 'POST'])
@login_required
def create_project():
    form = CreateProjectForm()
    if form.validate_on_submit():
        project = Project(
            date=form.date.data,
            title=form.title.data,
            description=form.description.data,
            body=form.body.data,
            project_type=form.project_type.data,
            image=form.file_image.data.read(),
            author_id=current_user.id
        )
        db.session.add(project)
        db.session.commit()
        # print(form.file_image.data)
        # filename= form.file_image.data
        # image_data = filename.read()
        # print(type(image_data))

    return render_template('projects/create-project.html', form=form, current_user=current_user)


@app.route('/edit-project/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit_project():
    pass


if __name__ == "__main__":
    app.run(debug=True)

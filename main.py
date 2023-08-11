from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("basic-information/home.html")


@app.route("/about")
def about():
    return render_template("basic-information/about.html")


@app.route("/contact")
def contact():
    return render_template("basic-information/contact.html")


@app.route("/blog")
def blog():
    return render_template("blogs/blogs.html")


@app.route("/blog/detail")
def post_detail():
    return render_template("blogs/post-detail.html")


@app.route("/project")
def project():
    return render_template("projects/projects.html")


@app.route("/project/detail")
def project_detail():
    return render_template("projects/project-detail.html")


if __name__ == "__main__":
    app.run(debug=True)

import os
from flask import Flask
from flask import request, render_template, redirect, url_for, jsonify
import flask_login
from annotation.application.document import Document
from annotation.application.aspect_sentiment_task import AspectSntimentTask


app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data/interim")
ANNOTATE_DIR = os.path.join(os.path.dirname(__file__), "../../data/annotated")

# Login Feature
app.secret_key = os.getenv("SECRET_KEY", "__YOUR__SECRET_KEY__")
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(flask_login.UserMixin):
    LOGINED = {}

    def __init__(self, id, authorized=False):
        self.id = id
        self.authenticated = authorized

    @property
    def is_authenticated(self):
        return self.authenticated

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


@login_manager.user_loader
def user_loader(user_id):
    if user_id in User.LOGINED:
        return User.LOGINED[user_id]
    else:
        return User(user_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", error=False)

    user_id = request.form["user_id"]
    password = request.form["password"]
    if password == os.getenv("LOGIN_PASSWORD", "__YOUR_PASSWORD__"):
        user = User(user_id, True)
        User.LOGINED[user_id] = user
        flask_login.login_user(user)
        return redirect(url_for("index"))

    return render_template("login.html", error=True)


@app.route("/logout")
@flask_login.login_required
def logout():
    del User.LOGINED[flask_login.current_user.id]
    flask_login.logout_user()
    return redirect(url_for("login"))


# Application
@app.route("/")
@flask_login.login_required
def index():
    return render_template("index.html")


@app.route("/documents")
@flask_login.login_required
def documents():
    documents = []
    for f in sorted(os.listdir(DATA_DIR)):
        path = os.path.join(DATA_DIR, f)
        if os.path.isfile(path) and not f.startswith("."):
            name, _ = os.path.splitext(f)
            name = name.upper()
            annotated = os.path.join(ANNOTATE_DIR, name)
            exist = False
            if os.path.exists(annotated):
                exist = True
            documents.append({"edi_id": name, "done": exist})

    return jsonify({"documents": documents})


@app.route("/document/<item_id>", methods=["GET", "POST"])
@flask_login.login_required
def get_document(item_id=None):
    annotator = flask_login.current_user.get_id()
    if not item_id:
        r = jsonify({"message": "No item id is specified"})
        r.status_code = 400
        return r
    else:
        path = os.path.join(DATA_DIR, item_id.lower() + ".jsonl")
        if not os.path.isfile(path):
            r = jsonify({"message": "Selected item id does not exist."})
            r.status_code = 400
            return r

        doc = Document.load(path)
        task = AspectSntimentTask.load(ANNOTATE_DIR, doc, annotator)

        if request.method == "POST":
            posted = request.json
            annotation_objs = posted["annotations"]
            task.save_annotations(ANNOTATE_DIR, annotation_objs, annotator)
            return jsonify({})
        else:
            labels = task.get_labels()
            labels = [label.dumps() for label in labels]
            r = jsonify({
                "header": doc.get_header(),
                "labels": labels,
                "tasks": task.get_dataset()
            })
            return r

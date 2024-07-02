from flask import Flask,request
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello,World !</p>"

# @app.route("/<firstname>")
# def hello(firstname):
#     return f" hello, {escape(firstname)}!"

@app.route('/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/pat/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'

@app.route("/userdetail/<int:user_id>", methods=['GET', 'POST','PATCH'])
def user_details(user_id):
    if request.method == 'PATCH':
        return f" user {user_id} requesting to patch"
    elif request.method == 'GET':
        return f"user {escape(user_id)} listing "

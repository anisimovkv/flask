from flask import Blueprint
from flask import render_template

from ..model import Post

posts = Blueprint('posts', __name__, template_folder='templates')


# search_word = 'blblblb'
# Post.query.filter(Post.title.ilike('%{search_word}%')).all()

@posts.route('/')
def index():
    posts_list = Post.query.all()
    return render_template('posts/post_index.html', posts=posts_list)


@posts.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first()
    print(post)
    return render_template('posts/post_detail.html', post=post)

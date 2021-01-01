from flask import Blueprint
from flask import render_template

from ..model import Post, Tag

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
    return render_template('posts/post_detail.html', post=post)


@posts.route('/tag/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first()
    posts = tag.posts.all()
    return render_template('posts/tag_detail.html', tag=tag, posts=posts)

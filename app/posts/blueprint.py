from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from sqlalchemy import exc

from ..model import Post, Tag
from ..app import db
from .forms import PostForm

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/create', methods=['GET', 'POST'])
def post_create():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        try:
            post = Post(title=title, body=body)
            db.session.add(post)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            print(e)

        return redirect(url_for('posts.index'))

    form = PostForm()
    return render_template('posts/post_create.html', form=form)


@posts.route('/')
def index():
    search_word = request.args.get('search')
    if search_word:
        posts_list = Post.query.filter(
            Post.title.ilike(f'%{search_word}%') |
            Post.body.ilike(f'%{search_word}%')).all()
    else:
        posts_list = Post.query.order_by(Post.date_created.desc())
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

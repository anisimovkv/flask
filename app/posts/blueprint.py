from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from sqlalchemy import exc

from .forms import PostForm
from ..app import db
from ..model import Post, Tag

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


@posts.route('/<slug>/edit/', methods=['POST', 'GET'])
def post_edit(slug):
    post = Post.query.filter(Post.slug == slug).first()
    if request.method == 'POST':
        form: PostForm = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        try:
            db.session.commit()
        except exc.SQLAlchemyError as e:
            print(e)
        return redirect(url_for('posts.post_detail', slug=post.slug))
    form = PostForm(obj=post)
    return render_template('posts/post_edit.html', post=post, form=form)


@posts.route('/')
def index():
    search_word = request.args.get('search')
    raw_page: str = request.args.get('page')
    if raw_page and raw_page.isdigit():
        page: int = int(raw_page)
    else:
        page = 1

    if search_word:
        posts_objects = Post.query.filter(
            Post.title.ilike(f'%{search_word}%') |
            Post.body.ilike(f'%{search_word}%'))  # .all()
    else:
        posts_objects = Post.query.order_by(Post.date_created.desc())

    pages = posts_objects.paginate(page=page, per_page=3)

    return render_template(
        'posts/post_index.html', posts=posts_objects, pages=pages)


@posts.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first()
    return render_template('posts/post_detail.html', post=post)


@posts.route('/tag/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first()
    posts = tag.posts.all()
    return render_template('posts/tag_detail.html', tag=tag, posts=posts)

import re
from datetime import datetime

from flask_security import UserMixin, RoleMixin
from sqlalchemy.schema import Column, Table

from .app import db


def slugify(string: str) -> str:
    pattern: str = r'[^\w+]'
    raw_string: str = re.sub(pattern, '-', string).lower()
    raw_string += '-'
    l: list = [
        raw_string[i] for i in range(len(raw_string) - 1) if
        raw_string[i] != raw_string[i + 1] and raw_string != '-'
    ]
    return ''.join(l)


# many to many
post_tags: Table = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.now())
    tags = db.relationship(
        'Tag', secondary=post_tags,
        backref=db.backref('posts', lazy='dynamic'))

    def generate_slug(self):
        self.slug = slugify(self.title)

    # def __init__(self, *args, **kwargs):
    #     if not 'slug' in kwargs:
    #         kwargs['slug'] = slugify(kwargs.get('title', ''))
    #     super().__init__(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return f'{self.title}'


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    slug = db.Column(db.String(100))

    def generate_slug(self):
        self.slug = slugify(self.name)

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    # def __init__(self, *args, **kwargs):
    #     if not 'slug' in kwargs:
    #         kwargs['slug'] = slugify(kwargs.get('name', ''))
    #     super().__init__(*args, **kwargs)

    def __repr__(self):
        return f'{self.name}'


# many to many
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship("Role", secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))

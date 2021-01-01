import re
from datetime import datetime
from .app import db
from sqlalchemy.schema import Column, Table


def slugify(string: str) -> str:
    pattern: str = r'[^\w+]'
    raw_string: str = re.sub(pattern, '-', string).lower()
    raw_string += '-'
    l: list = [
        raw_string[i] for i in range(len(raw_string) - 1) if
        raw_string[i] != raw_string[i + 1] and raw_string != '-'
    ]
    return ''.join(l)


post_tags: Table = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)


class Post(db.Model):
    id: Column = db.Column(db.Integer, primary_key=True)
    title: Column = db.Column(db.String(140))
    slug: Column = db.Column(db.String(140), unique=True)
    body: Column = db.Column(db.Text)
    date_created: Column = db.Column(db.DateTime, default=datetime.now())
    tags = db.relationship(
        'Tag', secondary=post_tags,
        backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return f'<Post id {self.id}, title {self.title}>'


class Tag(db.Model):
    id: Column = db.Column(db.Integer, primary_key=True)
    name: Column = db.Column(db.String(100))
    slug: Column = db.Column(db.String(100))

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __repr__(self):
        return f'<Tag id {self.id}, title {self.name}>'

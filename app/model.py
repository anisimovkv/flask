import re
from datetime import datetime

from .app import db


def slugify(string: str) -> str:
    pattern: str = r'[^\w+]'
    raw_string = re.sub(pattern, '-', string).lower()
    raw_string += '-'
    l = [
        raw_string[i] for i in range(len(raw_string) - 1) if
        raw_string[i] != raw_string[i + 1] and raw_string != '-'
    ]
    return ''.join(l)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return f'<Post id {self.id}, title {self.title}>'

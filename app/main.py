from .posts.blueprint import posts
from .view import *

app.register_blueprint(posts, url_prefix='/blog')

if __name__ == "__main__":
    app.run()

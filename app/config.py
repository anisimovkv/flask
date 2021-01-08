class Configuration(object):
    DEBUG: bool = True
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_DATABASE_URI: str = 'postgresql://postgres:123@localhost/test1'
    SECRET_KEY = 'asdfkjasdkfj dasfkfj ;asdfj;ak adkfj qieurtiunb'
    # flask security
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'

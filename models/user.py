from models.follow import Follow
from models.mongoo import Mongoo


class User(Mongoo):
    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('username', str, ''),
            ('password', str, ''),
            ('user_image', str, '/uploads/default.png'),
        ]
        return names

    def salted_password(self, password, salt='$!@><?>HUI&DWQa`'):
        import hashlib

        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()

        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    def hashed_password(self, pwd):
        import hashlib

        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        return s.hexdigest()

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')
        if len(name) > 2 and User.find_by(username=name) is None:
            # create user model
            u = User.new(form)
            u.password = u.salted_password(pwd)
            u.save()
            # create follow model
            f = Follow.new(user_id=u.id)
            f.save()
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        user = User.find_by(username=form['username'])
        if user is not None and user.password == user.salted_password(password=form['password']):
            return user
        else:
            return None

    @classmethod
    def change_password(cls, form):
        u = User.find_by(username=form.get('username', ''))
        old_pwd = form.get('old-password', '')
        new_pwd = form.get('new-password', '')
        confirm_pwd = form.get('confirm-password', '')
        if u.salted_password(old_pwd) == u.password and new_pwd == confirm_pwd:
            u.password = u.salted_password(new_pwd)
            u.save()
            return u
        else:
            return None

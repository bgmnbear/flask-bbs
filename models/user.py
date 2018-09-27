# from models import Model
from models.follow import Follow
from models.mongoo import Mongoo


class User(Mongoo):
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """

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
        # 用 ascii 编码转换成 bytes 对象
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        # 返回摘要字符串
        return s.hexdigest()

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')
        if len(name) > 2 and User.find_by(username=name) is None:
            u = User.new(form)
            u.password = u.salted_password(pwd)

            f = Follow.new(user_id=u.id)

            u.save()
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
        o_p = form.get('old-password', '')
        n_p = form.get('new-password', '')
        c_p = form.get('confirm-password', '')
        if u.salted_password(o_p) == u.password and n_p == c_p:
            u.password = u.salted_password(n_p)
            u.save()
            return u
        else:
            return None

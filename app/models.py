from . import db
import bleach
from markdown import markdown
from datetime import datetime


# 短信接收相关表
class SMS_Receive(db.Model):
    __tablename__ = 'SMS_Receive'
    id = db.Column(db.Integer, primary_key=True)
    PhoneNumber = db.Column(db.String(32))
    Content = db.Column(db.String(512))
    SMS_ReceiveTime = db.Column(db.DateTime, index=True)
    Type = db.Column(db.String(32))
    # 是否显示，如果电话号码在黑名单不显示，否则显示
    IsShow = db.Column(db.Boolean, default=True)


# 电话黑名单
class blacklist(db.Model):
    __tablename__ = 'blacklist'
    id = db.Column(db.Integer, primary_key=True, index=True)
    PhoneNumber = db.Column(db.String(32))


# 文章相关表
class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    seo_link = db.Column(db.String(128))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'img', 'video', 'div', 'iframe', 'p', 'br', 'span', 'hr', 'src', 'class']
        allowed_attrs = {'*': ['class'],
                         'a': ['href', 'rel'],
                         'img': ['src', 'alt']}
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True, attributes=allowed_attrs))


db.event.listen(Article.body, 'set', Article.on_changed_body)

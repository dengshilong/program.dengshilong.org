title: SQLAlchemy之relationship之remote_side
date: 2017-04-17 20:31:32
tags:
    - Python
    - SQLAlchemy
categories:
---
需要给每个user添加一个leader, 于是在user表里添加leader, 而leader也是一个user, 于是构成了自引用。
```
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(10))
    addresses = relationship("Address", back_populates="user")
    leader_id = db.Column(Integer, ForeignKey('users.id'))
    users = relationship("User", back_populates="leader")
    leader = relationship("User", back_populates="users", remote_side=[id])

    def __repr__(self):
        return u'<user id={0}, name={1}>'.format(self.id, self.name).encode('utf-8')
```
提示如下错误，

ArgumentError: User.users and back-reference User.leader are both of the same direction symbol('MANYTOONE').  Did you mean to set remote_side on the many-to-one side ?

最后参考StackOverFlow上[One to one self relationship in SQLAlchemy](http://stackoverflow.com/questions/12872873/one-to-one-self-relationship-in-sqlalchemy)和[SQLAlchemy One-to-Many relationship on single table inheritance - declarative](http://stackoverflow.com/questions/6782133/sqlalchemy-one-to-many-relationship-on-single-table-inheritance-declarative)
添加[remote_side](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship.params.remote_side)解决问题.

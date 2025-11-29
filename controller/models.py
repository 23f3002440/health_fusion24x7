from controller.database import db

class User(db.Model):
    
    # __tablename__ = 'user'
    
    user_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_name = db.Column(db.String(50), nullable=False)
    user_email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

    roles = db.relationship('Role', secondary = 'user_role', backref = 'users', lazy = True)
    customer_details = db.relationship('Customer', backref='user', lazy=True, uselist=False)
    store_manager_details = db.relationship('StoreManager', backref='user', lazy=True, uselist=False)
    
    
# store_manager = StoreManager(qualification='Bsc')
# user = User(user_email, password, user_name, store_manager_details=store_manager)
# db.session.commit()
    
class Role(db.Model):
    
    #__tablename__ = 'role'
    
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    
class UserRole(db.Model):
    
    # __tablename__ = 'user_role'
    
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    
class StoreManager(db.Model):
    
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    qualification = db.Column(db.String(100), nullable=False)
    
class Customer(db.Model):
    
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    address = db.Column(db.String(50), nullable=False)
    prefered_mode_of_payment = db.Column(db.String(50), nullable=False)
    phone_number= db.Column(db.String(50), nullable=False)
    
from setup import db, app, api

class Product(db.Model):
    __tablename__ = 'Product'
    name = db.Column(db.String, primary_key=True)
    density = db.Column(db.Float)
    proportions = db.Column(db.Float)
    kcal = db.Column(db.Integer)
    carbs = db.Column(db.Float)
    fats = db.Column(db.Float)
    proteins = db.Column(db.Float)

    def __init__(self, name, density, proportions, kcal, carbs, fats, proteins):
        self.name = name
        self.density = density
        self.proportions = proportions
        self.kcal = kcal
        self.carbs = carbs
        self.fats = fats
        self.proteins = proteins

class User(db.Model):
    __tablename__ = 'User'
    user_id = db.Column(db.Integer, primary_key=True) 

class Food(db.Model):

    __tablename__ = 'Food'
    food_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User'))
    user = db.relationship(
        User, backref=db.backref("user_food", uselist=False))
    name = db.Column(db.String)
    weight = db.Column(db.Integer)
    kcal = db.Column(db.Integer)
    carbs = db.Column(db.Integer)
    fats = db.Column(db.Integer)
    proteins = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    def __init__(
        self, user_id, name, weight, kcal, carbs, fats, proteins, date
    ):
        self.user_id = user_id
        self.name = name
        self.weight = weight
        self.kcal = kcal
        self.carbs = carbs
        self.fats = fats
        self.proteins = proteins
        self.date = date




    #def __init__(
    #    self, uuid, email, password,
    #    phone, avatar, ips, oauth_user
    #):
    #    self.uuid = uuid
    #    self.email = email
    #    self.password = password
    #    self.phone = phone
    #    self.avatar = avatar
    #    self.ips = ips
    #    self.registration_date = str(datetime.today())
    #    self.acceptable_token_creation_date = str(datetime.today())
    #    self.oauth_user = oauth_user


#   table for all pixels related data, core of the app
#   one row stores data of user's ratings for one year,
#   the ratings data is stored as a string in
#   format: "r,r,r,...,r" (called year-to-string format in documentation)
#   where r is a rating for a given day, so there is either
#   365 or 366 ratings in a given row and first r is for the 1st of january
#   and last is for the 31st december of a given year,
#   an empty (not filled by user) day always has rating equal to 0
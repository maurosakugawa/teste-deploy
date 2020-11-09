from app import db


class Categories(db.Model):
    __tablename__ = 'categories'

    category = db.Column(db.Integer, primary_key=True)
    categoryname = db.Column(db.String(50), nullable=False)


class Products(db.Model):
    __tablename__ = 'products'

    prod_id = db.Column(db.Integer, primary_key=True)
    categoryid = db.Column('category',
        db.Integer, db.ForeignKey('categories.category'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    actor = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(precision=12, scale=2), nullable=False)
    special = db.Column(db.Integer, nullable=True)
    common_prod_id = db.Column(db.Integer, nullable=False)
    category = db.relationship('Categories')
    inventory = db.relationship('Inventory', uselist=False)
    reorder = db.relationship('Reorder', uselist=False)


class Inventory(db.Model):
    __tablename__ = 'inventory'

    prod_id = db.Column(db.Integer,
        db.ForeignKey('products.prod_id'), primary_key=True)
    quan_in_stock = db.Column(db.Integer, nullable=False)
    sales = db.Column(db.Integer, nullable=False)


class Reorder(db.Model):
    __tablename__ = 'reorder'

    prod_id = db.Column(
        db.Integer, db.ForeignKey('products.prod_id'), primary_key=True)
    date_low = db.Column(db.DateTime, nullable=False)
    quan_low = db.Column(db.Integer, nullable=False)
    date_reordered = db.Column(db.DateTime, nullable=True)
    quan_reordered = db.Column(db.Integer, nullable=True)
    date_expected = db.Column(db.DateTime, nullable=True)

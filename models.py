from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Spreadsheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

class Cell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cell_id = db.Column(db.String, nullable=False)
    spreadsheet_id = db.Column(db.Integer, db.ForeignKey('spreadsheet.id'), nullable=False)
    value = db.Column(db.String)
    formula_string = db.Column(db.String)

class CellDependency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spreadsheet_id = db.Column(db.Integer, db.ForeignKey('spreadsheet.id'), nullable=False)
    from_cell = db.Column(db.String, nullable=False)
    to_cell = db.Column(db.String, nullable=False)

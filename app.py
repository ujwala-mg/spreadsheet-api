from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Spreadsheet, Cell, CellDependency

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spreadsheet.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables if not exist
with app.app_context():
    db.create_all()

# ✅ API: Set value for a cell
@app.route('/spreadsheets/<int:sheet_id>/cells/<string:cell_id>/value', methods=['POST'])
def set_cell_value(sheet_id, cell_id):
    data = request.get_json()
    value = data.get('value')

    if not value:
        return jsonify({'error': 'Value is required'}), 400

    # check if cell exists
    cell = Cell.query.filter_by(spreadsheet_id=sheet_id, cell_id=cell_id).first()

    if not cell:
        cell = Cell(spreadsheet_id=sheet_id, cell_id=cell_id)

    cell.value = str(value)
    cell.formula_string = None  # clear formula if value set manually
    db.session.add(cell)
    db.session.commit()

    return jsonify({
        'spreadsheet_id': sheet_id,
        'cell_id': cell_id,
        'value': value,
        'status': 'value_set'
    })

# ✅ Add dummy spreadsheet (ID=1) if not exists
with app.app_context():
    if not Spreadsheet.query.get(1):
        test_sheet = Spreadsheet(id=1, name="Test Sheet")
        db.session.add(test_sheet)
        db.session.commit()

# ✅ Start the app
if __name__ == '__main__':
    print("Spreadsheet API is working!")
    app.run(debug=True)

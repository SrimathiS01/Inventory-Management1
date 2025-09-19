from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Product(db.Model):
    product_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Product {self.product_id}: {self.name}>'

class Location(db.Model):
    location_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Location {self.location_id}: {self.name}>'

class ProductMovement(db.Model):
    movement_id = db.Column(db.String(50), primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    from_location = db.Column(db.String(50), db.ForeignKey('location.location_id'), nullable=True)
    to_location = db.Column(db.String(50), db.ForeignKey('location.location_id'), nullable=True)
    product_id = db.Column(db.String(50), db.ForeignKey('product.product_id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    
    # Relationships
    product = db.relationship('Product', backref='movements')
    from_loc = db.relationship('Location', foreign_keys=[from_location], backref='outgoing_movements')
    to_loc = db.relationship('Location', foreign_keys=[to_location], backref='incoming_movements')
    
    def __repr__(self):
        return f'<Movement {self.movement_id}: {self.qty} of {self.product_id}>'

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showcase')
def showcase():
    products_count = Product.query.count()
    locations_count = Location.query.count()
    movements_count = ProductMovement.query.count()
    return render_template('showcase.html',
                           products_count=products_count,
                           locations_count=locations_count,
                           movements_count=movements_count)

# Product Routes
@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product = Product(
            product_id=request.form['product_id'],
            name=request.form['name'],
            description=request.form['description']
        )
        try:
            db.session.add(product)
            db.session.commit()
            flash('Product added successfully!', 'success')
            return redirect(url_for('products'))
        except Exception as e:
            flash(f'Error adding product: {str(e)}', 'error')
    return render_template('add_product.html')

@app.route('/products/edit/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        try:
            db.session.commit()
            flash('Product updated successfully!', 'success')
            return redirect(url_for('products'))
        except Exception as e:
            flash(f'Error updating product: {str(e)}', 'error')
    return render_template('edit_product.html', product=product)

@app.route('/products/view/<product_id>')
def view_product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('view_product.html', product=product)

# Location Routes
@app.route('/locations')
def locations():
    locations = Location.query.all()
    return render_template('locations.html', locations=locations)

@app.route('/locations/add', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        location = Location(
            location_id=request.form['location_id'],
            name=request.form['name'],
            description=request.form['description']
        )
        try:
            db.session.add(location)
            db.session.commit()
            flash('Location added successfully!', 'success')
            return redirect(url_for('locations'))
        except Exception as e:
            flash(f'Error adding location: {str(e)}', 'error')
    return render_template('add_location.html')

@app.route('/locations/edit/<location_id>', methods=['GET', 'POST'])
def edit_location(location_id):
    location = Location.query.get_or_404(location_id)
    if request.method == 'POST':
        location.name = request.form['name']
        location.description = request.form['description']
        try:
            db.session.commit()
            flash('Location updated successfully!', 'success')
            return redirect(url_for('locations'))
        except Exception as e:
            flash(f'Error updating location: {str(e)}', 'error')
    return render_template('edit_location.html', location=location)

@app.route('/locations/view/<location_id>')
def view_location(location_id):
    location = Location.query.get_or_404(location_id)
    return render_template('view_location.html', location=location)

# Product Movement Routes
@app.route('/movements')
def movements():
    movements = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).all()
    return render_template('movements.html', movements=movements)

@app.route('/movements/add', methods=['GET', 'POST'])
def add_movement():
    if request.method == 'POST':
        movement = ProductMovement(
            movement_id=request.form['movement_id'],
            from_location=request.form['from_location'] if request.form['from_location'] else None,
            to_location=request.form['to_location'] if request.form['to_location'] else None,
            product_id=request.form['product_id'],
            qty=int(request.form['qty'])
        )
        try:
            db.session.add(movement)
            db.session.commit()
            flash('Movement added successfully!', 'success')
            return redirect(url_for('movements'))
        except Exception as e:
            flash(f'Error adding movement: {str(e)}', 'error')
    
    products = Product.query.all()
    locations = Location.query.all()
    return render_template('add_movement.html', products=products, locations=locations)

@app.route('/movements/edit/<movement_id>', methods=['GET', 'POST'])
def edit_movement(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    if request.method == 'POST':
        movement.from_location = request.form['from_location'] if request.form['from_location'] else None
        movement.to_location = request.form['to_location'] if request.form['to_location'] else None
        movement.product_id = request.form['product_id']
        movement.qty = int(request.form['qty'])
        try:
            db.session.commit()
            flash('Movement updated successfully!', 'success')
            return redirect(url_for('movements'))
        except Exception as e:
            flash(f'Error updating movement: {str(e)}', 'error')
    
    products = Product.query.all()
    locations = Location.query.all()
    return render_template('edit_movement.html', movement=movement, products=products, locations=locations)

@app.route('/movements/view/<movement_id>')
def view_movement(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    return render_template('view_movement.html', movement=movement)

# Balance Report Route
@app.route('/balance')
def balance_report():
    # Calculate balance for each product in each location
    balance_data = {}
    
    # Get all movements
    movements = ProductMovement.query.all()
    
    for movement in movements:
        product_id = movement.product_id
        qty = movement.qty
        
        # Initialize product in balance_data if not exists
        if product_id not in balance_data:
            balance_data[product_id] = {}
        
        # Handle incoming movements (to_location)
        if movement.to_location:
            if movement.to_location not in balance_data[product_id]:
                balance_data[product_id][movement.to_location] = 0
            balance_data[product_id][movement.to_location] += qty
        
        # Handle outgoing movements (from_location)
        if movement.from_location:
            if movement.from_location not in balance_data[product_id]:
                balance_data[product_id][movement.from_location] = 0
            balance_data[product_id][movement.from_location] -= qty
    
    # Convert to list format for template
    balance_list = []
    products = Product.query.all()
    locations = Location.query.all()
    
    product_dict = {p.product_id: p.name for p in products}
    location_dict = {l.location_id: l.name for l in locations}
    
    for product_id, locations_data in balance_data.items():
        for location_id, qty in locations_data.items():
            if qty != 0:  # Only show non-zero balances
                balance_list.append({
                    'product_id': product_id,
                    'product_name': product_dict.get(product_id, product_id),
                    'location_id': location_id,
                    'location_name': location_dict.get(location_id, location_id),
                    'qty': qty
                })
    
    return render_template('balance_report.html', balance_list=balance_list)

# API Endpoints - Analytics
@app.route('/api/metrics')
def api_metrics():
    products_count = Product.query.count()
    locations_count = Location.query.count()
    movements_count = ProductMovement.query.count()
    return jsonify({
        'products': products_count,
        'locations': locations_count,
        'movements': movements_count
    })

@app.route('/api/movements_trend')
def api_movements_trend():
    from datetime import timedelta
    today = datetime.utcnow().date()
    start_date = today - timedelta(days=6)  # last 7 days including today
    # Initialize date map
    date_map = { (start_date + timedelta(days=i)).isoformat(): 0 for i in range(7) }

    movements = ProductMovement.query.filter(ProductMovement.timestamp >= datetime.combine(start_date, datetime.min.time())).all()
    for m in movements:
        d = m.timestamp.date().isoformat()
        if d in date_map:
            date_map[d] += 1
    labels = sorted(date_map.keys())
    data = [date_map[d] for d in labels]
    return jsonify({'labels': labels, 'data': data})

@app.route('/api/top_products')
def api_top_products():
    # Aggregate quantity moved per product (absolute qty)
    from sqlalchemy import func
    rows = db.session.query(
        ProductMovement.product_id,
        func.sum(func.abs(ProductMovement.qty)).label('total_qty')
    ).group_by(ProductMovement.product_id).order_by(func.sum(func.abs(ProductMovement.qty)).desc()).limit(5).all()

    # Map IDs to names
    product_names = {p.product_id: p.name for p in Product.query.all()}
    labels = [product_names.get(pid, pid) for pid, _ in rows]
    data = [int(total or 0) for _, total in rows]
    return jsonify({'labels': labels, 'data': data})

@app.route('/api/recent_movements')
def api_recent_movements():
    recents = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).limit(10).all()
    items = []
    for m in recents:
        items.append({
            'movement_id': m.movement_id,
            'timestamp': m.timestamp.isoformat(),
            'product_id': m.product_id,
            'from_location': m.from_location,
            'to_location': m.to_location,
            'qty': m.qty
        })
    return jsonify({'items': items})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

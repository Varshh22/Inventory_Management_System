from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from functools import wraps
from models import db, User, Product, Location, ProductMovement
from methods import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'inventory-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
@login_required
def index():
    stats = get_dashboard_stats()
    recent_movements = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).limit(5).all()
    
    
    for movement in recent_movements:
        
        product = Product.query.get(movement.product_id)
        movement.product_name = product.name if product else movement.product_id
        
        
        if movement.from_location:
            from_loc = Location.query.get(movement.from_location)
            movement.from_location_name = from_loc.name if from_loc else movement.from_location
        else:
            movement.from_location_name = None
            
       
        if movement.to_location:
            to_loc = Location.query.get(movement.to_location)
            movement.to_location_name = to_loc.name if to_loc else movement.to_location
        else:
            movement.to_location_name = None
    
    return render_template('index.html', stats=stats, recent_movements=recent_movements)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return handle_register(request)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return handle_login(request, session)
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/products')
@login_required
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        return handle_add_product(request)
    
    locations = Location.query.all()
    return render_template('product_form.html', locations=locations)

@app.route('/products/edit/<product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    if request.method == 'POST':
        return handle_edit_product(product_id, request)
    
    product = Product.query.get_or_404(product_id)
    return render_template('product_form.html', product=product, edit=True)

@app.route('/products/delete/<product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    return handle_delete_product(product_id)


@app.route('/locations')
@login_required
def locations():
    locations = Location.query.all()
    return render_template('locations.html', locations=locations)

@app.route('/locations/add', methods=['GET', 'POST'])
@login_required
def add_location():
    if request.method == 'POST':
        return handle_add_location(request)
    return render_template('location_form.html')

@app.route('/locations/edit/<location_id>', methods=['GET', 'POST'])
@login_required
def edit_location(location_id):
    if request.method == 'POST':
        return handle_edit_location(location_id, request)
    
    location = Location.query.get_or_404(location_id)
    return render_template('location_form.html', location=location, edit=True)

@app.route('/locations/delete/<location_id>', methods=['POST'])
@login_required
def delete_location(location_id):
    return handle_delete_location(location_id)

# Movement Routes
@app.route('/movements')
@login_required
def movements():
    movements = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).all()
    
    
    for movement in movements:
        
        product = Product.query.get(movement.product_id)
        movement.product_name = product.name if product else movement.product_id
        
        
        if movement.from_location:
            from_loc = Location.query.get(movement.from_location)
            movement.from_location_name = from_loc.name if from_loc else movement.from_location
        else:
            movement.from_location_name = None
            
        
        if movement.to_location:
            to_loc = Location.query.get(movement.to_location)
            movement.to_location_name = to_loc.name if to_loc else movement.to_location
        else:
            movement.to_location_name = None
    
    return render_template('movements.html', movements=movements)

@app.route('/movements/add', methods=['GET', 'POST'])
@login_required
def add_movement():
    if request.method == 'POST':
        return handle_add_movement(request)
    
    
    products = Product.query.all()
    all_locations = Location.query.all()
    
    return render_template('movement_form.html', 
                         products=products,
                         locations=all_locations,
                         locations_with_stock=None)

@app.route('/movements/edit/<movement_id>', methods=['GET', 'POST'])
@login_required
def edit_movement(movement_id):
    if request.method == 'POST':
        return handle_edit_movement(movement_id, request)
    
    movement = ProductMovement.query.get_or_404(movement_id)
    return render_template('movement_form.html', 
                         movement=movement,
                         products=Product.query.all(),
                         locations=Location.query.all(),
                         edit=True)

@app.route('/movements/delete/<movement_id>', methods=['POST'])
@login_required
def delete_movement(movement_id):
    return handle_delete_movement(movement_id)


@app.route('/api/locations_with_stock/<product_id>')
@login_required
def get_locations_with_stock(product_id):
    locations = get_locations_with_product(product_id)
    return jsonify({'locations': locations})


@app.route('/reports/balance')
@login_required
def balance_report():
    balance_data = generate_balance_report()
    return render_template('balance_report.html', balance_data=balance_data)


def init_db():
    with app.app_context():
        db.create_all()
        initialize_sample_data()
        print("Database initialized!")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
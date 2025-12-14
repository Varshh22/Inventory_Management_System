from flask import redirect, url_for, flash
from werkzeug.security import check_password_hash
from datetime import datetime
from models import db, User, Product, Location, ProductMovement, get_ist_now


def handle_register(request):
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    
    if password != confirm_password:
        flash('Passwords do not match!', 'danger')
        return redirect(url_for('register'))
    
    if User.query.filter_by(username=username).first():
        flash('Username already exists!', 'danger')
        return redirect(url_for('register'))
    
    if User.query.filter_by(email=email).first():
        flash('Email already exists!', 'danger')
        return redirect(url_for('register'))
    
    user = User(
        username=username,
        email=email
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    flash('Registration successful! Please log in.', 'success')
    return redirect(url_for('login'))

def handle_login(request, session):
    username = request.form['username']
    password = request.form['password']
    
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password_hash, password):
        session['user_id'] = user.id
        session['username'] = user.username
        flash(f'Welcome back, {user.username}!', 'success')
        return redirect(url_for('index'))
    else:
        flash('Invalid username or password!', 'danger')
        return redirect(url_for('login'))


def handle_add_product(request):
    product_id = request.form['product_id']
    if Product.query.get(product_id):
        flash('Product ID exists!', 'danger')
        return redirect(url_for('add_product'))
    
    product = Product(
        product_id=product_id,
        name=request.form['name'],
        category=request.form['category']
    )
    db.session.add(product)
    
    # Handle initial location and quantity
    initial_location = request.form.get('initial_location')
    initial_qty = request.form.get('initial_qty', 0)
    
    if initial_location and int(initial_qty) > 0:
        movement_id = f"MOV{ProductMovement.query.count() + 1:04d}"
        movement = ProductMovement(
            movement_id=movement_id,
            product_id=product_id,
            to_location=initial_location,
            qty=int(initial_qty),
            timestamp=get_ist_now()
        )
        db.session.add(movement)
        location_name = Location.query.get(initial_location).name
        flash(f'Product added with {initial_qty} units at {location_name}!', 'success')
    else:
        flash('Product added successfully!', 'success')
    
    db.session.commit()
    return redirect(url_for('products'))

def handle_edit_product(product_id, request):
    product = Product.query.get_or_404(product_id)
    product.name = request.form['name']
    product.category = request.form['category']
    db.session.commit()
    flash('Product updated successfully!', 'success')
    return redirect(url_for('products'))

def handle_delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('products'))


def handle_add_location(request):
    location_id = request.form['location_id']
    if Location.query.get(location_id):
        flash('Location ID exists!', 'danger')
        return redirect(url_for('add_location'))
    
    db.session.add(Location(
        location_id=location_id,
        name=request.form['name']
    ))
    db.session.commit()
    flash('Location added successfully!', 'success')
    return redirect(url_for('locations'))

def handle_edit_location(location_id, request):
    location = Location.query.get_or_404(location_id)
    location.name = request.form['name']
    db.session.commit()
    flash('Location updated successfully!', 'success')
    return redirect(url_for('locations'))

def handle_delete_location(location_id):
    location = Location.query.get_or_404(location_id)
    db.session.delete(location)
    db.session.commit()
    flash('Location deleted successfully!', 'success')
    return redirect(url_for('locations'))


def get_locations_with_product(product_id):
    """Get all locations that have the specified product in stock"""
    balance_data = generate_balance_report()
    locations_with_stock = []
    
    for item in balance_data:
        if item['product_id'] == product_id and item['balance'] > 0:
            locations_with_stock.append({
                'location_id': item['location_id'],
                'location_name': item['location_name'],
                'balance': item['balance']
            })
    
    return locations_with_stock

def handle_add_movement(request):
    movement_id = request.form['movement_id']
    if ProductMovement.query.get(movement_id):
        flash('Movement ID exists!', 'danger')
        return redirect(url_for('add_movement'))
    
    product_id = request.form['product_id']
    from_location = request.form['from_location'] or None
    to_location = request.form['to_location'] or None
    quantity = int(request.form['qty'])
    
    # Validate stock availability while making movements
    if from_location:
        locations_with_stock = get_locations_with_product(product_id)
        source_location = next((loc for loc in locations_with_stock if loc['location_id'] == from_location), None)
        
        if not source_location:
            flash(f'Selected location does not have the product in stock!', 'danger')
            return redirect(url_for('add_movement'))
        
        if quantity > source_location['balance']:
            flash(f'Insufficient stock! Only {source_location["balance"]} units available at {source_location["location_name"]}', 'danger')
            return redirect(url_for('add_movement'))
    
    db.session.add(ProductMovement(
        movement_id=movement_id,
        product_id=product_id,
        from_location=from_location,
        to_location=to_location,
        qty=quantity,
        timestamp=get_ist_now()
    ))
    db.session.commit()
    flash('Movement recorded successfully!', 'success')
    return redirect(url_for('movements'))

def handle_edit_movement(movement_id, request):
    movement = ProductMovement.query.get_or_404(movement_id)
    movement.product_id = request.form['product_id']
    movement.from_location = request.form['from_location'] or None
    movement.to_location = request.form['to_location'] or None
    movement.qty = int(request.form['qty'])
    db.session.commit()
    flash('Movement updated successfully!', 'success')
    return redirect(url_for('movements'))

def handle_delete_movement(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    db.session.delete(movement)
    db.session.commit()
    flash('Movement deleted successfully!', 'success')
    return redirect(url_for('movements'))


def generate_balance_report():
    movements = ProductMovement.query.all()
    balance = {}
    
    for move in movements:
        
        if move.to_location:
            key = (move.product_id, move.to_location)
            if key not in balance:
                balance[key] = 0
            balance[key] += move.qty
        
       
        if move.from_location:
            key = (move.product_id, move.from_location)
            if key not in balance:
                balance[key] = 0
            balance[key] -= move.qty
    
    balance_data = []
    for (product_id, location_id), qty in balance.items():
        # Ensure stock doesn't go below 0
        if qty < 0:
            qty = 0
            
        if location_id and qty > 0:
            product = Product.query.get(product_id)
            location = Location.query.get(location_id)
            if product and location:
                balance_data.append({
                    'product_name': product.name,
                    'location_name': location.name,
                    'product_id': product_id,
                    'location_id': location_id,
                    'balance': qty
                })
    
    return balance_data


def get_dashboard_stats():
    return {
        'products': Product.query.count(),
        'locations': Location.query.count(),
        'movements': ProductMovement.query.count()
    }

def initialize_sample_data():
    
    if not User.query.first():
        admin_user = User(
            username='admin',
            email='admin@inventory.com'
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
    
    if not Product.query.first():
        
        products = [
            Product(product_id='P001', name='Laptop', category='Electronics'),
            Product(product_id='P002', name='Chair', category='Furniture'),
            Product(product_id='P003', name='Notebook', category='Stationery'),
        ]
        
        locations = [
            Location(location_id='L001', name='Warehouse A'),
            Location(location_id='L002', name='Warehouse B'),
            Location(location_id='L003', name='Store'),
        ]
        
        movements = [
            ProductMovement(movement_id='M001', product_id='P001', to_location='L001', qty=50, timestamp=get_ist_now()),
            ProductMovement(movement_id='M002', product_id='P002', to_location='L001', qty=30, timestamp=get_ist_now()),
            ProductMovement(movement_id='M003', product_id='P001', from_location='L001', to_location='L003', qty=10, timestamp=get_ist_now()),
        ]
        
        db.session.add_all(products + locations + movements)
        db.session.commit()
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, MenuItemForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, MenuItem
from werkzeug.urls import url_parse
from datetime import datetime
import json

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',title='Home')

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title = 'Sign In', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratualtions, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)

@app.route('/menu')
def menu():
    return render_template('menu.html')

# Route for the admin interface to edit the menu
@app.route('/admin/menu', methods=['GET', 'POST'])
def admin_menu():
    form = MenuItemForm()

    if form.validate_on_submit():
        # Update the menu item in the database
        menu_item = MenuItem.query.filter_by(name=form.name.data).first()
        if menu_item:
            menu_item.price = form.price.data
        else:
            menu_item = MenuItem(name=form.name.data, price=form.price.data)
            db.session.add(menu_item)
        
        db.session.commit()

        # Read the JSON file
        with open('menu.json', 'r') as json_file:
            menu_data = json.load(json_file)

        # Update the drink names and prices based on the form submission
        for item in menu_data:
            item_name = item['name']
            item_price = request.form.get(item_name)
            if item_price is not None:
                item['price'] = float(item_price)

        # Write the updated JSON file
        with open('menu.json', 'w') as json_file:
            json.dump(menu_data, json_file, indent=4)

        # Update the corresponding records in the database
        for item in menu_data:
            menu_item = MenuItem.query.filter_by(name=item['name']).first()
            if menu_item:
                menu_item.price = item['price']
            else:
                menu_item = MenuItem(name=item['name'], price=item['price'])
                db.session.add(menu_item)
        
        db.session.commit()

        return redirect(url_for('admin_menu'))

    # Retrieve the menu items from the database
    menu_items = MenuItem.query.all()

    return render_template('admin_menu.html', form=form, menu_items=menu_items)

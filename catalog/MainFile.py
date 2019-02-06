#!/user/bin/env python3

from flask import Flask, render_template, redirect
from flask import Flask, url_for, request, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Dbcreation import Base, Category, MenuItem, User
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import random
import string
from flask import make_response
import requests


app = Flask(__name__)


CLIENT_ID = json.loads(open('client_secrets.json', 'r').
                       read())['web']['client_id']

engine = create_engine('sqlite:///products.db',
                       connect_args={'check_same_thread': False},
                       echo=True)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/products/JSON')
def productsJSON():
    products = session.query(Category).all()
    return jsonify(Products=[i.serialize for i in products])


# Making an API endpoint (GET Request)
@app.route('/products/<int:product_id>/menu/JSON')
def productMenuJSON(product_id):
    product = session.query(Category).filter_by(id=product_id).one()
    items = session.query(MenuItem).filter_by(product_id=product_id).all()
    return jsonify(Product=product.serialize,
                   MenuItems=[i.serialize for i in items])


# Add your API endpoint here
@app.route('/products/<int:product_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(product_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menuItem.serialize)


# Create a state token to prevent request forgery.
# Store it in a session for later validation.
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # Render the login template
    return render_template("login.html", STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps("Current user is"
                                 "already connected."),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if user exsists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px;'
    output += 'height: 300px;'
    output += 'border-radius: 150px;'
    output += '-webkit-border-radius: 150px;'
    output += '-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session


# logout from session
@app.route('/gdisconnect')
def gdisconnect():

    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token='
    url += login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('showProducts'))
    else:
        response = make_response(json.dumps("Failed to revoke token for "
                                 "given user.", 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# show all Types of products
@app.route('/')
@app.route('/products/')
def showProducts():
    products = session.query(Category).all()
    if 'username' in login_session:
        return render_template('products.html', products=products)
    else:
        return render_template('publicproducts.html', products=products)


# adding new type of product
@app.route('/product/new/', methods=['GET', 'POST'])
def newProduct():
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        if request.form['name']:
            product = Category(name=request.form['name'],
                               user_id=login_session['user_id'])
            session.add(product)
            session.commit()
            return redirect(url_for('showProducts'))
    else:
        return render_template('newproduct.html')


# edit existing product
@app.route('/product/<int:product_id>/edit/', methods=['GET', 'POST'])
def editProduct(product_id):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    product = session.query(Category).filter_by(id=product_id).one()
    if product.user_id != login_session['user_id']:
        return redirect('/')
    if request.method == 'POST':
        if request.form['name']:
            product.name = request.form['name']
        session.add(product)
        session.commit()
        return redirect(url_for('showProducts'))
    else:
        return render_template('editproduct.html', product=product)


# delete existing product
@app.route('/product/<int:product_id>/delete/', methods=['GET', 'POST'])
def deleteProduct(product_id):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    product = session.query(Category).filter_by(id=product_id).one()
    items = session.query(MenuItem).filter_by(product_id=product_id).all()
    if product.user_id != login_session['user_id']:
        return redirect('/')
    if request.method == 'POST':
        for item in items:
            session.delete(item)
        session.delete(product)
        session.commit()
        return redirect(url_for('showProducts'))
    else:
        return render_template('deleteproduct.html', product=product)


# show all items in products
@app.route('/product/<int:product_id>/')
@app.route('/product/<int:product_id>/menu/')
def showMenu(product_id):
    product = session.query(Category).filter_by(id=product_id).one()
    items = session.query(MenuItem).filter_by(product_id=product_id).all()
    creator = getUserInfo(product.user_id)
    u = 'username'
    l_s = login_session
    c_id = creator.id
    if u not in l_s or c_id != login_session['user_id']:
        return render_template('publicmenu.html', product=product,
                               items=items)
    else:
        return render_template('menu.html', product=product, items=items)


# create new menu item in existing products
@app.route('/product/<int:product_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(product_id):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    product = session.query(Category).filter_by(id=product_id).one()
    if login_session['user_id'] != product.user_id:
        return redirect('/')
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        item = MenuItem(name=name, description=description, price=price,
                        product_id=product_id, product=product,
                        user_id=product.user_id)
        session.add(item)
        session.commit()
        return redirect(url_for('showMenu', product_id=product_id))
    else:
        return render_template('newMenuItem.html', product_id=product_id)


# Edit existing menu item
@app.route('/product/<int:product_id>/<int:menu_id>/edit/',
           methods=['GET', 'POST'])
def editMenuItem(product_id, menu_id):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    product = session.query(Category).filter_by(id=product_id).one()
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    if login_session['user_id'] != product.user_id:
        alert = "<script>function myFunction() {alert('You are not authorized"
        alert += "to edit menuitems to this product. Please create your own"
        alert += "product in order to edit items.');}</script>"
        alert += "<body onload='myFunction()''>"
        return alert
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        item.price = request.form['price']
        item.course = request.form['course']
        session.add(item)
        session.commit()
        return redirect(url_for('showMenu', product_id=product_id))
    else:
        return render_template('editMenuItem.html',
                               product=product,
                               item=item, menu_id=menu_id)


# Delete items
@app.route('/product/<int:product_id>/<int:menu_id>/delete/', methods=[
           'GET', 'POST'])
def deleteMenuItem(product_id, menu_id):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    product = session.query(Category).filter_by(id=product_id).one()
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    if login_session['user_id'] != product.user_id:
        alert = "<script>function myFunction() {alert('You are not authorized"
        alert += "to delete menu items to this restaurant. Please create your"
        alert += "own restaurant in order to delete items.');}"
        alert += "</script><body onload='myFunction()''>"
        return alert
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('showMenu', product_id=product_id))
    else:
        return render_template('deleteMenuItem.html',
                               product=product, menu_id=menu_id, item=item)

# starting
if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=9000)

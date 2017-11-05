from flask import Flask, render_template, request, flash, url_for, redirect, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurant')
def restaurantList():
    restaurants = session.query(Restaurant)
    return render_template('listrestaurant.html',restaurants=restaurants)

@app.route('/restaurant/new',methods=['GET','POST'])
def newRestaurant():
    if (request.method == 'POST'):
        newRestaurant = Restaurant(name = request.form['name'])
        session.add(newRestaurant)
        session.commit()
        flash("Successfully added new restaurant")
        return redirect(url_for('restaurantList'))
    else:
        return render_template('newrestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET','POST'])
def editRestaurant(restaurant_id):
    editedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if (request.method == 'POST'):
        editedRestaurant.name = request.form['name']
        session.add(editedRestaurant)
        session.commit()
        return redirect(url_for('restaurantList'))
    return render_template('editrestaurant.html',editedRestaurant = editedRestaurant)

@app.route('/restaurant/<int:restaurant_id>/delete',methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id =restaurant_id).one()
    if (request.method == 'POST'):
        session.delete(restaurant)
        session.commit()
        return redirect(url_for('restaurantList'))
    else:
        return render_template('deleterestaurant.html',restaurant = restaurant)

@app.route('/restaurant/JSON')
def restaurantJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[i.serialize for i in restaurants])



@app.route('/restaurant/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template('menu.html',restaurant = restaurant, items = items)

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return jsonify(Restaurant=[i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuItemJSON(restaurant_id,menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(id = menu_id)
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/new',methods = ['GET','POST'])
def newMenuItem(restaurant_id):
    if (request.method=='POST'):
        addedMenu = MenuItem(name = request.form['name'],description = request.form['description'], price = request.form['price'], course = request.form['course'],restaurant_id = restaurant_id)
        session.add(addedMenu)
        session.commit()
        return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))
    else:
        return render_template('newmenuitem.html',restaurant_id = restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods = ['GET','POST'])
def editMenuItem(restaurant_id,menu_id):
    editedMenu = session.query(MenuItem).filter_by(id = menu_id).one()
    if (request.method=='POST'):
        editedMenu.name = request.form['name']
        session.add(editedMenu)
        session.commit()
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))

    return render_template('editmenuitem.html',item = editedMenu, restaurant_id = restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods = ['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deletedMenu = session.query(MenuItem).filter_by(id = menu_id).one()
    if (request.method=='POST'):
        session.delete(deletedMenu)
        session.commit()
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    return render_template('deletemenuitem.html',menu_id = menu_id,restaurant_id=restaurant_id, item = deletedMenu)





if (__name__) == '__main__':
    app.secret_key = 'axderguy'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
    main()

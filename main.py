import json

from flask import Flask, render_template, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from utils import read_json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db: SQLAlchemy = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text(200))
    last_name = db.Column(db.Text(200))
    age = db.Column(db.Integer)
    email = db.Column(db.Text(30))
    role = db.Column(db.Text(50))
    phone = db.Column(db.Text(11))


class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order = db.relationship("Order", foreign_keys=[order_id])
    executor = db.relationship("User", foreign_keys=[executor_id])


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    description = db.Column(db.Text())
    start_date = db.Column(db.Text)
    end_date = db.Column(db.Text)
    address = db.Column(db.Text())
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    customer = db.relationship("Order", foreign_keys=[customer_id])
    executor = db.relationship("User", foreign_keys=[executor_id])


db.create_all()

for i in read_json('users.json'):
    user = User(id=i['id'],
                first_name=i['first_name'],
                last_name=i['last_name'],
                age=i['age'],
                email=i['email'],
                role=i['role'],
                phone=i['phone'])
    db.session.add(user)
    db.session.commit()

for i in read_json('orders.json'):
    order = Order(id=i['id'],
                  name=i['name'],
                  description=i['description'],
                  start_date=i['start_date'],
                  end_date=i['end_date'],
                  address=i['address'],
                  price=i['price'],
                  customer_id=i['customer_id'],
                  executor_id=i['executor_id'])

    db.session.add(order)
    db.session.commit()

for i in read_json('offers.json'):
    offer = Offer(id=i['id'],
                  order_id=i['order_id'],
                  executor_id=i['executor_id'])

    db.session.add(offer)
    db.session.commit()


@app.route('/users/', methods=['POST', 'GET'])
def users_all():
    users = User.query.all()
    if request.method == "GET":
        users_list = []
        for user in users:
            name = {"id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "age": user.age,
                    "email": user.email,
                    "role": user.role,
                    "phone": user.phone}
            users_list.append(name)

        return jsonify(users_list), 200, {'Content-Type': 'application/json; charset=utf-8'}

    elif request.method == "POST":
        user_data = request.args

        new_user = User(
            id=user_data['id'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            age=user_data['age'],
            email=user_data['email'],
            role=user_data['role'],
            phone=user_data['phone']
        )
        db.session.add(new_user)
        db.session.commit()
        return '', 201


@app.route('/users/<int:id>', methods=["GET", "PUT", "DELETE"])
def user(id):
    if request.method == "GET":
        users = User.query.get(id)
        name = {"id": users.id,
                "first_name": users.first_name,
                "last_name": users.last_name,
                "age": users.age,
                "email": users.email,
                "role": users.role,
                "phone": users.phone}

        return json.dumps(name)

    elif request.method == "DELETE":
        users = User.query.get(id)
        db.session.delete(users)
        db.session.commit()
        return "Удалено", 204

    elif request.method == "PUT":
        user_data = request.args
        u = User.query.get(id)
        u.first_name = user_data['first_name']
        u.last_name = user_data['last_name']
        u.age = user_data['age']
        u.email = user_data['email']
        u.role = user_data['role']
        u.phone = user_data['phone']

        db.session.add(u)
        db.session.commit()
        return "Обновили", 204


@app.route('/offers/', methods=['POST', 'GET'])
def offers_all():
    if request.method == "GET":
        offers = Offer.query.all()
        offers_list = []
        for offer in offers:
            name = {"id": offer.id,
                    "order_id": offer.order_id,
                    "executor_id": offer.executor_id
                    }
            offers_list.append(name)

        return jsonify(offers_list), 200, {'Content-Type': 'application/json; charset=utf-8'}

    elif request.method == "POST":
        user_data = request.args
        new_offer = Offer(
            id=user_data['id'],
            order_id=user_data['order_id'],
            executor_id=user_data['executor_id']
        )
        db.session.add(new_offer)
        db.session.commit()
        return '', 201


@app.route('/offers/<int:id>', methods=["GET", "PUT", "DELETE"])
def offer(id):
    offers = Offer.query.get(id)
    if request.method == "GET":
        name = {"id": offers.id,
                "order_id": offers.order_id,
                "executor_id": offers.executor_id
                }

        return json.dumps(name)

    elif request.method == "DELETE":
        db.session.delete(offers)
        db.session.commit()
        return "Удалено", 204

    elif request.method == "PUT":
        user_data = request.args
        off = Offer.query.get(id)
        off.executor_id = user_data['executor_id']
        db.session.add(off)
        db.session.commit()
        return "Обновили", 204


@app.route('/orders/', methods=['POST', 'GET'])
def orders_all():
    orders = Order.query.all()
    if request.method == "GET":
        orders_list = []
        for order in orders:
            name = {"id": order.id,
                    "name": order.name,
                    "description": order.description,
                    "start_date": order.start_date,
                    "end_date": order.end_date,
                    "address": order.address,
                    "price": order.price,
                    "customer_id": order.customer_id,
                    "executor_id": order.executor_id}
            orders_list.append(name)

        return jsonify(orders_list), 200, {'Content-Type': 'application/json; charset=utf-8'}

    elif request.method == "POST":
        user_data = request.args

        new_order = Order(
            id=user_data['id'],
            name=user_data['name'],
            description=user_data['description'],
            start_date=user_data['start_date'],
            end_date=user_data['end_date'],
            address=user_data['address'],
            price=user_data['price'],
            customer_id=user_data['customer_id'],
            executor_id=user_data['executor_id']
        )
        db.session.add(new_order)
        db.session.commit()
        return '', 201


@app.route('/orders/<int:id>', methods=["GET", "PUT", "DELETE"])
def order(id):
    if request.method == "GET":
        orders = Order.query.get(id)
        name = {"id": order.id,
                "name": order.name,
                "description": order.description,
                "start_date": order.start_date,
                "end_date": order.end_date,
                "address": order.address,
                "price": order.price,
                "customer_id": order.customer_id,
                "executor_id": order.executor_id}

        return json.dumps(name)

    elif request.method == "DELETE":
        orders = Order.query.get(id)
        db.session.delete(orders)
        db.session.commit()
        return "Удалено", 204

    elif request.method == "PUT":
        user_data = request.args
        u = Order.query.get(id)
        u.name = user_data['name']
        u.description = user_data['description']
        u.start_date = user_data['start_date']
        u.end_date = user_data['end_date']
        u.address = user_data['address']
        u.price = user_data['price']
        u.customer_id = user_data['customer_id']
        u.executor_id = user_data['executor_id']

        db.session.add(u)
        db.session.commit()
        return "Обновили", 204


app.run(debug=True)

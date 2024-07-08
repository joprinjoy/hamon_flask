import flask
from flask import render_template,request,redirect,url_for,session,flash,make_response,jsonify
from sqlalchemy import select
from flask_sqlalchemy import SQLAlchemy
from models import *
from flask_cors import CORS,cross_origin

app = flask.Flask(__name__)

CORS(app)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:5432/flask_db"

# initialize the app with the extension
db.init_app(app)

@app.route('/')
def index():
   return render_template("index.html")

@app.route('/products')
def list_products():
    select_query = db.select(Image).order_by(Image.id.desc())

    query =db.select(Product.id,Product.name,Product.price, Image.image_url).join_from(
    Product, Image)
    query_result = db.session.execute(query).fetchall()
    
    
    result = db.session.execute(select_query).scalars()
    ret = []
    for product in result:
        details = {
        "id": product.product.id,
        "name" : product.product.name,
        "price" : product.product.price,
        "image_ur": product.image_url
        }
        ret.append(details)
    return jsonify(ret)

@app.route('/category',methods = ['POST'])
def add_category():
   
   data = request.get_json()
   name =  data.get('name')
   new_category = Category(name = name)
   db.session.add(new_category)
   db.session.commit()
   return jsonify({'message':"category added succesfully"})

@app.route('/product',methods=['POST'])
@cross_origin() 
def add_product():
        
        data = request.get_json()
        
        print(data)
        name =  data.get('name')
        price = data.get('price')
        category_name= data.get('category')
        image_url = data.get("image_url")
        # checking all required fields are available
        if not all([name,price,category_name,image_url]):
            return jsonify({"error": "Fill all the fields"}), 400

        try:
            price = float(price)
        except:
            return jsonify({"error": "Price should be integer"}), 400

        category = db.session.query(Category).filter_by(name=category_name).first()        
        
       
        if category == None:
            category = Category(name = category_name)
            db.session.add(category)
            db.session.commit()
            #commit will refresh the database query instance and we get current data
            # category = db.session.query(Category).filter_by(name=category_name).first()
        new_product = Product(name = name, price = price,category_id = category.id)
        
        db.session.add(new_product)
        try:
            db.session.commit()
        except:
            return jsonify({"error": "Data already exist,use different Name or Image URL "}), 400
        new_image = Image(image_url = image_url,product_id = new_product.id)
        db.session.add(new_image)
        db.session.commit()
        return jsonify({'message':"Product added succesfully"})

@app.route('/deleteproduct',methods =['POST'])
@cross_origin() 
def delete_product(): 
    data = request.get_json()

    print(data)
    productId =data['id']
    product =db.session.query(Product).filter_by(id=productId).first()
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message':"Product deleted succesfully"})
   
    

    
   



with app.app_context():
    db.create_all()

if __name__ == "__main__":
  init_db()
  app.run(debug=True,port=5005)
  

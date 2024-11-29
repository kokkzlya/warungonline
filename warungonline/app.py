import inject
import shortuuid
import sqlite3
from flask import Blueprint, Flask, redirect, render_template, request, url_for

from warungonline import db, di
from warungonline.entities import Product, User

bp = Blueprint("app", __name__)

@bp.route("/", methods=["GET"])
@inject.autoparams("conn")
def landing_page(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("SELECT id, name, description, price, stock FROM products LIMIT 9")
    result = cur.fetchall()
    products = []
    for row in result:
        products.append(Product(
            id=row[0],
            name=row[1],
            description=row[2],
            price=row[3],
            stock=row[4],
        ))
    return render_template("index.html", products=products)

@bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@bp.route("/login", methods=["POST"])
@inject.autoparams("conn")
def login(conn: sqlite3.Connection):
    cur = conn.cursor()
    username = request.form.get("username")
    password = request.form.get("password")
    print(username, password)
    q = "SELECT id, name FROM users WHERE username = '" + username + "' AND password = '" + password + "' LIMIT 1"
    cur.execute(q)
    result = cur.fetchone()
    if not result:
        return render_template("login.html", error="Invalid username or password")
    user = User(
        id=result[0],
        username=username,
        name=result[1],
    )
    return redirect(url_for("app.landing_page"))

@bp.route("/products", methods=["GET"])
@inject.autoparams("conn")
def products_page(conn: sqlite3.Connection):
    category = request.args.get("category", None)
    cur = conn.cursor()
    q = "SELECT id, name, description, category, price, stock FROM products"
    if category:
        q += " WHERE category = '" + category + "'"
    cur.execute(q)
    result = cur.fetchall()
    products = []
    for row in result:
        products.append(Product(
            id=row[0],
            name=row[1],
            description=row[2],
            price=row[4],
            stock=row[5],
        ))  
    return render_template("products.html", products=products)

@bp.route("/products/new", methods=["GET"])
def new_product_page():
    return render_template("new_product.html")

@bp.route("/products/new", methods=["POST"])
@inject.autoparams("conn")
def create_product(conn: sqlite3.Connection):
    name = request.form.get("name")
    description = request.form.get("description")
    category = request.form.get("category", "lainnya")
    price = request.form.get("price")
    stock = request.form.get("stock")
    errors = {}
    if not name or len(name) < 3:
        errors["name"] = "Name must be at least 3 characters"
    if not price or not price.isdigit():
        errors["price"] = "Price must be a number"
    if not stock or not stock.isdigit():
        errors["stock"] = "Stock must be a number"
    if errors:
        return render_template(
            "new_product.html",
            errors=errors,
            name=name,
            description=description,
            price=price,
            stock=stock,
        )
    id = shortuuid.uuid()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO products (id, name, description, category, price, stock) VALUES (?, ?, ?, ?, ?, ?)",
        (id, name, description, category, price, stock)
    )
    return redirect(url_for("app.landing_page"))

@bp.route("/products/<product_id>", methods=["GET"])
@inject.autoparams("conn")
def product_page(product_id: str, conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("SELECT id, name, description, price, stock FROM products WHERE id = ? LIMIT 1", (product_id,))
    result = cur.fetchone()
    if not result:
        return render_template("404.html"), 404
    product = Product(
        id=result[0],
        name=result[1],
        description=result[2],
        price=result[3],
        stock=result[4],
    )
    return render_template("product_detail.html", product=product)

@bp.route("/register", methods=["POST"])
@inject.autoparams("conn")
def register(conn: sqlite3.Connection):
    cur = conn.cursor()
    name = request.form.get("name")
    username = request.form.get("username")
    password = request.form.get("password")
    retyped_pass = request.form.get("retyped_password")
    errors = {}
    if password != retyped_pass:
        errors["retyped_password"] = "Passwords do not match"
    if not password or len(password) < 3:
        errors["password"] = "Password must be at least 3 characters"
    if not name or len(name) < 3:
        errors["name"] = "Name must be at least 3 characters"
    if not username or len(username) < 3:
        errors["username"] = "Username must be at least 3 characters"
    cur.execute("SELECT id FROM users WHERE username = ? LIMIT 1", (username,))
    result = cur.fetchone()
    if result:
        errors["username"] = "Username already exists"
    if errors:
        return render_template(
            "register.html",
            errors=errors,
            name=name,
            username=username,
        )
    id = shortuuid.uuid()
    role = "user"
    cur.execute(
        "INSERT INTO users (id, username, password, name, role) VALUES (?, ?, ?, ?, ?)",
        (id, username, password, name, role)
    )
    return redirect(url_for("app.landing_page"))

@bp.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")

@bp.route("/users", methods=["GET"])
@inject.autoparams("conn")
def users_page(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("SELECT id, username, name, role FROM users")
    result = cur.fetchall()
    users = []
    for row in result:
        users.append(User(
            id=row[0],
            username=row[1],
            name=row[2],
            role=row[3],
        ))
    return render_template("users.html", users=users)

def create_app():
    app = Flask(
        __name__,
        static_folder="../public",
        static_url_path="/public",
    )
    app.register_blueprint(bp)
    db.init_app(app)
    di.init_app(app)
    return app

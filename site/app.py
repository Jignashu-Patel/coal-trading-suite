"""
app.py – main Flask entry-point
uses SQLAlchemy models from models.py
"""

from datetime import datetime
from collections import Counter

from flask import Flask, render_template, request
from models import SessionLocal, Product, QuoteRequest

# -------------------------------------------------
app = Flask(__name__)
app.secret_key = "dev"          # (needed only if you later use flash messages)

# helper – grab product list from the DB
def get_products():
    with SessionLocal() as db:
        return db.query(Product).all()

# ---------- routes --------------------------------

@app.route("/")
def home():
    return render_template("index.html", year=datetime.now().year)


@app.route("/products")
def products():
    return render_template(
        "products.html",
        products=get_products(),
        year=datetime.now().year,
    )


@app.route("/quote", methods=["GET", "POST"])
def quote():
    if request.method == "POST":
        with SessionLocal() as db:
            prod = db.query(Product).filter_by(
                       name=request.form["product"]).first()

            qr = QuoteRequest(
                name   = request.form["name"],
                email  = request.form["email"],
                tonnes = request.form["tonnes"],
                product= prod
            )
            db.add(qr)
            db.commit()

        return "<h2 style='font-family:sans-serif'>Thanks – we'll reply soon!</h2>"

    # GET → show the form
    return render_template(
        "quote.html",
        products=get_products(),
        preselect=request.args.get("product", ""),
        year=datetime.now().year,
    )


@app.route("/dashboard")
def dashboard():
    # keep the DB session open while we access q.product
    with SessionLocal() as db:
        quotes = db.query(QuoteRequest).all()

        # --- requests per product ---
        prod_counter = Counter(q.product.name for q in quotes)

        # --- requests per month (YYYY-MM) ---
        month_counter = Counter(q.created.strftime("%Y-%m") for q in quotes)

    # convert counters to lists after leaving the session
    labels_product = list(prod_counter.keys())
    data_product   = list(prod_counter.values())

    labels_month = sorted(month_counter.keys())
    data_month   = [month_counter[m] for m in labels_month]

    return render_template(
        "dashboard.html",
        labels_product=labels_product,
        data_product=data_product,
        labels_month=labels_month,
        data_month=data_month,
        year=datetime.now().year,
    )

# -------------------------------------------------
if __name__ == "__main__":
    # change the port if 5003 is busy, e.g. port=5004
    app.run(debug=True, port=5003)

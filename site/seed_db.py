"""
seed_db.py – populate the products table with demo rows
run: python site/seed_db.py
"""
from models import SessionLocal, Product

demo = [
    ("Premium Lump Coal",  "A", 7200, 320),
    ("Restaurant Grade",   "B", 6800, 290),
    ("Industrial Mix",     "C", 6400, 250),
    ("Smokeless Briquettes","A+",7300, 350),
    ("Anthracite Nuts",    "A", 7250, 330),
    ("Steam Coal 4800",    "D", 4800, 190),
    ("Steam Coal 5500",    "C", 5500, 220),
    ("Low-Ash Coal",       "B+",7000, 310),
    ("Pea Coal",           "B", 6900, 260),
    ("Metallurgical Coke", "A", 7500, 400),
    ("Charcoal (BBQ)",     "-", 6400, 180),
    ("Screenings / Fines", "E", 4200, 120),
]

with SessionLocal() as db:
    if db.query(Product).count() == 0:
        for n, g, k, p in demo:
            db.add(Product(name=n, grade=g, kcal=k, price=p))
        db.commit()
        print("✓ products table seeded")
    else:
        print("products table already populated")

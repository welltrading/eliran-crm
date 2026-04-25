import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
from dotenv import load_dotenv

# Load secrets
load_dotenv("/a0/usr/projects/eliran/.a0proj/secrets.env")
load_dotenv("/a0/usr/projects/eliran/.a0proj/variables.env")

# Fix API key env name
if os.environ.get("AIRTABLE_API") and not os.environ.get("AIRTABLE_API_KEY"):
    os.environ["AIRTABLE_API_KEY"] = os.environ["AIRTABLE_API"]

from airtable_client import get_client

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "crm-eliran-secret-2025")


def db():
    return get_client()


# ─────────────────────────────────────────────
# Dashboard
# ─────────────────────────────────────────────
@app.route("/")
def dashboard():
    client = db()
    customers = client.get_customers()
    orders = client.get_orders()
    tasks = client.get_tasks()
    inventory = client.get_inventory()

    stats = {
        "customers": len(customers),
        "orders": len(orders),
        "open_tasks": sum(1 for t in tasks if t.get("סטטוס") not in ["הושלם", "אושר", "בוטל"]),
        "inventory_items": len(inventory),
    }

    recent_orders = sorted(orders, key=lambda x: x.get("תאריך יצירה", ""), reverse=True)[:5]
    urgent_tasks = [t for t in tasks if t.get("סטטוס") not in ["הושלם", "אושר", "בוטל"]][:5]

    return render_template("dashboard.html",
                           stats=stats,
                           recent_orders=recent_orders,
                           urgent_tasks=urgent_tasks)


# ─────────────────────────────────────────────
# לקוחות
# ─────────────────────────────────────────────
@app.route("/customers")
def customers_list():
    search = request.args.get("q", "")
    clients = db().get_customers(search if search else None)
    return render_template("customers/list.html", customers=clients, search=search)


@app.route("/customers/new", methods=["GET", "POST"])
def customer_new():
    if request.method == "POST":
        fields = {
            "שם": request.form.get("name", ""),
            "טלפון": request.form.get("phone", ""),
            "אימייל": request.form.get("email", ""),
            "כתובת": request.form.get("address", ""),
            "הערות": request.form.get("notes", ""),
        }
        fields = {k: v for k, v in fields.items() if v}
        result = db().create("customers", fields)
        if result:
            flash("לקוח נוסף בהצלחה!", "success")
            return redirect(url_for("customer_detail", record_id=result["id"]))
        else:
            flash("שגיאה ביצירת לקוח", "danger")
    return render_template("customers/new.html")


@app.route("/customers/<record_id>")
def customer_detail(record_id):
    customer = db().get_one("customers", record_id)
    if not customer:
        flash("לקוח לא נמצא", "danger")
        return redirect(url_for("customers_list"))
    orders = db().get_orders(customer_id=record_id)
    return render_template("customers/detail.html", customer=customer, orders=orders)


@app.route("/customers/<record_id>/edit", methods=["GET", "POST"])
def customer_edit(record_id):
    customer = db().get_one("customers", record_id)
    if not customer:
        flash("לקוח לא נמצא", "danger")
        return redirect(url_for("customers_list"))
    if request.method == "POST":
        fields = {
            "שם": request.form.get("name", ""),
            "טלפון": request.form.get("phone", ""),
            "אימייל": request.form.get("email", ""),
            "כתובת": request.form.get("address", ""),
            "הערות": request.form.get("notes", ""),
        }
        fields = {k: v for k, v in fields.items() if v}
        result = db().update("customers", record_id, fields)
        if result:
            flash("לקוח עודכן בהצלחה!", "success")
            return redirect(url_for("customer_detail", record_id=record_id))
        else:
            flash("שגיאה בעדכון לקוח", "danger")
    return render_template("customers/edit.html", customer=customer)


# ─────────────────────────────────────────────
# הזמנות
# ─────────────────────────────────────────────
@app.route("/orders")
def orders_list():
    status = request.args.get("status", "")
    orders = db().get_orders(status=status if status else None)
    return render_template("orders/list.html", orders=orders, status_filter=status)


@app.route("/orders/new", methods=["GET", "POST"])
def order_new():
    customers = db().get_customers()
    if request.method == "POST":
        customer_id = request.form.get("customer_id")
        fields = {
            "תיאור": request.form.get("description", ""),
            "סטטוס": request.form.get("status", "טיוטה"),
            "הערות": request.form.get("notes", ""),
        }
        if customer_id:
            fields["לקוח"] = [customer_id]
        fields = {k: v for k, v in fields.items() if v}
        result = db().create("orders", fields)
        if result:
            flash("הזמנה נוצרה בהצלחה!", "success")
            return redirect(url_for("order_detail", record_id=result["id"]))
        else:
            flash("שגיאה ביצירת הזמנה", "danger")
    return render_template("orders/new.html", customers=customers)


@app.route("/orders/<record_id>")
def order_detail(record_id):
    order = db().get_one("orders", record_id)
    if not order:
        flash("הזמנה לא נמצאה", "danger")
        return redirect(url_for("orders_list"))
    lines = db().get_order_lines(record_id)
    return render_template("orders/detail.html", order=order, lines=lines)


@app.route("/orders/<record_id>/status", methods=["POST"])
def order_update_status(record_id):
    new_status = request.form.get("status")
    if new_status:
        db().update("orders", record_id, {"סטטוס": new_status})
        flash(f"סטטוס עודכן ל: {new_status}", "success")
    return redirect(url_for("order_detail", record_id=record_id))


@app.route("/orders/<record_id>/pdf")
def order_pdf(record_id):
    order = db().get_one("orders", record_id)
    if not order:
        flash("הזמנה לא נמצאה", "danger")
        return redirect(url_for("orders_list"))
    lines = db().get_order_lines(record_id)
    html = render_template("pdf/order_pdf.html", order=order, lines=lines)
    from weasyprint import HTML
    pdf_bytes = HTML(string=html, base_url=request.host_url).write_pdf()
    response = make_response(pdf_bytes)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"inline; filename=order_{record_id[:8]}.pdf"
    return response


# ─────────────────────────────────────────────
# הצעות מחיר
# ─────────────────────────────────────────────
@app.route("/quotes")
def quotes_list():
    status = request.args.get("status", "")
    quotes = db().get_quotes(status=status if status else None)
    return render_template("quotes/list.html", quotes=quotes, status_filter=status)


@app.route("/quotes/new", methods=["GET", "POST"])
def quote_new():
    client = db()
    products = client.get_products()
    if request.method == "POST":
        product_id = request.form.get("product_id")
        fields = {
            "שם לקוח": request.form.get("customer_name", ""),
            "טלפון": request.form.get("phone", ""),
            "כתובת": request.form.get("address", ""),
            "כמות": int(request.form.get("quantity", 1)),
            "מחיר בשקלים": float(request.form.get("price", 0)) if request.form.get("price") else None,
            "הערות": request.form.get("notes", ""),
            "סטטוס": request.form.get("status", "טיוטה"),
            "סטנדרטי/ייצור אישי": request.form.get("type", "סטנדרטי"),
        }
        if product_id:
            fields["מוצרים"] = [product_id]
        fields = {k: v for k, v in fields.items() if v not in ["", None, 0.0]}
        result = client.create("quotes", fields)
        if result:
            flash("הצעת מחיר נוצרה בהצלחה!", "success")
            return redirect(url_for("quote_detail", record_id=result["id"]))
        else:
            flash("שגיאה ביצירת הצעת מחיר", "danger")
    return render_template("quotes/new.html", products=products)


@app.route("/quotes/<record_id>")
def quote_detail(record_id):
    quote = db().get_one("quotes", record_id)
    if not quote:
        flash("הצעה לא נמצאה", "danger")
        return redirect(url_for("quotes_list"))
    return render_template("quotes/detail.html", quote=quote)


@app.route("/quotes/<record_id>/pdf")
def quote_pdf(record_id):
    quote = db().get_one("quotes", record_id)
    if not quote:
        flash("הצעה לא נמצאה", "danger")
        return redirect(url_for("quotes_list"))
    html = render_template("pdf/quote_pdf.html", quote=quote)
    from weasyprint import HTML
    pdf_bytes = HTML(string=html, base_url=request.host_url).write_pdf()
    response = make_response(pdf_bytes)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"inline; filename=quote_{record_id[:8]}.pdf"
    return response


# ─────────────────────────────────────────────
# מוצרים
# ─────────────────────────────────────────────
@app.route("/products")
def products_list():
    search = request.args.get("q", "")
    products = db().get_products()
    if search:
        products = [p for p in products if search.lower() in p.get("שם מוצר מלא", "").lower()]
    return render_template("products/list.html", products=products, search=search)


@app.route("/products/new", methods=["GET", "POST"])
def product_new():
    if request.method == "POST":
        model_base = request.form.get("model_base", "").strip()
        if not model_base:
            flash("דגם בסיס הוא שדה חובה", "danger")
            return render_template("products/new.html")
        fields = {
            "דגם בסיס": model_base,
        }
        if request.form.get("size"):
            fields["מידה"] = request.form.get("size").strip()
        if request.form.get("height"):
            fields["גובה"] = request.form.get("height").strip()
        if request.form.get("glass_type"):
            fields["סוג זכוכית"] = request.form.get("glass_type").strip()
        if request.form.get("hardware_color"):
            fields["גוון פרזול"] = request.form.get("hardware_color").strip()
        if request.form.get("model_name"):
            fields["דגם"] = request.form.get("model_name").strip()
        if request.form.get("description"):
            fields["תיאור המוצר"] = request.form.get("description").strip()
        result = db().create_product(fields)
        if result:
            flash("מוצר נוסף בהצלחה!", "success")
            return redirect(url_for("products_list"))
        else:
            flash("שגיאה בהוספת מוצר", "danger")
    return render_template("products/new.html")


# ─────────────────────────────────────────────
# מלאי
# ─────────────────────────────────────────────
@app.route("/inventory")
def inventory_list():
    inventory = db().get_inventory()
    return render_template("inventory/list.html", inventory=inventory)


# ─────────────────────────────────────────────
# מתקינים
# ─────────────────────────────────────────────
@app.route("/installers")
def installers_list():
    installers = db().get_installers()
    return render_template("installers/list.html", installers=installers)


@app.route("/installers/<record_id>")
def installer_detail(record_id):
    installer = db().get_one("installers", record_id)
    if not installer:
        flash("מתקין לא נמצא", "danger")
        return redirect(url_for("installers_list"))
    tasks = db().get_all("tasks", formula=f"FIND('{record_id}', ARRAYJOIN({{מתקין}}))")
    return render_template("installers/detail.html", installer=installer, tasks=tasks)


# ─────────────────────────────────────────────
# משימות
# ─────────────────────────────────────────────
@app.route("/tasks")
def tasks_list():
    status = request.args.get("status", "")
    tasks = db().get_tasks(status=status if status else None)
    installers = db().get_installers()
    installers_map = {inst["id"]: inst.get("Name", inst.get("שם פרטי", "—")).strip() for inst in installers}
    return render_template("tasks/list.html", tasks=tasks, status_filter=status, installers_map=installers_map)


@app.route("/tasks/new", methods=["GET", "POST"])
def task_new():
    client = db()
    installers = client.get_installers()
    if request.method == "POST":
        installer_id = request.form.get("installer_id")
        fields = {
            "תיאור משימה": request.form.get("description", ""),
            "סטטוס": request.form.get("status", "פתוח"),
            "תאריך ביצוע": request.form.get("date", ""),
        }
        if installer_id:
            fields["מתקין"] = [installer_id]
        fields = {k: v for k, v in fields.items() if v not in ["", None]}
        result = client.create("tasks", fields)
        if result:
            flash("משימה נוצרה בהצלחה!", "success")
            return redirect(url_for("tasks_list"))
        else:
            flash("שגיאה ביצירת משימה", "danger")
    return render_template("tasks/new.html", installers=installers)


# ─────────────────────────────────────────────
# API endpoints (JSON)
# ─────────────────────────────────────────────
@app.route("/api/customers")
def api_customers():
    data = db().get_customers(request.args.get("q"))
    return jsonify({"success": True, "data": data, "meta": {"total": len(data)}})


@app.route("/api/orders")
def api_orders():
    data = db().get_orders(request.args.get("status"))
    return jsonify({"success": True, "data": data, "meta": {"total": len(data)}})


@app.route("/api/inventory")
def api_inventory():
    data = db().get_inventory()
    return jsonify({"success": True, "data": data, "meta": {"total": len(data)}})


@app.route("/api/products")
def api_products():
    data = db().get_products()
    return jsonify({"success": True, "data": data, "meta": {"total": len(data)}})


@app.route("/api/health")
def api_health():
    return jsonify({"success": True, "message": "CRM פעיל"})


# ─────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

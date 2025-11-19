from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Simple in-memory storage
expenses = []

CATEGORIES = ["food", "transport", "entertainment"]
MONTHLY_BUDGET = 300  # default

@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/set-budget", methods=["GET", "POST"])
def set_budget():
    global MONTHLY_BUDGET

    if request.method == "POST":
        MONTHLY_BUDGET = float(request.form["budget"])
        expenses.clear()
        return redirect("/")
    
    # GET request
    return render_template("set_budget.html")

@app.route("/increase-budget", methods=["GET", "POST"])
def increase_budget():
    global MONTHLY_BUDGET

    if request.method == "POST":
        MONTHLY_BUDGET = float(request.form["budget"])
        return redirect("/")
    
    # GET request
    return render_template("increase_budget.html")

@app.route("/")
def dashboard():
    totals = {cat: 0 for cat in CATEGORIES}

    for exp in expenses:
        totals[exp["category"]] += exp["amount"]

    total_spent = sum(totals.values())
    percent_used = round((total_spent / MONTHLY_BUDGET) * 100, 2)

    totals["percent"] = min(percent_used, 100)

    return render_template("index.html", totals=totals, budget=MONTHLY_BUDGET)


@app.route("/add", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        amount = float(request.form["amount"])
        category = request.form["category"]

        totals = {cat: 0 for cat in CATEGORIES}
        for exp in expenses:
            totals[exp["category"]] += exp["amount"]

        total_spent = sum(totals.values())

        # Check budget limit
        if total_spent + amount > MONTHLY_BUDGET:
            return render_template(
                "add_expense.html",
                error=f"Cannot add expense ${amount}. Budget limit is ${MONTHLY_BUDGET}, already spent ${total_spent}."
            )

        # Otherwise add normally
        expenses.append({"amount": amount, "category": category})
        return redirect("/")

    # GET request
    return render_template("add_expense.html", error=None)





if __name__ == "__main__":
    app.run(debug=True)

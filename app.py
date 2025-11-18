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
        return redirect("/")

    return """
    <h2>Set Monthly Budget</h2>
    <form method="POST">
        <label>New Budget Amount:</label><br>
        <input type="number" name="budget" step="0.01" required>
        <br><br>
        <button type="submit">Save</button>
    </form>
    """

@app.route("/")
def dashboard():
    totals = {cat: 0 for cat in CATEGORIES}

    for exp in expenses:
        totals[exp["category"]] += exp["amount"]

    total_spent = sum(totals.values())
    percent_used = round((total_spent / MONTHLY_BUDGET) * 100, 2)

    totals["percent"] = min(percent_used, 100)

    return render_template("index.html", totals=totals)


@app.route("/add", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        amount = float(request.form["amount"])
        category = request.form["category"]

        expenses.append({"amount": amount, "category": category})

        return redirect("/")

    return """
    <h2>Add Expense</h2>
    <form method="POST">
        Amount: <input name="amount" type="number" step="0.01" required><br><br>
        Category:
        <select name="category">
            <option value="food">Food</option>
            <option value="transport">Transport</option>
            <option value="entertainment">Entertainment</option>
        </select><br><br>
        <button type="submit">Add</button>
    </form>
    """


if __name__ == "__main__":
    app.run(debug=True)

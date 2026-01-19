from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from helpers import apology, login_required
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///todo.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    user_id = session["user_id"]

    # Getting all the tasks the user has created
    tasks = db.execute("SELECT id, titulo, descricao, concluida, data_limite FROM tarefas WHERE user_id = ?", user_id)

    # Initially the user does not have any tasks so we need to cover that case
    if not tasks:
        return render_template("index.html", tasks=[])

    return render_template("index.html", tasks=tasks)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Invalid username!")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Invalid password!")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM utilizadores WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["password_hash"], request.form.get("password")
        ):
            return apology("Wrong password!")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        name = request.form.get("username")
        if not name:
            return apology("Invalid username!")

        email = request.form.get("email")
        if not email:
            return apology("Invalid email!")

        password = request.form.get("password")
        if not password:
            return apology("Invalid Password!")

        confirmation = request.form.get("confirmation")
        if password != confirmation:
            return apology("Invalid confirmation!")

        try:
            db.execute(
                "INSERT INTO utilizadores (username, email, password_hash) VALUES(?,?,?)", name, email, generate_password_hash(password))
            flash("Utilizador registado com sucesso!")
            return render_template("login.html")
        except ValueError:
            return apology("User already Exists!")
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/add_task", methods=["GET", "POST"])
@login_required
def add_task():

    if request.method == "POST":

        title = request.form.get("titulo")
        if not title:
            return apology("Invalid Title!")

        description = request.form.get("descricao")
        if not description:
            description = ""
        limit_date = request.form.get("data_limite")
        if not limit_date:
            return apology("Invalid date!")

        user_id = session["user_id"]

        db.execute("INSERT INTO tarefas (user_id, titulo, descricao, data_limite) VALUES (?,?,?,?)", user_id, title, description, limit_date)

        flash("Tarefa adicionada com sucesso!")
        return redirect("/")
    else:
        return render_template("task.html")

@app.route("/removetask", methods=["POST"])
@login_required
def remove_task():
    """Removes a task from the user database"""

    task_id = request.form.get("task_id")

    if not task_id:
        return apology("Task not found!")

    db.execute(
        "DELETE FROM tarefas WHERE id = ? AND user_id = ?",
        task_id,
        session["user_id"]
    )

    flash("Tarefa eliminada com sucesso!")
    return redirect("/")

@app.route("/conclude", methods=["POST"])
@login_required
def conclude():
    """Completes a task from the user database"""

    task_id = request.form.get("task_id")

    if not task_id:
        return apology("Task not found!")

    db.execute(
        "UPDATE tarefas SET concluida = ? WHERE id = ? AND user_id = ?",
        True,
        task_id,
        session["user_id"]
    )

    flash("Tarefa completa com sucesso!")
    return redirect("/")

@app.route("/edit_task", methods=["POST"])
@login_required
def edit_task():

    task_id = request.form.get("task_id")
    novo_titulo = request.form.get("titulo")
    nova_descricao = request.form.get("descricao")

    if not task_id or not novo_titulo:
        return apology("Invalid data!")

    db.execute(
        "UPDATE tarefas SET titulo = ?, descricao = ? WHERE id = ? AND user_id = ?",
        novo_titulo, nova_descricao, task_id, session["user_id"]
    )

    flash("Tarefa atualizada com sucesso!")
    return redirect("/")


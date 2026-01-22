import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, apology, allowed_file

# Configure application
app = Flask(__name__)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["UPLOAD_FOLDER"] = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
MAX_IMAGES = 3

Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

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


    reviews = db.execute("""
    SELECT
        r.id,
        r.title,
        r.created_at,

        u.username,
        u.profile_picture,

        -- ⭐ média de estrelas
            ROUND(
        (
            IFNULL(
                (SELECT SUM(stars) FROM ratings WHERE review_id = r.id),
                0
            ) + r.rating
        )
        /
        (
            IFNULL(
                (SELECT COUNT(*) FROM ratings WHERE review_id = r.id),
                0
            ) + 1
            ),
        1
        ) AS avg_rating,

        -- ❤️ likes
        (
            SELECT COUNT(*)
            FROM likes
            WHERE review_id = r.id
        ) AS likes_count,

        -- 💬 comentários
        (
            SELECT COUNT(*)
            FROM comments
            WHERE review_id = r.id
        ) AS comments_count,

        -- 🖼 imagem principal
        (
            SELECT image_path
            FROM review_images
            WHERE review_id = r.id
            LIMIT 1
        ) AS main_image

    FROM reviews r
    JOIN users u ON u.id = r.user_id
    ORDER BY r.created_at DESC
""")


    return render_template("index.html", reviews=reviews)




@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        user = request.form.get("username")
        passwd = request.form.get("password")
        cpasswd = request.form.get("confirmation")

        if not user or not passwd or not cpasswd:
            return apology("Fill the spaces in blank")
        elif passwd != cpasswd:
            return apology("passwords dont match")

        hashpasswd = generate_password_hash(passwd, method='scrypt', salt_length=16)

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", user, hashpasswd)

        return redirect("/login")

    return render_template("register.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/rate", methods=["GET", "POST"])
@login_required
def rate():
    if request.method == "POST":

        # Dados do formulário
        title = request.form.get("title")
        description = request.form.get("description")
        rating = request.form.get("rating")
        images = request.files.getlist("images")

        # Verificações
        if not title or not description or not rating:
            flash("Please fill all fields.")
            return redirect("/rate")

        if len(images) > MAX_IMAGES:
            flash("You can upload up to 3 images.")
            return redirect("/rate")

        # 1. Salvar review
        review_id = db.execute(
            """
            INSERT INTO reviews (user_id, title, description, rating)
            VALUES (?, ?, ?, ?)
            """,
            session.get("user_id"),
            title,
            description,
            rating
        )

        # 2. Salvar imagens (se existirem)
        for img in images:
            if img.filename == "":
                continue

            if allowed_file(img.filename):

                # Nome único
                ext = img.filename.rsplit(".", 1)[1].lower()
                filename = f"review_{review_id}_{os.urandom(8).hex()}.{ext}"

                # Caminho final
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

                # Salvar imagem
                img.save(filepath)

                # Registrar no banco
                db.execute(
                    "INSERT INTO review_images (review_id, image_path) VALUES (?, ?)",
                    review_id,
                    filename
                )
            else:
                flash("Only images (png, jpg, jpeg, gif) are allowed.")
                return redirect("/rate")

        flash("Review submitted successfully!")
        return redirect("/")

    return render_template("rate.html")


@app.route("/review/<int:review_id>")
def review_page(review_id):

    # Dados principais do post
    review = db.execute("""
        SELECT
            r.id,
            r.user_id,
            r.title,
            r.description,
            r.created_at,
            u.username,
            u.profile_picture,
            IFNULL(ROUND(AVG(rt.stars), 1), 0) AS avg_rating,
            COUNT(DISTINCT l.id) AS likes_count
        FROM reviews r
        JOIN users u ON u.id = r.user_id
        LEFT JOIN ratings rt ON rt.review_id = r.id
        LEFT JOIN likes l ON l.review_id = r.id
        WHERE r.id = ?
        GROUP BY r.id
    """, review_id)

    if not review:
        return apology("Post not found", 404)

    review = review[0]

    images = db.execute("""
        SELECT image_path
        FROM review_images
        WHERE review_id = ?
    """, review_id)

    comments = db.execute("""
        SELECT
            c.id,
            c.user_id,
            c.content,
            c.created_at,
            u.username,
            u.profile_picture
        FROM comments c
        JOIN users u ON u.id = c.user_id
        WHERE c.review_id = ?
        ORDER BY c.created_at DESC
    """, review_id)

    is_author = session.get("user_id") == review["user_id"]

    user_rating = None
    if session.get("user_id") and not is_author:
        result = db.execute("""
            SELECT stars
            FROM ratings
            WHERE user_id = ? AND review_id = ?
        """, session["user_id"], review_id)

        if result:
            user_rating = result[0]["stars"]

    # 🔥 USER LOGADO (para avatar do comment box)
    user = None
    if session.get("user_id"):
        user = db.execute("""
            SELECT id, username, profile_picture
            FROM users
            WHERE id = ?
        """, session["user_id"])[0]

    session["username"] = user["username"]
    session["profile_picture"] = user["profile_picture"]

    return render_template(
        "review.html",
        review=review,
        images=images,
        comments=comments,
        user_rating=user_rating,
        is_author=is_author,
        user=user  # 👈 ISSO É O QUE FALTAVA
    )


@app.route("/like/<int:review_id>", methods=["POST"])
@login_required
def like(review_id):
    user_id = session["user_id"]

    liked = db.execute(
        "SELECT 1 FROM likes WHERE user_id = ? AND review_id = ?",
        user_id, review_id
    )

    if liked:
        db.execute(
            "DELETE FROM likes WHERE user_id = ? AND review_id = ?",
            user_id, review_id
        )
    else:
        db.execute(
            "INSERT INTO likes (user_id, review_id) VALUES (?, ?)",
            user_id, review_id
        )

    likes_count = db.execute(
        "SELECT COUNT(*) AS count FROM likes WHERE review_id = ?",
        review_id
    )[0]["count"]

    return jsonify({
        "likes": likes_count,
        "liked": not liked
    })

@app.route("/review/<int:review_id>/rate", methods=["POST"])
@login_required
def rate_review(review_id):
    user_id = session["user_id"]
    stars = request.json.get("stars")

    if not stars or int(stars) not in range(1, 6):
        return jsonify({"error": "Invalid rating"}), 400

    # Dados do review
    review = db.execute(
        "SELECT user_id FROM reviews WHERE id = ?",
        review_id
    )[0]

    # autor não pode avaliar
    if review["user_id"] == user_id:
        return jsonify({"locked": True})

    # rating existente?
    existing = db.execute("""
        SELECT id FROM ratings
        WHERE user_id = ? AND review_id = ?
    """, user_id, review_id)

    if existing:
        db.execute("""
            UPDATE ratings
            SET stars = ?
            WHERE user_id = ? AND review_id = ?
        """, stars, user_id, review_id)
    else:
        db.execute("""
            INSERT INTO ratings (stars, user_id, review_id)
            VALUES (?, ?, ?)
        """, stars, user_id, review_id)

    # ⭐ média REAL (só ratings)
    avg_rating = db.execute("""
        SELECT ROUND(AVG(stars), 1) AS avg
        FROM ratings
        WHERE review_id = ?
    """, review_id)[0]["avg"] or 0

    return jsonify({
        "avg_rating": avg_rating,
        "user_rating": int(stars)
    })


@app.route("/comment/<int:review_id>", methods=["POST"])
@login_required
def add_comment(review_id):
    data = request.get_json()
    content = data.get("content", "").strip()

    if not content:
        return jsonify({"error": "Comentário vazio"}), 400

    user_id = session["user_id"]

    db.execute("""
        INSERT INTO comments (content, user_id, review_id)
        VALUES (?, ?, ?)
    """, content, user_id, review_id)

    comment = db.execute("""
        SELECT
            c.id,
            c.content,
            c.created_at,
            c.user_id,
            u.username,
            u.profile_picture
        FROM comments c
        JOIN users u ON u.id = c.user_id
        WHERE c.id = last_insert_rowid()
    """)[0]

     # 🔥 monta URL certinha aqui
    comment["profile_picture_url"] = (
        f"/static/uploads/{comment['profile_picture']}"
        if comment["profile_picture"]
        else "/static/uploads/default_pfp.png"
    )

    comment["is_owner"] = True  # 🔥 esse comentário acabou de ser criado por ele

    return jsonify(comment)


@app.route("/comment/delete/<int:comment_id>", methods=["POST"])
@login_required
def delete_comment(comment_id):
    user_id = session["user_id"]

    # verifica se o comentário existe e é do usuário
    comment = db.execute("""
        SELECT id
        FROM comments
        WHERE id = ? AND user_id = ?
    """, comment_id, user_id)

    if not comment:
        return jsonify({"error": "Not authorized"}), 403

    # apaga comentário + filhos (thread inteira)
    db.execute("""
        DELETE FROM comments
        WHERE id = ? OR parent_id = ?
    """, comment_id, comment_id)

    return jsonify({"success": True})

@app.route("/profile")
@login_required
def my_profile():
    return redirect(f"/profile/{session['user_id']}")

def profile():
    user_id = session["user_id"]

    user = db.execute("""
        SELECT
            id,
            username,
            profile_picture
        FROM users
        WHERE id = ?
    """, user_id)[0]

    stats = db.execute("""
        SELECT
            COUNT(DISTINCT r.id) AS posts,
            COUNT(DISTINCT l.id) AS likes
        FROM users u
        LEFT JOIN reviews r ON r.user_id = u.id
        LEFT JOIN likes l ON l.review_id = r.id
        WHERE u.id = ?
    """, user_id)[0]

    posts = db.execute("""
        SELECT
            r.id,
            r.title,
            r.created_at,
            (
                SELECT image_path
                FROM review_images
                WHERE review_id = r.id
                LIMIT 1
            ) AS main_image,
            (
                SELECT COUNT(*) FROM likes WHERE review_id = r.id
            ) AS likes_count,
            (
                SELECT COUNT(*) FROM comments WHERE review_id = r.id
            ) AS comments_count
        FROM reviews r
        WHERE r.user_id = ?
        ORDER BY r.created_at DESC
    """, user_id)


    return render_template(
        "profile.html",
        user=user,
        stats=stats,
        posts=posts,
        is_owner=(user["id"] == session["user_id"])
    )

@app.route("/profile/<int:user_id>")
@login_required
def profile(user_id):

    user = db.execute("""
        SELECT id, username, profile_picture
        FROM users
        WHERE id = ?
    """, user_id)


    if not user:
        return apology("User not found", 404)

    user = user[0]

    stats = db.execute("""
        SELECT
            COUNT(DISTINCT r.id) AS posts,
            COUNT(DISTINCT l.id) AS likes
        FROM users u
        LEFT JOIN reviews r ON r.user_id = u.id
        LEFT JOIN likes l ON l.review_id = r.id
        WHERE u.id = ?
    """, user["id"])[0]

    posts = db.execute("""
        SELECT
            r.id,
            r.title,
            r.created_at,
            (
                SELECT image_path
                FROM review_images
                WHERE review_id = r.id
                LIMIT 1
            ) AS main_image,
            (
                SELECT COUNT(*) FROM likes WHERE review_id = r.id
            ) AS likes_count,
            (
                SELECT COUNT(*) FROM comments WHERE review_id = r.id
            ) AS comments_count
        FROM reviews r
        WHERE r.user_id = ?
        ORDER BY r.created_at DESC
    """, user["id"])

    is_owner = session.get("user_id") == user["id"]

    return render_template(
        "profile.html",
        user=user,
        stats=stats,
        posts=posts,
        is_owner=is_owner
    )


@app.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    user_id = session["user_id"]

    if request.method == "POST":
        username = request.form.get("username")
        photo = request.files.get("photo")

        # 🔤 atualizar username
        if username:
            db.execute(
                "UPDATE users SET username = ? WHERE id = ?",
                username, user_id
            )

        # 🖼 atualizar foto
        if photo and photo.filename != "" and allowed_file(photo.filename):
            ext = photo.filename.rsplit(".", 1)[1].lower()
            filename = f"user_{user_id}_{os.urandom(6).hex()}.{ext}"
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            photo.save(path)

            db.execute(
                "UPDATE users SET profile_picture = ? WHERE id = ?",
                filename, user_id
            )

        flash("Profile updated!")
        return redirect("/profile")

    user = db.execute("SELECT * FROM users WHERE id = ?", user_id)[0]
    return render_template("edit_profile.html", user=user)


@app.route("/profile/delete", methods=["POST"])
@login_required
def delete_profile():
    user_id = session["user_id"]

    # apagar dados relacionados
    db.execute("DELETE FROM comments WHERE user_id = ?", user_id)
    db.execute("DELETE FROM likes WHERE user_id = ?", user_id)
    db.execute("DELETE FROM ratings WHERE user_id = ?", user_id)
    db.execute("DELETE FROM reviews WHERE user_id = ?", user_id)

    # apagar usuário
    db.execute("DELETE FROM users WHERE id = ?", user_id)

    session.clear()
    return "", 204

@app.route("/review/<int:review_id>/delete", methods=["POST"])
@login_required
def delete_review(review_id):

    print("CHEGOU NA ROTA DELETE")

    # Confere se o post existe e é do usuário
    review = db.execute(
        "SELECT user_id FROM reviews WHERE id = ?",
        review_id
    )

    if not review:
        return apology("Post not found", 404)

    if review[0]["user_id"] != session["user_id"]:
        return apology("Not allowed", 403)

    # Apaga tudo relacionado
    db.execute("DELETE FROM likes WHERE review_id = ?", review_id)
    db.execute("DELETE FROM comments WHERE review_id = ?", review_id)
    db.execute("DELETE FROM ratings WHERE review_id = ?", review_id)
    db.execute("DELETE FROM review_images WHERE review_id = ?", review_id)
    db.execute("DELETE FROM reviews WHERE id = ?", review_id)

    return redirect("/")


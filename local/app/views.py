from flask import jsonify, render_template, Blueprint, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User
from app import db

views = Blueprint("views", __name__)

# Create route decorators

# Home Page
@views.route('/')
def out():
    return render_template("out.html", user=current_user)

@views.route('/home')
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)

@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')
        meal_type = request.form.get('meal_type')

        if not text:
            flash('Post cannot be empty.', category='danger')
            return redirect(url_for('views.home'))
        elif not meal_type:
            flash('Please select a meal type for your recipe.', category='danger')
            return redirect(url_for('views.home'))
        else:
            post = Post(text=text, author=current_user.id, meal_type=meal_type)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('home.html', user=current_user)

@views.route("delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='danger')
    elif current_user.id != post.author:
        flash("You do not have permission to delete this post.", category='danger')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')
    
    return redirect(url_for('views.home'))

@views.route("/profile/<username>")
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash("User does not exist.", category='danger')
        return redirect(url_for('views.home'))
    
    posts = user.posts
    return render_template("profile.html", user=current_user, posts=posts, username=username)

@views.route("/like-post/<int:post_id>", methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get(post_id)
    if post:
        if current_user in post.likes:
            post.likes.remove(current_user)
        else:
            post.likes.append(current_user)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False})

from flask import render_template, url_for, flash, redirect,abort, request
from Qwitter import app, db
from Qwitter.forms import RegistrationForm, LoginForm, PostForm
from Qwitter.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required




@app.route('/home')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username= form.username.data, email= form.email.data, password= form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account registered Successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form = form)

@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))

    form = LoginForm()
    if form.validate_on_submit():
        # if form.email.data =='admin@blog.com' and form.password.data == 'password':
        #     flash('Welcome back!', 'success')
        #     return redirect(url_for('home'))
        # else:
        user = User.query.filter_by(email = form.email.data).first()
        if user and user.password==form.password.data:
            login_user(user, remember=form.remember.data)
            flash('Welcome Back! ','success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful! Please Enter correct Details', 'danger')
        

    return render_template('login.html', title='Login', form = form)



@app.route('/logout')
def logout():
    logout_user()
    flash('Logout successfully ','success')
    return redirect(url_for('login'))



@app.route('/account')
def account():
    if current_user.is_authenticated:
        return render_template('account.html', title = 'Profile')
    else:
        flash('You must login first', 'danger')
        return redirect(url_for('login'))



@app.route("/post", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')



@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)



@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')



@app.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))
from flask.helpers import flash
from werkzeug.utils import redirect
from url_shortener_app.models import Creator, ShortUrl
from url_shortener_app.forms import CreateShortUrlForm, LoginForm, RegistrationForm
from url_shortener_app import app, db
from flask import render_template, url_for
from flask_login import login_user, logout_user, login_required, current_user


def get_url_id(base62_value):
    BASE62 = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    number = 0
    for i in range(len(base62_value)-1, -1, -1):
        number += BASE62.index(base62_value[i]) * (62 ** abs(i - len(base62_value) + 1))
    return number


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_username = form.username.data
        attempted_password = form.password.data
        attempted_user = Creator.query.filter_by(
            username=attempted_username).first()
        if attempted_user and attempted_user.check_password(attempted_password):
            login_user(attempted_user)
            flash(f'Success! You are logged in as {attempted_username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash(f'Username and Password are invalid!', category='danger')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        plain_text_password = form.password1.data
        user_to_create = Creator(username=username, email=email,
                              password=plain_text_password)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully and you are logged in as {username}.', category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}:
        for error in form.errors.values():
            flash(f'Error in creating account {error}', category='danger')
    return render_template('register.html', form=form)


@app.route('/home', methods=['POST', 'GET'])
@login_required
def home_page():
    form = CreateShortUrlForm()
    urls = current_user.urls
    # print(bool(urls))
    if form.validate_on_submit():
        url_name = form.url_name.data
        original_url = form.original_url.data
        created_url = ShortUrl(name=url_name, original_url=original_url,creator_id=current_user.id)
        db.session.add(created_url)
        db.session.commit()
        return redirect(url_for('home_page'))
    if form.errors != {}:
        for error in form.errors.values():
            flash(f'Error in creating short URL {error}', category='danger')
    return render_template('dashboard.html', urls=urls, form=form)



@app.route('/logout')
def logout_page():
    logout_user()
    flash(f'You have been logged out.', category='info')
    return redirect(url_for('login_page'))


@app.route('/redirect/<short_url>')
def redirect_page(short_url):
    url_id = get_url_id(short_url)
    original_url = ShortUrl.query.get(int(url_id)).original_url
    # print(url_id)
    return redirect(original_url)

@app.route('/delete/<short_url>')
def delete_page(short_url):
    url_id = get_url_id(short_url)
    url_to_delete = ShortUrl.query.get(int(url_id))
    db.session.delete(url_to_delete)
    db.session.commit()
    flash('Url deleted successfully', category='success')
    return redirect(url_for('home_page'))
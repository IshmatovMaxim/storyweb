from flask import render_template, redirect, request, url_for, g
from flask.ext.login import login_required, login_user
from flask.ext.login import logout_user, current_user

from tmi.core import app
from tmi.util import jsonify
from tmi.model import User
from tmi.model.forms import LoginForm, Invalid


@app.route("/", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('ui'))
    error, data = None, dict(request.form.items())
    try:
        data = LoginForm().deserialize(data)
        user = User.query.filter_by(email=data.get('email')).first()
        if user is None or not user.check_password(data.get('password')):
            error = "Invalid email or password"
        else:
            login_user(user, remember=True)
            return redirect(request.args.get("next") or url_for('ui'))
    except Invalid:
        pass
    return render_template("login.html", data=data, error=error)


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/api/1/session", methods=["GET"])
def get_session():
    return jsonify({
        'user': g.user if g.user.is_authenticated() else None,
        'logged_in': g.user.is_authenticated(),
        'is_admin': g.user.is_admin if g.user.is_authenticated() else False
    })

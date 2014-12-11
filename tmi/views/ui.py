import os
from flask import render_template, redirect, url_for

from tmi.core import app
from tmi import authz


def angular_templates():
    partials_dir = os.path.join(app.static_folder, 'templates')
    for (root, dirs, files) in os.walk(partials_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, 'rb') as fh:
                file_name = file_path[len(partials_dir) + 1:]
                yield (file_name, fh.read().decode('utf-8'))


@app.route('/app')
def ui():
    if not authz.logged_in():
        return redirect(url_for('login'))
    return render_template("app.html", templates=angular_templates())

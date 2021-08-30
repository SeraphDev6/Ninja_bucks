from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.ninja import Ninja
from flask_app.models.message import Message


@app.route('/login/')
def login():
    return render_template('ninja_login.html')

@app.route('/login_submit', methods=['POST'])
def sumbit_login():
    ninja_id=Ninja.has_username(request.form)
    if not ninja_id:
        return redirect('/login')
    session['id'] = ninja_id
    return redirect(f"/ninja/{session['id']}")

@app.route('/ninja/<id>/')
def view_ninja(id):
    if 'id' not in session:
        return redirect('/login')
    if 'authority' not in session and not session['id'] == int(id):
        return redirect(f"/ninja/{session['id']}")
    ninja = Ninja.get_by_id({'id':id})
    messages = Message.get_all_messages_for_ninja({'ninja_id':id})
    return render_template("view_ninja.html",ninja=ninja,messages=messages)
from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.ninja import Ninja
from flask_app.models.sensei import Sensei
from flask_app.models.message import Message

@app.route('/edit/<id>/')
def edit_ninja(id):
    if not 'authority' in session or session['authority'] < 2:
        return redirect('/')
    ninja=Ninja.get_by_id({'id':id})
    messages = Message.get_all_messages_for_ninja({'ninja_id':ninja.id})
    return render_template('edit.html',ninja=ninja,messages=messages)

@app.route('/submit_edit', methods=['POST'])
def submit_edit():
    ninja = Ninja.get_by_id({'id':request.form['ninja_id']})
    ninja.update(request.form)
    return redirect(f"/ninja/{request.form['ninja_id']}")

@app.route('/delete_message/<id>/')
def delete_message(id):
    if not 'authority' in session or session['authority'] < 2:
        return redirect('/')
    message = Message.get_by_id({'id':id})
    ninja_id=message.ninja_id
    message.delete()
    return redirect(f"/edit/{ninja_id}")

@app.route('/delete/<id>/')
def delete_ninja(id):
    if not 'authority' in session or session['authority'] < 3:
        return redirect('/')
    ninja = Ninja.get_by_id({'id':id})
    return render_template('delete_ninja.html', ninja=ninja)

@app.route('/confirm_delete', methods=['POST'])
def finish_delete():
    ninja = Ninja.get_by_id(request.form)
    data =  {'ninja_id':ninja.id}
    Message.delete_all_messages_for_ninja(data)
    ninja.delete_self()
    return redirect('/')

@app.route('/add_sensei/')
def sensei_form():
    if 'authority' in session and session['authority']>=3:
        return render_template('add_sensei.html')
    return redirect('/')

@app.route('/new_sensei', methods=['POST'])
def new_sensei():
    if not Sensei.validate_reg(request.form):
        return redirect('/add_sensei')
    Sensei.save(request.form)
    return redirect('/senseis')

@app.route('/senseis/')
def view_all_senseis():
    if 'authority' in session and session['authority']>=3:
        return render_template('view_senseis.html',results=Sensei.get_all())
    return redirect('/')

@app.route('/edit_sensei/<id>/')
def edit_sensei(id):
    if 'authority' in session and session['authority']>=3:
        return render_template('edit_sensei.html',sensei=Sensei.get_by_id({'id':id}))
    return redirect('/')

@app.route('/update_sensei', methods=['POST'])
def update_sensei():
    if not Sensei.validate_reg(request.form):
        return redirect(f"/edit_sensei/{request.form['id']}")
    Sensei.update(request.form)
    return redirect('/senseis')

@app.route('/delete_sensei/<id>/')
def delete_sensei(id):
    if 'authority' in session and session['authority']>=3:
        return render_template('delete_sensei.html',sensei=Sensei.get_by_id({'id':id}))
    return redirect('/')

@app.route('/confirm_delete_sensei', methods=['POST'])
def confirm_delete_sensei():
    Sensei.get_by_id({'id':request.form['id']}).delete_self()
    return redirect('/senseis')
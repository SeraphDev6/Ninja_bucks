from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.ninja import Ninja
from flask_app.models.sensei import Sensei
from flask_app.models.message import Message

@app.route('/')
def index():
    if not Sensei.any_senseis():
        session['id']=0
        session['authority']=5
        return redirect('/add_sensei')
    if not 'id' in session:
        return redirect('/login')
    elif not 'authority' in session:
        return redirect(f"/ninja/{session['id']}")
    return render_template('index.html',results=Ninja.get_all())

@app.route('/sensei_login/')
def sensei_login():
    return render_template('sensei_login.html')

@app.route('/sensei_login_submit', methods=['POST'])
def submit_sensei_login():
    sensei = Sensei.valid_login(request.form)
    if not sensei:
        return redirect('/sensei_login/')
    session['id']=sensei.id
    session['authority']=int(sensei.authority)
    return redirect('/')

@app.route('/add_ninja')
def add_ninja():
    if 'authority' in session and session['authority'] >= 2:
        return render_template("add_ninja.html")
    return redirect('/')

@app.route('/new_ninja', methods=['POST'])
def new_ninja():
    if not Ninja.valid_ninja(request.form):
        return redirect('/add_ninja')
    Ninja.save(request.form)
    return redirect('/')

@app.route('/earn/<id>')
def earn(id):
    if 'id' not in session:
        return redirect('/login')
    if 'authority' not in session:
        return redirect('/sensei_login')
    ninja =Ninja.get_by_id({'id':id})
    return render_template('earn.html', ninja=ninja)

@app.route('/add_bucks', methods=['POST'])
def add_bucks():
    ninja=Ninja.get_by_id({'id':request.form['ninja_id']})
    ninja.add_ninja_bucks(request.form['ninja_buck_change'])
    Message.save(request.form)
    return redirect(f"/ninja/{ninja.id}")

@app.route('/redeem/<id>')
def redeem(id):
    if 'id' not in session:
        return redirect('/login')
    if 'authority' not in session:
        return redirect('/sensei_login')
    ninja =Ninja.get_by_id({'id':id})
    return render_template('redeem.html', ninja=ninja)

@app.route('/redeem_bucks', methods=['POST'])
def redeem_bucks():
    data={
        'ninja_id':request.form['ninja_id'],
        'sensei_id':request.form['sensei_id'],
        'ninja_buck_change':int(request.form['ninja_buck_change'])*-1,
        'message_text':request.form['message_text']
    }
    ninja=Ninja.get_by_id({'id':data['ninja_id']})
    if not ninja.can_afford(data['ninja_buck_change']):
        return redirect(f"/redeem/{ninja.id}")
    ninja.add_ninja_bucks(data['ninja_buck_change'])
    Message.save(data)
    return redirect(f"/ninja/{ninja.id}")

@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/login')
from flask import Flask, render_template, request, redirect, url_for, session, flash, logging
from wtforms import Form, StringField, PasswordField, validators, TextField, BooleanField,DateField
import os

app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'app.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

phone_book = [{'name':'James', 'phone':'00007777'},
            {'name':'John', 'phone':'07333333'},
            {'name':'Bill', 'phone':'07444444'}]
store = {}
#home
@app.route('/')
def home():
    Lists = phone_book
    for item in Lists:
        return render_template("home.html", Lists=Lists)
    else:
        msg = 'No List Found'
        return render_template("home.html", msg=msg)


#Contact Form class
class addForm(Form):
    name = StringField('name', [validators.Length(min = 1, max = 1000)])
    phone = StringField('phone', [validators.Length(min = 3, max = 10)])
    
#Add details
@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    form = addForm(request.form)
    if request.method == 'POST' and form.validate():
        name = request.form['name']
        phone = request.form['phone']
        store['name'] = name
        store['phone'] = phone
        phone_book.insert(0,store)

        flash('contact created', 'success')
        return redirect(url_for('home'))

    return render_template("add_contact.html", form=form)

@app.route('/delete_contact/<string:Id>', methods=['POST'])
def delete_contact(Id):
    for item in store:
        del store['name']
        del store['phone']
        flash('contact Removed', 'success')
        return redirect(url_for('home'))
    else:
        msg = 'No contacts Found'
        return render_template("home.html", msg=msg)

@app.route('/edit_contact/<string:Id>', methods=['GET', 'POST'])
def edit_contact(Id):
    form = addForm(request.form)
    if store == {}:
        msg = 'No List Found'
        return render_template("home.html", msg=msg)
    else:
    #get item by title
        for item in store:
            #populate form fields
            request.form['name']= store['name']
            request.form['phone']  = store['phone']
            if request.method == 'POST' and form.validate():
                name = request.form['name']
                phone = request.form['phone']
                store['name'] = name
                store['phone'] = phone
                phone_book.append(store)

                flash('List edited', 'success')
                return redirect(url_for('home'))

    return render_template("edit_contact.html", form=form)


if __name__ == "__main__":
    app.secret_key='ThisIsSecret'
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
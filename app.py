from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from forms import ClientForm
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tattoo_salon.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads/clients'
db = SQLAlchemy(app)

from models import Client

@app.route('/')
def index():
    clients = Client.query.all()
    return render_template('index.html', clients=clients)

@app.route('/add', methods=['GET', 'POST'])
def add_client():
    form = ClientForm()
    if form.validate_on_submit():
        filename = secure_filename(form.photo.data.filename)
        form.photo.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        new_client = Client(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            photo=filename
        )
        db.session.add(new_client)
        db.session.commit()
        flash('Client added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_client.html', form=form)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_client(id):
    client = Client.query.get_or_404(id)
    form = ClientForm(obj=client)
    if form.validate_on_submit():
        if form.photo.data:
            filename = secure_filename(form.photo.data.filename)
            form.photo.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            client.photo = filename
        client.name = form.name.data
        client.email = form.email.data
        client.phone = form.phone.data
        db.session.commit()
        flash('Client updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('edit_client.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)

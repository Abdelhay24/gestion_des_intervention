from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
# import matplotlib.pyplot as plt
import io
import base64
from sqlalchemy import ForeignKey
from datetime import datetime
def convert_to_date(date_str):
    """
    Converts a string to a Python date object using multiple formats.

    Args:
        date_str (str): The date string to convert.

    Returns:
        datetime.date: A Python date object.

    Raises:
        ValueError: If the date string is invalid.
    """
    # List of possible date formats
    formats = ['%d/%m/%y', '%d-%m-%Y', '%Y-%m-%d', '%m/%d/%y']

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue  # Try the next format

    # If no format matches, raise an error
    raise ValueError(f"Invalid date format: '{date_str}'")
from dateutil.parser import parse

app = Flask(__name__)
app.secret_key = "secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Client(db.Model):
    __tablename__ = 'client'

    id_Client = db.Column(db.Integer, primary_key=True)
    Nom = db.Column(db.String(20), nullable=False)
    PreNom = db.Column(db.String(20), nullable=False)
    Direction = db.Column(db.String(20), nullable=False)

    def __init__(self, Nom, PreNom, Direction):
        self.Nom = Nom
        self.PreNom = PreNom
        self.Direction = Direction
class Intervenant(db.Model):
    __tablename__ = 'intervenant'

    id_IN = db.Column(db.Integer, primary_key=True)
    Nom = db.Column(db.String(20),  nullable=False)
    PreNom = db.Column(db.String(20), nullable=False)
    Post = db.Column(db.String(20), nullable=False)

    def __init__(self, Nom, PreNom, Post):
        self.Nom = Nom
        self.PreNom = PreNom
        self.Post = Post

class Intervantion(db.Model):
    __tablename__ = 'intervantion'

    id_INS = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    motif = db.Column(db.String(20), nullable=False)
    ID_Client = db.Column(db.Integer, ForeignKey('client.id_Client'))
    ID_IN = db.Column(db.Integer, ForeignKey('intervenant.id_IN'))

    def __init__(self, date, type, motif, ID_C, ID_IN):
        self.date = date
        self.type = type
        self.motif = motif
        self.ID_Client = ID_C
        self.ID_IN = ID_IN




# Create the database
with app.app_context():
    db.create_all()
# def create_graph():
#     plt.figure(figsize=(8, 6))
#     categories = ['Category A', 'Category B', 'Category C', 'Category D']
#     values = [23, 45, 56, 78]
#     plt.bar(categories, values, color=['blue', 'green', 'red', 'purple'])
#     plt.title('Example Bar Chart', fontsize=16)
#     plt.xlabel('Categories', fontsize=12)
#     plt.ylabel('Values', fontsize=12)
#     plt.tight_layout()
#
#     # Sauvegarde du graphique en mémoire
#     buf = io.BytesIO()
#     plt.savefig(buf, format='png')
#     buf.seek(0)
#     return base64.b64encode(buf.getvalue()).decode('utf-8')
#
# @app.route('/graphs')
# def graph():
#     graph = create_graph()
#     return render_template('graph_page.html', graph=graph)
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/inscription',methods=['GET', 'POST'])
def inscription():
    Users = [
    {"name": "Alice", "pwd": "12345678"},
    {"name": "Bob", "pwd": "abcdefgh"},
    {"name": "Charlie", "pwd": "my_passwd"}
]
    if request.method == 'POST':
        nom = request.form['nom']
        mot_de_passe = request.form['mot_de_passe']

        # Check if the user exists and password matches
        for user in Users:
            if user["name"] == nom and user["pwd"] == mot_de_passe:
                flash('Welcome, ' + nom + '!', 'success')
                return redirect(url_for("home"))  # Redirect to the client page

        # If no match, redirect to intervenant page
        # flash('Invalid credentials, please try again.', 'danger')
        flash('weylak ye 3abdou ', 'danger')
        return redirect(url_for("inscription"))

    return render_template('inscription.html')
@app.route('/client')
def client():
    all_clients = Client.query.all()
    return render_template('client.html', clients=all_clients)


@app.route('/insertclient', methods=['POST'])
def insert():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        direction = request.form['direction']

        new_client = Client(nom, prenom, direction)
        db.session.add(new_client)
        db.session.commit()
        flash("The client has been added successfully!")
        return redirect(url_for('client'))


@app.route('/updateclient/<IdClient>/', methods=['POST'])
def update(IdClient):
    if request.method == "POST":
        client = Client.query.get(request.form.get('idClient'))  # Fetch the client by ID

        if client:
            client.Nom = request.form['nom']
            client.PreNom = request.form['prenom']
            client.Direction = request.form['direction']
            db.session.commit()
            flash("Client updated successfully!")
        else:
            flash("Client not found")

        return redirect(url_for('client'))
@app.route('/Deleteclient/<IdClient>/', methods =['GET','POST'])
def delete(IdClient):
    my_client=Client.query.get(IdClient)
    db.session.delete(my_client)
    db.session.commit()
    flash("client deleted successfuly")
    return redirect(url_for('client'))
@app.route('/intervenant')
def intervenant():
    all_IN = Intervenant.query.all()
    return render_template('intervenant.html', intervenants=all_IN)


@app.route('/insertIN', methods=['POST'])
def insert_IN():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        Post = request.form['Post']

        new_IN = Intervenant(nom, prenom, Post)
        db.session.add(new_IN)
        db.session.commit()
        flash("The Intervenant has been added successfully!")
        return redirect(url_for('intervenant'))


# @app.route('/updateIN/<id_IN>/', methods=['POST'])
# def update_IN(id_IN):
#     if request.method == "POST":
#         # IN = Intervenant.query.get(request.form.get(Id_IN))
#         IN=Intervenant.query.get(request.form.get(id_IN))
#
#         if IN:
#             IN.Nom = request.form['nom']
#             IN.PreNom = request.form['prenom']
#             IN.Post = request.form['Post']
#             db.session.commit()
#             flash("IN updated successfully!")
#         else:
#             flash("IN not found")
#
#         return redirect(url_for('intervenant'))
@app.route('/updateIN/<id_IN>/', methods=['GET', 'POST'])
def update_IN(id_IN):
    # Fetch the Intervenant by id_IN, using it directly from the URL parameter
    IN = Intervenant.query.get(id_IN)

    if request.method == "POST":
        if IN:
            IN.Nom = request.form['nom']
            IN.PreNom = request.form['prenom']
            IN.Post = request.form['Post']
            db.session.commit()
            flash("Intervenant updated successfully!")
        else:
            flash("Intervenant not found")


        return redirect(url_for('intervenant'))

    # If method is GET, render the update form (if you have one)
    return render_template('update_intervenant.html', intervenant=IN)


@app.route('/DeleteIN/<Id_IN>/', methods =['GET','POST'])
def delete_IN(Id_IN):
    my_IN=Intervenant.query.get(Id_IN)
    db.session.delete(my_IN)
    db.session.commit()
    flash("IN deleted successfuly")
    return redirect(url_for('intervenant'))


@app.route('/intervantion')
def intervantion():
    all_INS = Intervantion.query.all()
    return render_template('intervention.html', intervantion=all_INS)


@app.route('/insertINS', methods=['POST'])
def insert_INS():
    if request.method == 'POST':
        dateStr = request.form['date']
        date=datetime.strptime(dateStr, '%d/%m/%y').date()
        type = request.form['type']
        motif = request.form['motif']
        ID_C = request.form['ID_C']
        ID_IN = request.form['ID_IN']

        new_INS = Intervantion(date, type, motif,ID_C,ID_IN)
        db.session.add(new_INS)
        db.session.commit()
        flash("The Intervantion has been added successfully!")
        return redirect(url_for('intervantion'))


# @app.route('/updateIN/<id_IN>/', methods=['POST'])
# def update_IN(id_IN):
#     if request.method == "POST":
#         # IN = Intervenant.query.get(request.form.get(Id_IN))
#         IN=Intervenant.query.get(request.form.get(id_IN))
#
#         if IN:
#             IN.Nom = request.form['nom']
#             IN.PreNom = request.form['prenom']
#             IN.Post = request.form['Post']
#             db.session.commit()
#             flash("IN updated successfully!")
#         else:
#             flash("IN not found")
#
#         return redirect(url_for('intervenant'))
@app.route('/updateINS/<id_INS>/', methods=['GET', 'POST'])
def update_INS(id_INS):
    # Fetch the Intervenant by id_IN, using it directly from the URL parameter
    IN = Intervantion.query.get(id_INS)

    if request.method == "POST":
        if IN:
            date_Str = request.form['date']
            IN.date = convert_to_date(date_Str)
            IN.type = request.form['type']
            IN.motif = request.form['motif']
            IN.ID_Client = request.form['ID_C']
            IN.ID_IN = request.form['ID_IN']
            db.session.commit()
            flash("Intervenant updated successfully!")
        else:
            flash("Intervenant not found")

        return redirect(url_for('intervantion'))

    # If method is GET, render the update form (if you have one)
    return render_template('update_intervenant.html', intervenant=IN)


@app.route('/DeleteINS/<Id_INS>/', methods=['GET', 'POST'])
def delete_INS(Id_INS):
    my_INS = Intervantion.query.get(Id_INS)
    db.session.delete(my_INS)
    db.session.commit()
    flash("IN deleted successfuly")
    return redirect(url_for('intervantion'))





if __name__ == "__main__":
    app.run(debug=True)



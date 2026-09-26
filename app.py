
import json
import os
import time
from flask import Flask, render_template, request, redirect, session
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from email_validator import validate_email, EmailNotValidError
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev_key_change_in_production')
app.config['UPLOAD_FOLDER'] = 'static'
FICHIER_BDD = 'database.json'
FICHIER_CATALOGUE = 'catalogue.json'
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD_PLAIN', 'FORGERON2026')

STOCK_DE_BASE = [
	{"id": "couteau1", "nom": "Le Damas", "description": "Lame en acier damas aux motifs uniques.", "prix": 250, "image": "imagecouteau1.jpg"},
	{"id": "couteau2", "nom": "Le Brut de Forge", "description": "Lame brute de forge pour un style authentique.", "prix": 120, "image": "imagecouteau2.jpg"}
]

def charger_commandes():
	if not os.path.exists(FICHIER_BDD): return []
	with open(FICHIER_BDD, 'r', encoding='utf-8') as f: return json.load(f)

def sauvegarder_commandes(commandes):
	with open(FICHIER_BDD, 'w', encoding='utf-8') as f: json.dump(commandes, f, indent=4)

def charger_catalogue():
	if not os.path.exists(FICHIER_CATALOGUE):
		with open(FICHIER_CATALOGUE, 'w', encoding='utf-8') as f: json.dump(STOCK_DE_BASE, f, indent=4)
		return STOCK_DE_BASE
	with open(FICHIER_CATALOGUE, 'r', encoding='utf-8') as f: return json.load(f)

def sauvegarder_catalogue(catalogue):
	with open(FICHIER_CATALOGUE, 'w', encoding='utf-8') as f: json.dump(catalogue, f, indent=4)

def valider_email(email):
	try:
		validate_email(email)
		return True
	except EmailNotValidError:
		return False

def charger_panier_serveur(panier_json):
	try:
		panier = json.loads(panier_json) if panier_json else []
		for article in panier:
			if not isinstance(article.get('nom'), str) or not isinstance(article.get('prix'), (int, str)) or not isinstance(article.get('quantite'), int):
				return None
		return panier
	except:
		return None

@app.route('/')
def accueil():
	return render_template('index.html', produits=charger_catalogue())

@app.route('/galerie')
def page_galerie():
	return render_template('galerie.html', produits=charger_catalogue())

@app.route('/a-propos')
def page_a_propos():
	return render_template('a-propos.html')

@app.route('/contact', methods=['GET', 'POST'])
def page_contact():
	if request.method == 'POST':
		return render_template('contact.html', message_succes="Message reçu ! Nous vous répondrons rapidement.")
	return render_template('contact.html')

@app.route('/panier')
def page_panier():
	return render_template('panier.html')

@app.route('/savoir-faire')
def page_savoir_faire():
	return render_template('savoir_faire.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	erreur = None
	if request.method == 'POST':
		mdp = request.form.get('mdp', '')
		if mdp == ADMIN_PASSWORD:
			session['admin_connecte'] = True
			return redirect('/admin')
		else:
			erreur = "Mot de passe incorrect."
	return render_template('login.html', message_erreur=erreur)

@app.route('/logout')
def logout():
	session.pop('admin_connecte', None)
	return redirect('/')

@app.route('/commande', methods=['POST'])
def valider_commande():
	email = request.form.get('email', '').strip()
	nom = request.form.get('nom', '').strip()
	prenom = request.form.get('prenom', '').strip()
	anniversaire = request.form.get('anniversaire', '').strip()
	pays = request.form.get('pays', '').strip()
	adresse = request.form.get('adresse', '').strip()
	complement = request.form.get('complement', '').strip()
	code_postal = request.form.get('code_postal', '').strip()
	ville = request.form.get('ville', '').strip()
	panier_texte = request.form.get('panier_secret', '')

	# VALIDATION des données
	if not valider_email(email):
		return render_template('panier.html', erreur="Email invalide"), 400
	if not nom or not prenom or len(nom) < 2 or len(prenom) < 2:
		return render_template('panier.html', erreur="Nom/Prénom invalide"), 400
	if not anniversaire or not pays or not adresse or not code_postal or not ville:
		return render_template('panier.html', erreur="Données manquantes"), 400

	articles_commandes = charger_panier_serveur(panier_texte)
	if not articles_commandes or len(articles_commandes) == 0:
		return render_template('panier.html', erreur="Panier vide"), 400

	# CALCULS: Total couteaux + Frais de port selon le pays
	try:
		total_articles = sum(int(art['prix']) * int(art.get('quantite', 1)) for art in articles_commandes)
	except (ValueError, KeyError):
		return render_template('panier.html', erreur="Erreur de calcul du panier"), 400

	frais_port = 10 if pays == 'France' else 25
	total_ttc = total_articles + frais_port
	tva_calculee = round(total_ttc - (total_ttc / 1.20), 2)

	nouvelle_commande = {
		"id": int(time.time()),
		"email": email,
		"nom": nom,
		"prenom": prenom,
		"anniversaire": anniversaire,
		"adresse_complete": f"{adresse}, {complement} - {code_postal} {ville} ({pays})",
		"articles": articles_commandes,
		"total": total_ttc,
		"frais_port": frais_port,
		"tva": tva_calculee,
		"statut": "En préparation"
	}

	historique = charger_commandes()
	historique.append(nouvelle_commande)
	sauvegarder_commandes(historique)

	return render_template('confirmation.html', prenom=prenom)

@app.route('/admin')
def page_admin():
	if not session.get('admin_connecte'): return redirect('/login')
    
	historique = charger_commandes()
	chiffre_affaires = sum(cmd['total'] for cmd in historique)
	tva_totale = sum(cmd['tva'] for cmd in historique)
    
	clients_crm = {}
	for cmd in historique:
		email = cmd['email']
		if email not in clients_crm:
			clients_crm[email] = {"nom": cmd['nom'], "anniversaire": cmd['anniversaire'], "total_depense": 0, "nb_commandes": 0}
		clients_crm[email]['total_depense'] += cmd['total']
		clients_crm[email]['nb_commandes'] += 1

	return render_template('admin.html', commandes=historique, total_gagne=chiffre_affaires, tva_globale=round(tva_totale, 2), clients=clients_crm)

@app.route('/expedier/<int:id_commande>')
def expedier_commande(id_commande):
	if not session.get('admin_connecte'): return redirect('/login')
	historique = charger_commandes()
	for commande in historique:
		if commande.get('id') == id_commande:
			commande['statut'] = 'Expédiée'
			break
	sauvegarder_commandes(historique)
	return redirect('/admin')

@app.route('/admin/ajouter_couteau', methods=['POST'])
def ajouter_couteau():
	if not session.get('admin_connecte'): return redirect('/login')
	nom = request.form.get('nom', '').strip()
	description = request.form.get('description', '').strip()
	prix = request.form.get('prix', '').strip()
	photo = request.files.get('photo')

	# Validation
	if not nom or len(nom) < 2:
		return redirect('/admin?erreur=Nom+invalide')
	if not description or len(description) < 5:
		return redirect('/admin?erreur=Description+trop+courte')

	try:
		prix_int = int(prix)
		if prix_int <= 0:
			return redirect('/admin?erreur=Prix+invalide')
	except ValueError:
		return redirect('/admin?erreur=Prix+invalide')

	nom_fichier = "default.jpg"
	if photo and photo.filename != '':
		nom_fichier = secure_filename(photo.filename)
		if nom_fichier:
			photo.save(os.path.join(app.config['UPLOAD_FOLDER'], nom_fichier))

	catalogue = charger_catalogue()
	catalogue.append({
		"id": f"couteau_{int(time.time())}",
		"nom": nom,
		"description": description,
		"prix": prix_int,
		"image": nom_fichier
	})
	sauvegarder_catalogue(catalogue)
	return redirect('/admin?succes=Couteau+ajouté')

@app.route('/admin/supprimer_couteau/<couteau_id>', methods=['POST'])
def supprimer_couteau(couteau_id):
	if not session.get('admin_connecte'): return redirect('/login')
	catalogue = charger_catalogue()
	catalogue = [c for c in catalogue if c.get('id') != couteau_id]
	sauvegarder_catalogue(catalogue)
	return redirect('/admin?succes=Couteau+supprimé')

@app.errorhandler(404)
def page_non_trouvee(error):
	return render_template('404.html'), 404

@app.errorhandler(500)
def erreur_serveur(error):
	return render_template('500.html'), 500

if __name__ == '__main__':
	port = int(os.getenv('PORT', 5001))
	app.run(debug=False, port=port, host='0.0.0.0')

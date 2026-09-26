# 🔨 L'Atelier des Lames - Site E-Commerce

Site de vente de couteaux artisanaux avec gestion admin.

## ✨ Améliorations Effectuées

### 🔒 Sécurité
- ✅ Mot de passe déplacé dans `.env` (plus de hardcoding)
- ✅ Validation des emails avec `email-validator`
- ✅ Validation de tous les formulaires (côté serveur)
- ✅ Protection contre les injections XSS et manipulation du panier

### 🛒 Panier & Commandes
- ✅ Système de **quantités** (augmenter/diminuer au lieu de dupliquer)
- ✅ Affichage détaillé avec prix unitaire × quantité
- ✅ Confirmation avant suppression d'article
- ✅ **Compteur du panier** en navigation (badge rouge)

### 👨‍💼 Espace Admin
- ✅ Formulaire pour **ajouter des couteaux** (nom, description, prix, photo)
- ✅ Formulaire pour **supprimer des couteaux**
- ✅ Messages d'erreur/succès
- ✅ Meilleure organisation du dashboard

### 🎨 Design & UX
- ✅ **Footer** avec liens et mentions légales
- ✅ **Pages 404 & 500** élégantes
- ✅ Affichage prix lors de l'ajout au panier
- ✅ Amélioration visuelle du panier avec boutons +/-
- ✅ Navigation cohérente sur toutes les pages

### 📦 Produits
- ✅ 4 couteaux ajoutés au catalogue avec images
- ✅ Descriptions enrichies

### 📋 Code
- ✅ `requirements.txt` pour les dépendances
- ✅ `.gitignore` pour ignorer les fichiers sensibles
- ✅ Code mieux organisé et commenté

---

## 🚀 Installation & Lancement

### 1. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 2. Configurer l'environnement
Modifie le fichier `.env` :
```
FLASK_SECRET_KEY=ta_clé_secrète_très_longue_ici
ADMIN_PASSWORD_PLAIN=ton_mot_de_passe_admin
```

### 3. Lancer le serveur
```bash
python app.py
```

Le site est accessible sur : **http://localhost:5001**

---

## 📝 Identifiants par défaut

- **Admin Panel** : `/admin`
- **Mot de passe** : `FORGERON2026` (changeable dans `.env`)

---

## 📂 Structure du projet

```
/
├── app.py              ← Backend Flask
├── catalogue.json      ← Liste des couteaux
├── database.json       ← Commandes (créé automatiquement)
├── requirements.txt    ← Dépendances Python
├── .env               ← Variables d'environnement (PRIVÉ)
├── .gitignore         ← Fichiers à ignorer dans Git
├── static/
│   ├── style.css      ← Styles globaux
│   └── script.js      ← JavaScript (panier, compteur)
└── templates/
    ├── index.html         ← Homepage
    ├── panier.html        ← Page panier
    ├── savoir-faire.html  ← Page savoir-faire
    ├── admin.html         ← Dashboard admin
    ├── login.html         ← Connexion admin
    ├── confirmation.html  ← Confirmation commande
    ├── 404.html          ← Page non trouvée
    └── 500.html          ← Erreur serveur
```

---

## 🎯 Fonctionnalités Principales

### 👥 Clients
- Parcourir la collection de couteaux
- Ajouter des articles au panier (avec quantités)
- Voir le total en direct
- Valider une commande avec infos de livraison
- Page de confirmation

### 👨‍🍳 Admin
- Dashboard avec stats (CA, TVA, nb commandes)
- CRM clients (emails, anniversaires, dépenses)
- **Ajouter/Supprimer des couteaux** ← NOUVEAU
- Voir les commandes en attente
- Marquer comme "Expédiée"
- Archives des commandes

---

## 🔜 Prochaines Étapes Possibles

- [ ] **Paiement réel** : Intégrer Stripe ou PayPal
- [ ] **Envoi d'emails** : Confirmation + suivi commande
- [ ] **Stock** : Gérer les quantités disponibles
- [ ] **Codes promo** : Réductions automatiques
- [ ] **Galerie photos** : Avant/après des couteaux
- [ ] **Avis clients** : Système de notation
- [ ] **Newsletter** : Inscription clients

---

## ⚠️ À Noter

- Les images utilisées sont des placeholders de Unsplash
- Les données sont sauvegardées en JSON (DB simple)
- Pour la production, utiliser une vraie base de données (PostgreSQL, MongoDB)
- Changer la `SECRET_KEY` en production

---

**Bon courage dans l'atelier ! 🔨✨**

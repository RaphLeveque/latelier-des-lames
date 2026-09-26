const cartes = document.querySelectorAll(".carte-couteau");

cartes.forEach(function(carte) {
    carte.addEventListener("click", function() {
        const nomCouteau = carte.querySelector("h3").textContent;
        const prixCouteau = carte.getAttribute("data-prix");

        let panier = JSON.parse(localStorage.getItem("monPanier")) || [];

        // Chercher si le couteau est déjà dans le panier
        let couteauExistant = panier.find(item => item.nom === nomCouteau);

        if (couteauExistant) {
            // Si oui, augmenter la quantité
            couteauExistant.quantite = (couteauExistant.quantite || 1) + 1;
        } else {
            // Sinon, l'ajouter avec quantité 1
            panier.push({ nom: nomCouteau, prix: prixCouteau, quantite: 1 });
        }

        localStorage.setItem("monPanier", JSON.stringify(panier));
        mettreAJourCompteur();

        const toast = document.getElementById("toast-notification");
        toast.textContent = nomCouteau + " ("+prixCouteau+"€) ajouté au panier ! 🗡️";
        toast.classList.add("afficher");

        setTimeout(function() {
            toast.classList.remove("afficher");
        }, 3000);
    });
});

function mettreAJourCompteur() {
    let panier = JSON.parse(localStorage.getItem("monPanier")) || [];
    let totalArticles = panier.reduce((sum, item) => sum + (item.quantite || 1), 0);

    let compteur = document.getElementById("compteur-panier");
    if (compteur) {
        compteur.textContent = totalArticles;
        compteur.style.display = totalArticles > 0 ? "flex" : "none";
    }
}

// Initialiser au chargement
document.addEventListener("DOMContentLoaded", mettreAJourCompteur);
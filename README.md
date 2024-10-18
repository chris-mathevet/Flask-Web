# TP Flask

## Membres du groupe

MATHEVET Chris 
MARQUES Julian
Classe : TD 21



Pour installer toutes les dépendances
> pip install -r .\requirements.txt                                                                                          

Pour créer la BD 
> flask loaddb myApp/data.yml 

Pour supprimer la BD
> flask cleardb

Pour lancer le site
> flask run


### GITHUB
https://github.com/chris-mathevet/Flask-Web


### Fonctionnalité

- lien entre les pages (dans le header, boutons lien cliquable etc)
- bouton login/signup fonctionne + implémentation du login/signup
- page avec tous les auteurs (Possibilité de les voir (sur une page auteur) Et les supprimer)
- page auteur avec le nom, les livres qu'il a etc 
- barre de recherche
- Favoris livre
- recommandation (via les favoris)
- ajout de commentaire sous un livre + voir commentaire des autres (édit, supprimer, voir le commentaire)
- ajout de note pour un livre
- note moyenne par livre par rapport aux notes des utilisateurs
- Gérer les erreurs 404 (page spéciale)
- pour la page avec des livres ou auteurs, on affiche avec une limite de 10 livres/auteurs et on peut augmenter cette taille. (bouton Voir Plus)
- voir le favoris des personnes qui ont commenté un livre
- footer




## Fonctionnalité expliqué
Recommandation  

Search

Moyenne note  

Chaque personne peut ajouter une note en plus d'un commentaire la note est entre 0 et 5 sous-formes d'étoile qu'on peut sélectionner est il y a un affichage dynamique complètement en CSS
Puis nous calcul la moyenne et on l'affiche. 
Et pour chaque utilisateur, on fait une boucle sur le nombre d'étoile qu'il a mis, ou on la colorer en jaune et le reste des étoiles on l'affiche sans couleur. 
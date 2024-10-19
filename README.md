# My Books

### Membres du groupe

MATHEVET Chris 
MARQUES Julian
Classe : TD 21

### Comandes

Pour installer toutes les dépendances
> `pip install -r .\requirements.txt`                                                                                       

Pour créer la BD 
> `flask loaddb myApp/data.yml`

Pour supprimer la BD
> `flask cleardb`

Pour lancer le site
> `flask run`

Pour ajouter un utilisateur
> `flask newuser <nom> <mdp>`

Pour changer le mdp d'un utilisateur
> `flask passwd <nom> <newmdp>`

### GITHUB
[Github](https://github.com/chris-mathevet/My-books)

### Utilisateurs par défaut
- roberto : roberto
- julian : marques
- chris : mathevet

### Fonctionnalités

- Lien entre les pages (dans le header, boutons lien cliquable...)
- Bouton login/signup + implémentation du login/signup
- Page avec tous les auteurs
    - Possibilité de voir un auteur individuel ( Page avec tous ses livres )
    - Editer le nom de l'auteur
    - Créer un nouvel auteur
- Barre de recherche
    - Renvoie sur une page recherche divisé en deux parties, livres et auteurs
- Page de favoris
    - On peut ajouter et supprimer un livre des favoris via la page "détail" d'un livre ( Bouton coeur )
    - Recommandations
- Commentaires de livres
    - Voir les commentaires des autres utilisateurs
    - Déposer un commentaire
    - Editer son commentaire
    - Supprimer son commentaire
- Ajout de note pour un livre
    - On peut voir les notes des utilisateurs dans la section des commentaires 
    - Note moyenne par livre par rapport aux notes des utilisateurs
- Redirection sur une page spécial lors d'erreur 404
- Page des livres ou auteurs
    - Affiche avec une limite de 10 que l'on peut augmenter (bouton Voir Plus)
- Voir le favoris des personnes qui ont commenté un livre (en cliquant sur leur nom)
- Footer avec le lien vers le github, le nom des développeurs

### Fonctionnalités expliquées

##### Recommandation  

Dans un premier temps, on récupère l'ensemble des auteurs des livres que l'utilisateur a mis en favoris.
Ensuite, on récupère l'ensemble des livres de ces auteurs que l'utilisateur n'a pas encore mis en favoris.
Et on prend un sample de 5 livres aléatoire dans cette liste de livres.

##### Search

Dans un premier temps, on récupère ce que l'utilisateur a entré et on fait une première liste avec les livres (Titre) / auteurs (Nom) qui commencent par l'entrée de l'utilisateur.
Et ensuite on y ajoute les livres (Titre) / auteurs (Nom) dans lesquels l'entrée est présente et que l'on n'a pas déjà ajoutés.

##### Moyenne note  

Chaque personne peut ajouter une note en plus d'un commentaire. La note est entre 0 et 5 sous-formes d'étoile qu'on peut sélectionner et il y a un affichage dynamique complètement en CSS
Puis nous calculons la moyenne et on l'affiche. 
Et pour chaque utilisateur, on fait une boucle sur le nombre d'étoile qu'il a mis, ou on la colore en jaune et le reste des étoiles on l'affiche sans couleur.

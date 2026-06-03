# MoleCool
Simulation simple des atomes, de leurs couches électroniques et des liaisons entre eux.

## Fonctions disponibles
- Création d'atomes avec un symbole et numéro atomique
- Afficher la configuration électronique (*avec les exceptions du tableau périodique!*)
- Ajout / retir d'électrons
- Avoir les électrons de valence
- Hybridation des couches électroniques
- Visualisation des molécules et composés ioniques avec *VPython*

## Comment utiliser les modules
D'abord, il faut installer les modules requis pour la visualisation des molécules avec:
```bash
pip install -r requirements.txt
```
Puis, il faut simplement mettre en marche le programme depuis `main.py`.
Des molécules exemplaires s'afficheront sur une fenêtre VPython.
Pour se déplacer en 3D:
- Click droit **OU** *CTRL* + click gauche &rarr; Tourner la caméra
- *SHIFT* + click gauche **OU** *ALT* + click gauche &rarr; Bouger la caméra
- Rouler la roue de souris &rarr; Contrôler le zoom
----
### Comment créer une molécule
1. Créer les atômes nécessaires à l'aide de la classe `Atome`.**

2. Créer une liste et la remplir de toutes les liaisons de la molécule
    <br></br>
    - Une liaison ionique est représentée avec un objet `LiaisonIonique`:\
    Fournissez d'abord l'*oxydant* (atôme qui donne ses électrons),
    puis le *réducteur* (atôme qui reçoit des électrons) et le nombre d'électrons échangés.
    <br></br>
    - Une liaison covalente est représentée avec un objet `LiaisonCovalente`.\
    Fournissez les deux atomes liées, puis le nombre de liaisons si il s'agit d'une double ou triple liaison.
    <br></br>

3. Utiliser la méthode statique `Liaison.appliquer(X)`, où `X` doit être votre liste de liaisons. **Cette méthode hybridera les orbitales et effectuera les échanges d'électrons au sein de votre molécule automatiquement.**

4. Créer un objet `MoleculeViewer` en fournissant l'atôme centrale de la molécule et la liste des liaisons. Une fenêtre VPython devrait apparaitre dès que le programme est exécuté.


##### Haha, I beat you victor
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
1. Créer les atômes nécessaires à l'aide de la classe `Atome`.

2. Créer un objet `Molecule` en lui fournissant le nom, puis l'atome centrique de la molécule. Ensuite, il faut lui renseigner toutes les liaisons dans la molécules, que ce soit dans le constructeur ou avec la méthode `ajouter_liaisons`. Finalement, il faut construire la molécule avec la méthode `construire`.
    <br></br>
    - Une liaison ionique est représentée avec un objet `LiaisonIonique`:\
    Fournissez d'abord l'*oxydant* (atôme qui donne ses électrons),
    puis le *réducteur* (atôme qui reçoit des électrons) et le nombre d'électrons échangés.
    <br></br>
    - Une liaison covalente est représentée avec un objet `LiaisonCovalente`.\
    Fournissez les deux atomes liées, puis le nombre de liaisons si il s'agit d'une double ou triple liaison.
    <br></br>

3. **Lorsque la molécule sera construite, les hybridations des orbitales et les échanges d'électrons au sein de votre molécule seront appliqués automatiquement.**

4. Utilisez la méthode `visualiser` sur votre molécule pour afficher sa géométrie moléculaire en 3D. Une fenêtre VPython devrait apparaitre dès que le programme est exécuté.


##### Haha, I beat you victor
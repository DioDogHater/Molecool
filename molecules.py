from __future__ import annotations
from types import NoneType

from atomes import Atome
from couches import *
from liaisons import *
from utilitees import formatter_molecule, perpendiculaire

import vpython as vp

class Molecule:
    """Facilite la représentation et l'utilisation d'une molécule."""
    # TODO: Ajouter un algorithme pour faire une structure de lewis avec la représentation texte de la molécule...

    def __init__(self, nom : str, centre : Atome, ls : list[Liaison] | None = None):
        """Construit la molécule.
        Args:
            nom (str) : Le nom de la molecule.
            centre (Atome) : L'atome centrale de la molécule
            ls (list[Liaison] | None) : La liste contenant toutes les liaisons de la molécule
            construire (bool) : Si True, construit la molécules directement"""
        if not isinstance(nom, str): raise TypeError("nom doit être un str")
        if not isinstance(centre, Atome): raise TypeError("centre doit être une Atome")
        if not isinstance(ls, (list, NoneType)): raise TypeError("ls doit être une list[Liaison] ou None")
        self.__nom : str = nom
        self.__atomes : set[Atome] = set()
        self.__centre : Atome = centre
        self.__ls : list[Liaison] = ls if ls else []
        self.__construite : bool = False
        for l in self.__ls:
            for a in (l.a, l.b): self.__atomes.add(a)
    
    @property
    def nom(self) -> str:
        return self.__nom

    @property
    def atomes(self) -> set[Atome]:
        """Les atomes présentes dans la molécule."""
        return self.__atomes
    
    @property
    def centre(self) -> Atome:
        """L'atome centrale de la molécule."""
        return self.__centre
    
    @property
    def liaisons(self) -> list[Liaison]:
        """Les liaisons présentes dans la molécule."""
        return self.__ls
    
    def ajouter_liaisons(self, *liaisons : Liaison | list[Liaison]) -> Molecule:
        """Ajoute des liaisons à la molécule.
        Args:
            *liaisons (Liaison | list[Liaison]) : Nombre variable d'arguments contenant les liaisons, ou des listes de liaisons.
        Returns:
            Molecule : La molécule elle-même"""
        if self.__construite: raise ValueError("La molécule a déjà été construite, il est impossible d'ajouter plus.")
        for l in liaisons:
            if isinstance(l, (list, tuple)):
                self.__ls.extend(l)
                for _l in l:
                    for a in (_l.a, _l.b): self.__atomes.add(a)
            else:
                self.__ls.append(l)
                for a in (l.a, l.b): self.__atomes.add(a)
            
        return self

    def construire(self) -> Molecule:
        """Construit la molécule entière.
        Returns:
            Molecule : La molécule elle-même"""
        if self.__construite: raise ValueError("La molécule a déjà été construite!")
        Liaison.appliquer(self.liaisons)
        self.__construite = True
        return self
    
    def visualiser(self, offset : vp.vector = vp.vector(0,0,0), titre : str | None = None) -> MoleculeViewer:
        """Crée un MoleculeViewer pour visualiser la molécule en 3D.
        Args:
            offset (vp.vector) : La position du centre de l'atome dans la scène en 3D.
            titre (str) : Le titre affiché sur la molécule. (le nom de la molécule par défaut)"""
        if not self.__construite: raise ValueError("La molécule doit être construite pour pouvoir s'afficher correctement.")
        return MoleculeViewer(self, offset, self.nom if titre is None else titre)
    
    def avoir_nbre_liaisons(self, atome : Atome) -> int:
        """Retourne le nombre de liaisons d'une atome.
        Args:
            atome (Atome) : L'atome concernée.
        Returns:
            int : Le nombre de liaisons que atome a."""
        return len([l for l in self.liaisons if l.a == atome or l.b == atome])
    
    def __str__(self) -> str:
        return formatter_molecule(self.nom)

    def __repr__(self) -> str: return str(self)

class MoleculeViewer:
    """Génère un modèle en VPython de la molécule"""

    # La taille proportionelle au réel rayon des atomes
    RAYON_SCALE : float = 0.35

    # Rayon des electrons et liaisons
    RAYON_AFFICHAGE : float = 0.01

    class InfoAtome:
        """Informations diverses sur une atome dans la molécule."""
        def __init__(self, atome : Atome, liaison : Liaison | None = None, position : vp.vector | None = None, centre : bool = False):
            self.centre : bool = centre
            self.position : vp.vector | None = position
            self.axis : vp.vector = vp.vector(0, 1, 0)
            self.liaisons : list[Liaison] = [liaison] if liaison else []
            if isinstance(atome.couches[-1], Hybride):
                self.__nbre_sterique : int | None = atome.couches[-1].type.value
            else:
                self.__nbre_sterique = None
        
        @property
        def nbre_sterique(self) -> int:
            if self.__nbre_sterique:
                return self.__nbre_sterique
            return len(self.liaisons)
        
        @property
        def doublets(self) -> int:
            if self.__nbre_sterique:
                return self.__nbre_sterique - len(self.liaisons)
            return 0

        def ajouter(self, liaison : Liaison):
            self.liaisons.append(liaison)
        
        def index(self, liaison : Liaison):
            try: return self.liaisons.index(liaison)
            except: raise ValueError(f"{liaison} not in {self.liaisons}")
    
    def avoir_axe(self, info : MoleculeViewer.InfoAtome, i : int, doublet : bool = False) -> vp.vector:
        """Donne l'axe dans lequel l'atome est situé par rapport à son atome central."""
        if info.nbre_sterique == 1 or info.nbre_sterique == 2:
            angle : float = vp.radians(180.0) * i
            axe : vp.vector = perpendiculaire(info.axis).rotate(angle)
        elif info.nbre_sterique == 3:
            angle : float = vp.radians(120.0) * i - vp.radians(60.0)
            axe : vp.vector = info.axis.rotate(angle, perpendiculaire(info.axis))
        elif info.nbre_sterique == 4:
            if not info.centre and not doublet: i += 1
            if i == 0:
                axe : vp.vector = -info.axis
            else:
                angle : float = vp.radians(120.0) * (i - 1)
                axe : vp.vector = perpendiculaire(info.axis)
                axe = (-info.axis).rotate(vp.radians(109.5), axe).rotate(angle, info.axis)
        elif info.nbre_sterique == 5:
            if not info.centre and not doublet: i += 1
            if i < 2:
                axe : vp.vector = info.axis * (1 if i == 0 else -1)
            else:
                angle : float = vp.radians(120.0) * (i - 2)
                axe : vp.vector = perpendiculaire(info.axis).rotate(angle, info.axis)
        elif info.nbre_sterique == 6:
            if not info.centre and not doublet: i += 1
            if i < 2:
                axe : vp.vector = info.axis * (1 if i == 0 else -1)
            else:
                angle : float = vp.radians(90.0) * (i - 2)
                axe : vp.vector = perpendiculaire(info.axis).rotate(angle, info.axis)
        elif info.nbre_sterique == 7:
            if not info.centre and not doublet: i += 1
            if i < 2:
                axe : vp.vector = info.axis * (1 if i == 0 else -1)
            else:
                angle : float = vp.radians(72.0) * (i - 2)
                axe : vp.vector = perpendiculaire(info).rotate(angle, info.axis)
        elif info.nbre_sterique == 8:
            if not info.centre and not doublet: i += 1
            if i < 4:
                axe_principal : vp.vector = info.axis.rotate(vp.radians(120.0), perpendiculaire(info.axis))
                angle : float = vp.radians(90.0) * i
                axe : vp.vector = info.axis.rotate(angle, axe_principal)
            else:
                axe_principal : vp.vector = info.axis.rotate(vp.radians(120.0), perpendiculaire(info.axis))
                axe : vp.vector = info.axis.rotate(vp.radians(60.0), perpendiculaire(info.axis))
                angle : float = vp.radians(90.0) * i + vp.radians(45.0)
                axe = axe.rotate(angle, axe_principal)
        else:
            raise Exception(f"Pas de position pour {info.liaisons}")
        return axe.norm()

    def trouver_position(self, atome : Atome, info2 : MoleculeViewer.InfoAtome = None, l : LiaisonCovalente = None):
        """Calcule la position des atomes depuis l'atome central avec la récursion."""
        info : MoleculeViewer.InfoAtome = self.atomes[atome]

        if info.position is None:
            if info2 is None:
                raise ValueError(f"InfoAtome doit être donné pour déterminer la position de {atome}")
            origine : vp.vector = info2.position
            info.axis = self.avoir_axe(info2, info2.index(l))
            info.position = info.axis * l.longueur + origine
        else:
            l = None

        for l_next in info.liaisons:
            a_next = l_next.a if l_next.b is atome else l_next.b
            if self.atomes[a_next].position is None:
                self.trouver_position(a_next, info, l_next)

    def trouver_doublet(self, atome : Atome, index : int) -> tuple[vp.vector, vp.vector]:
        """Donne la position du doublet d'électrons libres"""
        info : MoleculeViewer.InfoAtome = self.atomes[atome]
        axe = self.avoir_axe(info, len(info.liaisons) + index, doublet=True)
        axe2 = vp.vector(axe.y, -axe.x, 0).norm()
        pos = axe * (atome.rayon * self.RAYON_SCALE + Liaison.LONGUEUR_MOYENNE / 4) + info.position
        return pos, pos + axe2 * self.RAYON_AFFICHAGE

    def __init__(self, molecule : Molecule, offset : vp.vector = vp.vector(0,0,0), titre : str = ""):
        """Crée le modèle en VPython
        Args:
            molecule (Molecule) : La molecule à visualiser.
            offset (vector) : Le "offset" (décalage) du modèle par rapport à l'origine de la scène
            titre (str) : Le titre à placer en haut de la molécule en 3D"""
        if not isinstance(molecule, Molecule):
            raise TypeError("molecule doit être une Molecule")
        self.atomes      : dict[Atome, MoleculeViewer.InfoAtome] = {molecule.centre: MoleculeViewer.InfoAtome(molecule.centre, position=vp.vector(0,0,0), centre=True)}
        self.spheres     : list[vp.sphere] = []
        self.cylindres   : list[vp.cylinder] = []
        self.fleches     : list[vp.arrow] = []
        self.texte       : list[vp.label] = []
        self.titre       : str | None = titre
        
        for l in molecule.liaisons:
            for a in (l.a, l.b):
                if a in self.atomes:
                    self.atomes[a].ajouter(l)
                else:
                    self.atomes[a] = MoleculeViewer.InfoAtome(a, liaison=l)

        self.trouver_position(molecule.centre)

        for a in self.atomes:
            pos : vp.vector = self.atomes[a].position + offset
            self.texte.append(vp.label(pos=pos, text=f"{a}", box=False, opacity=0, color=vp.color.black))
            self.spheres.append(vp.sphere(pos=pos, radius=a.rayon * self.RAYON_SCALE, color=a.couleur))
            for i in range(self.atomes[a].doublets):
                pos1, pos2 = self.trouver_doublet(a, i)
                self.spheres.append(vp.sphere(pos=pos1 + offset, radius=self.RAYON_AFFICHAGE, color=a.couleur))
                self.spheres.append(vp.sphere(pos=pos2 + offset, radius=self.RAYON_AFFICHAGE, color=a.couleur))
        
        for l in molecule.liaisons:
            if isinstance(l, LiaisonIonique):
                a_pos, b_pos = self.atomes[l.a].position, self.atomes[l.b].position
                self.fleches.append(
                    vp.arrow(
                        pos=a_pos + offset,
                        axis=(b_pos-a_pos).norm() * ((b_pos-a_pos).mag - l.b.rayon * self.RAYON_SCALE),
                        round=True,  shaftwidth=self.RAYON_AFFICHAGE
                    )
                )
            elif isinstance(l, LiaisonCovalente):
                a_pos, b_pos = self.atomes[l.a].position, self.atomes[l.b].position
                self.cylindres.append(vp.cylinder(pos=a_pos+offset, axis=b_pos-a_pos, radius=self.RAYON_AFFICHAGE))
                if l.liens >= 2:
                    self.cylindres.append(vp.cylinder(pos=a_pos+offset+vp.vector(0,0.02,0), axis=b_pos-a_pos, radius=self.RAYON_AFFICHAGE))
                if l.liens == 3:
                    self.cylindres.append(vp.cylinder(pos=a_pos+offset-vp.vector(0,0.02,0), axis=b_pos-a_pos, radius=self.RAYON_AFFICHAGE))

        # Afficher le titre de la molécule
        if titre:
            max_y : float = max([s.pos.y - offset.y for s in self.spheres]) + 0.1
            self.texte.append(vp.text(pos=offset + vp.vector(0, max_y, 0), align="center", height=0.025, text=titre, emissive=True, billboard=True))

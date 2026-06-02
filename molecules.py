from __future__ import annotations
from atomes import Atome
from couches import *
from liaisons import *

import vpython as vp

class MoleculeViewer:
    """Génère un modèle en VPython de la molécule"""
    # Longueur moyenne d'une liaison
    LIAISON_MOYENNE : float = 0.15

    # La taille proportionelle au réel rayon des atomes
    RAYON_SCALE : float = 0.5

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
            axe : vp.vector = vp.vector(info.axis.y, -info.axis.x, 0).rotate(angle)
        elif info.nbre_sterique == 3:
            angle : float = vp.radians(120.0) * i - vp.radians(60.0)
            axe : vp.vector = info.axis.rotate(angle, vp.vector(info.axis.y, -info.axis.x, 0))
        elif info.nbre_sterique == 4:
            if not info.centre and not doublet: i += 1
            if i == 0:
                axe : vp.vector = -info.axis
            else:
                angle : float = vp.radians(120.0) * (i - 1)
                axe : vp.vector = vp.vector(info.axis.y, -info.axis.x, 0)
                axe = (-info.axis).rotate(vp.radians(109.5), axe).rotate(angle, info.axis)
        elif info.nbre_sterique == 5:
            if not info.centre and not doublet: i += 1
            if i < 2:
                axe : vp.vector = info.axis * (1 if i == 0 else -1)
            else:
                angle : float = vp.radians(120.0) * (i - 2)
                axe : vp.vector = vp.vector(info.axis.y, -info.axis.x, 0).rotate(angle, info.axis)
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
            info.position = info.axis * self.LIAISON_MOYENNE + origine
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
        pos = axe * (atome.rayon * self.RAYON_SCALE + self.LIAISON_MOYENNE / 4) + info.position
        angle = vp.radians(5)
        return pos.rotate(-angle, axe2), pos.rotate(angle, axe2)

    def __init__(self, centre : Atome, ls : list[Liaison], offset : vp.vector = vp.vector(0,0,0), titre : str = None):
        """Crée le modèle en VPython
        Args:
            centre (Atome) : L'atome centrale de la molécule
            ls (list[Liaison]) : Les liasons qui composent la molécule entière
            offset (vector) : Le "offset" (décalage) du modèle par rapport à l'origine de la scène
            titre (str) : Le titre à placer en haut de la molécule en 3D"""
        self.atomes      : dict[Atome, MoleculeViewer.InfoAtome] = {centre: MoleculeViewer.InfoAtome(centre, position=vp.vector(0,0,0), centre=True)}
        self.spheres     : list[vp.sphere] = []
        self.cylindres   : list[vp.cylinder] = []
        self.fleches     : list[vp.arrow] = []
        self.texte       : list[vp.label] = []
        self.titre       : str | None = titre
        
        for l in ls:
            for a in (l.a, l.b):
                if a in self.atomes:
                    self.atomes[a].ajouter(l)
                else:
                    self.atomes[a] = MoleculeViewer.InfoAtome(a, liaison=l)

        self.trouver_position(centre)

        for a in self.atomes:
            pos : vp.vector = self.atomes[a].position + offset
            self.texte.append(vp.label(pos=pos, text=f"{a}", box=False, border=1, opacity=0.2, color=vp.color.green))
            self.spheres.append(vp.sphere(pos=pos, radius=a.rayon * self.RAYON_SCALE))
            for i in range(self.atomes[a].doublets):
                pos1, pos2 = self.trouver_doublet(a, i)
                self.spheres.append(vp.sphere(pos=pos1 + offset, radius=self.RAYON_AFFICHAGE, color=vp.color.cyan))
                self.spheres.append(vp.sphere(pos=pos2 + offset, radius=self.RAYON_AFFICHAGE, color=vp.color.cyan))
        
        for l in ls:
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
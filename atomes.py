
from __future__ import annotations

from utilitees import superscript
from couches import *

class Atome:
    """Représente une atome selon le modèle quantique moderne."""

    def __init__(self, symbole : str, numero : int):
        """Crée une atome.
        Args:
            symbole (str) : Le symbole de l'atome (affichage seulement)
            numero (int) : Le numéro atomique de l'atome"""
        if not isinstance(symbole, str): raise TypeError("symbole doit être un str")
        if not isinstance(numero, int): raise TypeError("numero doit être un int")
        if numero <= 0: raise ValueError("numero doit être > 0")
        self.__symbole : str = symbole
        self.__numero : int = numero
        self.__couches : list[SousCouche] = []
        [self.ajouter_electron() for _ in range(numero)]
    
    @property
    def symbole(self) -> str:
        """Le symbole atomique."""
        return self.__symbole
    
    @property
    def numero(self) -> int:
        """Le numéro atomique."""
        return self.__numero
    
    @property
    def couches(self) -> list[SousCouche]:
        """Les sous-couches électroniques de l'atome."""
        return self.__couches
    
    @property
    def n_final(self) -> int:
        return max([c.n for c in self.couches])
    
    @property
    def rayon(self) -> float:
        """Le rayon atomique approximatif."""
        # Le calcul n'est toujours pas correct, mais je planifie
        # l'implantation d'un tableau périodique avec lequel on peut se réferrer
        n_corrige = [1.0, 2.0, 3.0, 3.7, 4.0, 4.2, 4.5]
        return (self.numero / n_corrige[self.n_final - 1]**2) * 0.0529
    
    @property
    def nbre_e(self) -> int:
        """Le nombre d'électrons dans l'atome."""
        return sum([c.nbre_e for c in self.couches])
    
    @property
    def charge(self) -> int:
        """La charge globale de l'atome (protons - électrons)."""
        return self.numero - self.nbre_e
    
    @property
    def electrons(self) -> list[Electron]:
        """Les électrons dans l'atome."""
        electrons : list[Electron] = []
        for c in self.couches:
            electrons.extend(c.electrons)
        electrons.sort(key = lambda a: a.n * 100 + a.l * 10 + a.m)
        return electrons
    
    @property
    def e_val(self) -> int:
        """Le nombre d'électrons de valence de l'atome."""
        n_max : int = max([c.n for c in self.couches])
        return sum([c.nbre_e for c in self.couches if c.n == n_max])
    
    @property
    def configuration(self) -> str:
        """La configuration électronique de l'atome, en texte."""
        return " ".join([str(c) for c in self.couches])
    
    def ajouter_electron(self) -> Electron:
        """Ajoute un électron à l'atome (avec les exceptions incluses)
        Returns:
            Electron : L'électron ajouté à l'atome."""
        EXCEPTIONS_S : dict[int, int] = {24: 4, 29: 4, 41: 5, 42: 5, 44: 5, 45: 5, 47: 5, 78: 6, 79: 6, 110: 7}
        EXCEPTIONS_F : dict[int, int] = {58: 4, 64: 4, 91: 5, 92: 5, 93: 5, 96: 5, 103: 5, }
        EXCEPTIONS_SKIP : dict[int, SPDF] = {46: SPDF(5, 0), 57: SPDF(4, 3), 89: SPDF(5, 3), 90: SPDF(5, 3), 103: SPDF(6, 1)}

        if len(self.couches) == 0:
            self.couches.append(SPDF(1, 0))
        elif (self.couches and self.couches[-1].nbre_e == self.couches[-1].e_max) or\
           (self.numero in EXCEPTIONS_S and self.couches[-1] == SPDF(EXCEPTIONS_S[self.numero], 0)) or\
           (self.numero in EXCEPTIONS_F and self.couches[-1] == SPDF(EXCEPTIONS_F[self.numero], 3) and self.nbre_e == self.numero - 1):
            nouveau : SPDF = SPDF.avoir_prochain(self.couches[-1])
            if not self.numero in EXCEPTIONS_SKIP or nouveau != EXCEPTIONS_SKIP[self.numero]:
                self.couches.append(nouveau)
        return self.couches[-1].ajouter_electron()
    
    def enlever_electron(self) -> bool:
        """Enlève un électron de l'atome.
        Returns:
            bool : Si la dernière sous-couche de l'atome n'a plus d'électrons"""
        if len(self.couches) == 0: raise ValueError("Pas d'é à enlever")
        dernier : SousCouche = self.couches[-1]
        if dernier.enlever_electron():
            self.couches.pop()
            return True
        return False
    
    def hybrider(self, sigma : int, pi : int) -> Hybride:
        """Applique l'hybridation.
        Args:
            sigma (int) : Le nombre de liaisons sigma
            pi (int) : Le nombre de liaisons pi
        Returns:
            Hybride : La sous-couche hybridée"""

        if not isinstance(sigma, int) or not isinstance(pi, int):
            raise TypeError("sigma et pi doivent être des int")
        if sigma <= 0 or pi < 0 or pi > sigma:
            raise ValueError(f"{sigma=} et {pi=} n'est pas valide")
        if sigma + pi > self.e_val:
            raise ValueError(f"Pas assez d'électrons de valence pour {sigma=} et {pi=} ({self.e_val}é de valence)")
        
        if self.numero == 1:
            if pi != 0: raise ValueError(f"Hydrogène ne peut faire qu'une liaison sigma ({sigma=}, {pi=})")
            return self.couches[0]

        n_final : int = max([c.n for c in self.couches])
        s : SPDF = None ; p : SPDF = None
        for c in self.couches[::-1]:
            if c.n == n_final and isinstance(c, SPDF):
                if c.l == 0: s = c
                elif c.l == 1: p = c
        
        if s is None or p is None:
            raise ValueError(f"Ne peut pas avoir de liaisons covalentes (s et/ou p manquant à n={n_final}):\n{self.configuration}")
        
        h = Hybride(self.couches[-1].n, sigma + (self.e_val - sigma - pi) // 2, self.e_val - pi)
        self.__couches.remove(s)
        self.__couches.remove(p)
        self.__couches.append(h)

        if pi > 0:
            self.__couches.append(SPDF(self.couches[-1].n, 1, pi))
        
        return h
    
    def __str__(self) -> str:
        texte : str = f"{self.symbole}"
        charge : int = self.charge
        if charge != 0: texte += f"{superscript(charge, True)}"
        return texte
    
    def __repr__(self) -> str: return str(self)
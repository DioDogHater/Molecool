from __future__ import annotations
from typing import Self
from abc import ABC, abstractmethod
from typing import override

from atomes import Atome
from couches import *

class Liaison(ABC):
    def __init__(self, a : Atome, b : Atome):
        super().__init__()
        if not isinstance(a, Atome) or not isinstance(b, Atome):
            raise TypeError("a et b doivent être des atomes")
        self.__a : Atome = a
        self.__b : Atome = b
    
    @property
    def a(self) -> Atome:
        return self.__a
    
    @property
    def b(self) -> Atome:
        return self.__b
    
    @staticmethod
    def appliquer(liaisons : list[Self]):
        """Applique les liaisons (ajoute les hybridations + échanges d'électrons)"""
        LiaisonIonique.appliquer(liaisons)
        LiaisonCovalente.appliquer(liaisons)

    @abstractmethod
    def __str__(self) -> str:
        pass

    def __repr__(self) -> str: return str(self)

class LiaisonIonique(Liaison):
    def __init__(self, anion : Atome, cation : Atome, electrons : int = 1):
        if not isinstance(electrons, int): raise TypeError("electrons doit être un int")
        if electrons <= 0: raise ValueError("electrons doit être > 0")
        self.__electrons : int = electrons
        super().__init__(anion, cation)
    
    @property
    def electrons(self) -> int:
        """Le nombre d'électrons transférés de a à b."""
        return self.__electrons
    
    @staticmethod
    @override
    def appliquer(liaisons : list[Liaison]):
        # Atome : é gagnés / perdus
        liens : dict[Atome, int] = {}

        for l in liaisons:
            if not isinstance(l, LiaisonIonique): continue
            if not l.a in liens: liens[l.a] = 0
            if not l.b in liens: liens[l.b] = 0
            liens[l.a] += l.electrons
            liens[l.b] -= l.electrons
        
        for a in liens:
            if liens[a] > 0: [a.enlever_electron() for _ in range(liens[a])]
            elif liens[a] < 0: [a.ajouter_electron() for _ in range(-liens[a])]
    
    @override
    def __str__(self) -> str:
        return f"{self.a.symbole} {self.electrons}é -> {self.b.symbole}"

class LiaisonCovalente(Liaison):
    def __init__(self, a : Atome, b : Atome, liens : int = 1):
        if not isinstance(liens, int): raise TypeError("liens doit être un int")
        if liens <= 0: raise ValueError("liens doit être > 0")
        self.__liens : int = liens
        super().__init__(a, b)
    
    @property
    def liens(self) -> int:
        """Le nombre de liaisons entre a et b."""
        return self.__liens
    
    @property
    def sigma(self) -> int:
        """Le nombre de liaisons sigma."""
        return 1
    
    @property
    def pi(self) -> int:
        """Le nombre de liaisons pi."""
        return self.liens - 1
    
    @staticmethod
    @override
    def appliquer(liaisons : list[Liaison]):
        # Atome : (liasons sigma, liasons pi)
        liens : dict[Atome, tuple[int, int]] = {}

        for l in liaisons:
            if not isinstance(l, LiaisonCovalente): continue
            if not l.a in liens: liens[l.a] = (0, 0)
            if not l.b in liens: liens[l.b] = (0, 0)
            liens[l.a] = (liens[l.a][0] + l.sigma, liens[l.a][1] + l.pi)
            liens[l.b] = (liens[l.b][0] + l.sigma, liens[l.b][1] + l.pi)
        
        for a in liens:
            a.hybrider(*liens[a])
    
    @override
    def __str__(self) -> str:
        SYMBOLES : list[str] = ["-","=","≡"]
        return f"{self.a.symbole}{SYMBOLES[self.liens - 1]}{self.b.symbole}"
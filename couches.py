from __future__ import annotations
from typing import Any
from enum import IntEnum
from abc import ABC, abstractmethod
from typing import override

from utilitees import superscript

class Electron:
    """Représente un électron selon le modèle quantique moderne."""

    def __init__(self, n : int, l : int, m : int, s : float) -> None:
        """Construit l'électron.
        Args:
            n (int) : Nombre quantique principal (niveau d'énergie)
            l (int) : Nombre quantique secondaire (sous-couche)
            """
        self.n = n
        self.l = l
        self.m = m
        self.s = s

    @property
    def n(self) -> int:
        """Nombre quantique principal.
        Indique l'énergie et dimension de l'orbitale."""
        return self.__n
    
    @n.setter
    def n(self, val : int):
        if not isinstance(val, int): raise TypeError("n doit être un int")
        if val <= 0:
            raise ValueError(f"Nombre quantique n={val} doit être supérieur à 0")
        self.__n : int = val

    @property
    def l(self) -> int:
        """Nombre quantique secondaire.
        Forme de l'orbitale dans laquelle se trouve l'électron."""
        return self.__l
    
    @property
    def type_orbitale(self) -> str:
        """Le type de l'orbitale (SPDF) dans laquelle se situe l'électron."""
        return SPDF.NOMS[self.l]
    
    @l.setter
    def l(self, val : int):
        if not isinstance(val, int): raise TypeError("l doit être un int")
        if val < 0 or val >= self.n:
            raise ValueError(f"Nombre quantique l={val} doit être entre [0, {self.n-1}]")
        self.__l : int = val
    
    @property
    def m(self) -> int:
        """L'orientation de l'orbitale dans laquelle se trouve l'électron."""
        return self.__m
    
    @m.setter
    def m(self, val : int):
        if not isinstance(val, int): raise TypeError("m doit être un int")
        if abs(val) > self.l:
            raise ValueError(f"Nombre quantique m={val} doit être entre [{-self.l}, {self.l}]")
        self.__m : int = val
    
    @property
    def s(self) -> float:
        """Nombre quantique de 'spin'.
        Soit -1/2, soit 1/2."""
        return self.__s
    
    @s.setter
    def s(self, val : float):
        if not isinstance(val, float): raise TypeError("s doit être un float")
        if abs(val) != 0.5:
            raise ValueError(f"Nombre quantique s={val} doit être soit -1/2, soit 1/2")
        self.__s : int = val

    def __repr__(self) -> str:
        return f"é(n={self.n}, l={self.l}, m={self.m:2}, s={"+½" if self.s > 0 else "-½"})"

class SousCouche(ABC):
    """Sous-couche électronique abstraite."""
    def __init__(self, n : int, electrons : int = 0):
        if not isinstance(n ,int) or not isinstance(electrons, int):
            raise TypeError("n et electrons doivent être des int")
        super().__init__()
        self.__n : int = n
        self._electrons : list[Electron] = []
        [self.ajouter_electron() for _ in range(electrons)]
    
    @property
    def n(self) -> int:
        """Le nombre quantique principal de la couche."""
        return self.__n
    
    @property
    def electrons(self) -> list[Electron]:
        """Les électrons dans la sous-couche."""
        return self._electrons
    
    @property
    def nbre_e(self) -> int:
        """Le nombre d'électrons dans la sous-couche."""
        return len(self.electrons)
    
    @property
    @abstractmethod
    def e_max(self) -> int:
        """Le nombre maximal d'électrons qui peuvent être dans la sous-couche"""
        pass

    @property
    @abstractmethod
    def orbitales(self) -> int:
        """Le nombre d'orbitales dans la sous-couche."""
        pass

    @abstractmethod
    def ajouter_electron(self) -> Electron:
        pass
    
    def enlever_electron(self) -> bool:
        """Enlève un électron à la sous-couche.
        Returns:
            bool : Si la couche est vidée d'électrons, retourne True"""
        if self.nbre_e == 0:
            raise ValueError(f"Il n'y plus d'électrons à enlever dans la sous-couche électronique")
        self._electrons.pop()
        return self.nbre_e == 0

    @abstractmethod
    def __str__(self) -> str:
        pass

    def __repr__(self) -> str: return str(self)

    @abstractmethod
    def __eq__(self, other : Any) -> bool:
        pass

class SPDF(SousCouche):
    """Sous-couche électronique s, p, d, f ou g."""
    NOMS = ["s", "p", "d", "f", "g"]

    def __init__(self, n : int, l : int, electrons : int = 0):
        """Construit la sous-couche s, p, d, f ou g.
        Args:
            n (int) : Le nombre quantique principal de la couche où se situe la sous-couche
            l (int) : Le type de couche selon s=0, p=1, d=2, f=3, g=4"""
        if not isinstance(l, int): raise TypeError("l doit être un int")
        if l < 0 or l >= n: raise ValueError("l doit être entre [0, n-1]")
        self.__l : int = l
        super().__init__(n, electrons)
    
    @staticmethod
    def avoir_prochain(couche : SPDF) -> SPDF:
        """Donne la prochaine sous-couche spdf selon la dernière."""
        if couche.l == 0:
            return SPDF(couche.n - (couche.n // 2 - 1), couche.n // 2)
        return SPDF(couche.n + 1, couche.l - 1)
    
    @property
    def l(self) -> int:
        """Le nombre quantique secondaire."""
        return self.__l

    @property
    @override
    def e_max(self) -> int:
        return 4 * self.l + 2

    @property
    @override
    def orbitales(self) -> int:
        return 2 * self.l + 1

    @override
    def ajouter_electron(self) -> Electron:
        if self.nbre_e == self.e_max:
            raise ValueError(f"La sous-couche électronique est pleine (é_max={self.e_max})")
        e = Electron(self.n, self.l, -self.l + self.nbre_e % self.orbitales, +0.5 if self.nbre_e < self.orbitales else -0.5)
        self._electrons.append(e)
        return e
    
    @override
    def __str__(self) -> str:
        return f"{self.n}{SPDF.NOMS[self.l]}{superscript(self.nbre_e)}"
    
    def __repr__(self) -> str: return str(self)
    
    @override
    def __eq__(self, other : Any) -> bool:
        if not isinstance(other, SPDF): return False
        return self.n == other.n and self.l == other.l

class Hybridation(IntEnum):
    sp      = 2
    sp2     = 3
    sp3     = 4
    sp3d    = 5
    sp3d2   = 6
    sp3d3   = 7
    sp3d4   = 8

class Hybride(SousCouche):
    """Représente une sous-couche hybridée."""
    TYPES = [x for x in Hybridation]

    def __init__(self, n : int, nbre_sterique : int, electrons : int = 0):
        """Génère une sous-couche hybride selon le nombre stérique.
        Args:
            nbre_sterique (int) : Le nombre stérique
            electrons (int) : Le nombre d'électrons dans la couche hybridée."""
        if not isinstance(nbre_sterique, int): raise TypeError("nbre_sterique doit être un int")
        if nbre_sterique > 8: raise ValueError("Nombre stérique > 8 n'est pas pas supporté")

        self.__type : Hybridation = Hybride.TYPES[nbre_sterique - 2]
        if electrons > self.e_max: raise ValueError(f"Trop d'électrons dans la couche {self}")
        super().__init__(n, electrons)
    
    @property
    def type(self) -> Hybridation:
        """Le type de sous-couche hybridée."""
        return self.__type

    @property
    @override
    def e_max(self) -> int:
        return self.__type.value * 2

    @property
    @override
    def orbitales(self) -> int:
        return self.__type.value
    
    @override
    def ajouter_electron(self) -> Electron:
        if self.nbre_e == self.e_max:
            raise ValueError(f"La sous-couche électronique est pleine (é_max={self.e_max})")
        if self.nbre_e < 2:
            e = Electron(self.n, 0, 0, +0.5 if self.nbre_e == 0 else -0.5)
        elif self.nbre_e < 8:
            e = Electron(self.n, 1, -2 + self.nbre_e // 2, +0.5 if self.nbre_e % 2 == 0 else -0.5)
        else:
            e = Electron(self.n, 2, -2 + self.nbre_e // 2, +0.5 if self.nbre_e % 2 == 0 else -0.5)
        self._electrons.append(e)
        return e

    @override
    def __str__(self) -> str:
        return f"{self.n}({self.type.name}){superscript(self.nbre_e)}"
    
    @override
    def __eq__(self, other : Any) -> bool:
        if not isinstance(other, Hybride): return False
        return self.n == other.n and self.type == other.type

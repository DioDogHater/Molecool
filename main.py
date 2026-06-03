from atomes import Atome
from liaisons import *
from molecules import MoleculeViewer, vp

from utilitees import formatter_molecule

offset = vp.vector(0,0,0)

# Examples de molécules
def H2O():
    global offset

    h1 = Atome("H")
    h2 = Atome("H")
    o = Atome("O")
    ls1 : list[Liaison] = [LiaisonCovalente(o, h1), LiaisonCovalente(o, h2)]
    Liaison.appliquer(ls1)
    print(o.configuration)
    
    mv = MoleculeViewer(o, ls1, offset, titre="H2O")
    print(formatter_molecule(mv.titre))
    offset += vp.vector(1, 0, 0)

def MgCl2():
    global offset

    mg = Atome("Mg")
    cl1 = Atome("Cl")
    cl2 = Atome("Cl")
    ls2 : list[Liaison] = [LiaisonIonique(mg, cl1), LiaisonIonique(mg, cl2)]
    Liaison.appliquer(ls2)

    mv = MoleculeViewer(mg, ls2, offset, titre="MgCl2")
    print(formatter_molecule(mv.titre))
    offset += vp.vector(1, 0, 0)

# CH3NHCH3
def CH3NHCH3():
    global offset

    hs = [Atome("H") for _ in range(7)]
    cs = [Atome("C"), Atome("C")]
    n  = Atome("N")
    ls3 : list[Liaison] = [LiaisonCovalente(n, hs[3]), LiaisonCovalente(n, cs[0]), LiaisonCovalente(n, cs[1])]
    ls3.extend([LiaisonCovalente(cs[1], h) for h in hs[-3:]])
    ls3.extend([LiaisonCovalente(cs[0], h) for h in hs[:3]])
    Liaison.appliquer(ls3)

    mv = MoleculeViewer(n, ls3, titre="CH3NHCH3")
    print(formatter_molecule(mv.titre))
    offset += vp.vector(1, 0, 0)

# C2H4
def C2H4():
    global offset

    cs = [Atome("C"), Atome("C")]
    hs = [Atome("H") for _ in range(4)]
    ls4 : list[Liaison] = [LiaisonCovalente(cs[x // 2], hs[x]) for x in range(4)] + [LiaisonCovalente(cs[0], cs[1], 2)]
    Liaison.appliquer(ls4)

    mv = MoleculeViewer(cs[1], ls4, offset, titre="C2H4")
    print(formatter_molecule(mv.titre))
    offset += vp.vector(1, 0, 0)

def main():
    vp.scene.ambient = vp.color.gray(0.5)

    CH3NHCH3()
    C2H4()
    MgCl2()
    H2O()


# Garde le programme ouvert
if __name__ == "__main__":
    print("Appuyez sur CTRL+C ou fermez la page VPython pour terminer.")
    main()
    try:
        while True:
            vp.rate(60)
    except KeyboardInterrupt:
        exit(0)
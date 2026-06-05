from atomes import Atome
from liaisons import *
from molecules import *

# Permet d'afficher plusieurs molécules une à côté de l'autre
offset = vp.vector(0,0,0)

# Examples de molécules
def H2O():
    global offset

    h1 = Atome("H")
    h2 = Atome("H")
    o = Atome("O")
    h2o = Molecule("H2O", o,
                    [LiaisonCovalente(o, h1), LiaisonCovalente(o, h2)]) \
          .construire()

    print(o.configuration)
    
    h2o.visualiser(offset)
    print(h2o)
    offset += vp.vector(1, 0, 0)

def MgCl2():
    global offset

    mg = Atome("Mg")
    cl1 = Atome("Cl")
    cl2 = Atome("Cl")
    mgcl2 = Molecule("MgCl2", mg,
                    [LiaisonIonique(mg, cl1), LiaisonIonique(mg, cl2)]) \
            .construire()

    mgcl2.visualiser(offset)
    print(mgcl2)
    offset += vp.vector(1, 0, 0)

# CH3NHCH3
def CH3NHCH3():
    global offset

    hs = [Atome("H") for _ in range(7)]
    cs = [Atome("C"), Atome("C")]
    n  = Atome("N")
    ch3nhch3 = Molecule("CH3NHCH3", n) \
        .ajouter_liaisons(LiaisonCovalente(n, hs[3]), LiaisonCovalente(n, cs[0]), LiaisonCovalente(n, cs[1])) \
        .ajouter_liaisons([LiaisonCovalente(cs[1], h) for h in hs[-3:]]) \
        .ajouter_liaisons([LiaisonCovalente(cs[0], h) for h in hs[:3]]) \
        .construire()

    ch3nhch3.visualiser(offset)
    print(ch3nhch3)
    offset += vp.vector(1, 0, 0)

# C2H4
def C2H4():
    global offset

    cs = [Atome("C"), Atome("C")]
    hs = [Atome("H") for _ in range(4)]
    c2h4 = Molecule("C2H4", cs[0]) \
        .ajouter_liaisons([LiaisonCovalente(cs[x // 2], hs[x]) for x in range(4)]) \
        .ajouter_liaisons(LiaisonCovalente(cs[0], cs[1], 2)) \
        .construire()

    c2h4.visualiser(offset)
    print(c2h4)
    offset += vp.vector(1, 0, 0)

def main():
    # Change l'intensité de la lumière ambiente
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
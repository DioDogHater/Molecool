def superscript(exposant : int, signe_obligatoire : bool = False) -> str:
    """Donne la version texte 'superscript' (comme un exposant) d'un nombre.
    Args:
        nombre (int) : Le nombre à transformer en superscript
        sign_obligatoire (bool) : Si mis à True, ajoute un + devant les nombre positifs
    Returns:
        str : La version superscript du nombre"""
    superscripts : str = "⁰¹²³⁴⁵⁶⁷⁸⁹"
    signe : str = ""

    if exposant < 0:
        signe = "⁻"
        exposant = -exposant
    elif exposant != 0 and signe_obligatoire:
        signe = "⁺"

    if exposant >= 10:
        return signe + superscript(exposant // 10) + superscripts[exposant % 10]
    return signe +  superscripts[exposant]

def subscript(nombre : int, signe_obligatoire : bool = False) -> str:
    """Donne la version texte 'subscript' (petite et en bas) d'un nombre.
    Args:
        nombre (int) : Le nombre à transformer en subscript
        sign_obligatoire (bool) : Si mis à True, ajoute un + devant les nombre positifs
    Returns:
        str : La version subscript du nombre"""
    subscripts : str = "₀₁₂₃₄₅₆₇₈₉"
    signe : str = ""

    if nombre < 0:
        signe = "₋"
        nombre = -nombre
    elif nombre != 0 and signe_obligatoire:
        signe = "₊"

    if nombre >= 10:
        return signe + subscript(nombre // 10) + subscripts[nombre % 10]
    return signe + subscripts[nombre]

def formatter_molecule(molecule : str) -> str:
    """Va remplacer les nombre dans une molécule par des nombres 'subscript'
    Args:
        molecule (str) : La forme moléculaire en texte.
    Returns:
        str : La molécule avec des nombre 'subscript'
    Example:
    >>> formatter_molecule("CH3NHCH3")
    = "CH₃NHCH₃"""""
    resultat : str = ""
    for c in molecule:
        if c.isdigit():
            resultat += subscript(int(c))
        else:
            resultat += c
    return resultat
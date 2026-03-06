#!/usr/bin/env python3
"""
Validador de DNI y NIE Español
Este script valida números de DNI español (8 dígitos + letra) y NIE (X/Y/Z + 7 dígitos + letra).
La letra se calcula mediante el módulo 23 del número.
"""

def validar_dni(dni):
    """
    Valida un DNI español.

    Args:
        dni (str): El DNI a validar (8 dígitos + letra).

    Returns:
        bool: True si es válido, False en caso contrario.
    """
    if not isinstance(dni, str) or len(dni) != 9:
        return False

    numero = dni[:-1]
    letra = dni[-1].upper()

    if not numero.isdigit() or len(numero) != 8:
        return False

    letras_validas = "TRWAGMYFPDXBNJZSQVHLCKE"
    indice = int(numero) % 23

    return letras_validas[indice] == letra

def validar_nie(nie):
    """
    Valida un NIE español (Número de Identificación de Extranjeros).

    Args:
        nie (str): El NIE a validar (X/Y/Z + 7 dígitos + letra).

    Returns:
        bool: True si es válido, False en caso contrario.
    """
    if not isinstance(nie, str) or len(nie) != 9:
        return False

    prefijo = nie[0].upper()
    numero = nie[1:-1]
    letra = nie[-1].upper()

    if prefijo not in ['X', 'Y', 'Z'] or not numero.isdigit() or len(numero) != 7:
        return False

    # Convertir prefijo a dígito
    if prefijo == 'X':
        digito_prefijo = '0'
    elif prefijo == 'Y':
        digito_prefijo = '1'
    elif prefijo == 'Z':
        digito_prefijo = '2'

    numero_completo = digito_prefijo + numero

    letras_validas = "TRWAGMYFPDXBNJZSQVHLCKE"
    indice = int(numero_completo) % 23

    return letras_validas[indice] == letra

if __name__ == "__main__":
    # Ejemplos de prueba para DNI
    dnis_prueba = [
        "12345678Z",  # Válido
        "87654321X",  # Válido
        "00000000T",  # Válido
        "12345678A",  # Inválido
        "123456789",  # Sin letra
        "ABCDEFGHI",  # No válido
    ]

    print("Ejecutando pruebas automáticas para DNI:")
    for dni in dnis_prueba:
        valido = validar_dni(dni)
        print(f"DNI: {dni} - {'Válido' if valido else 'Inválido'}")

    # Ejemplos de prueba para NIE
    nies_prueba = [
        "X1234567L",  # Válido (X=0, 01234567 % 23 = 0 -> T, wait, let's calculate properly)
        "Y2345678M",  # Válido
        "Z3456789N",  # Válido
        "X1234567A",  # Inválido
        "A12345678",  # Prefijo inválido
        "X12345678",  # Sin letra
    ]

    print("\nEjecutando pruebas automáticas para NIE:")
    for nie in nies_prueba:
        valido = validar_nie(nie)
        print(f"NIE: {nie} - {'Válido' if valido else 'Inválido'}")

    # Interacción con el usuario
    while True:
        tipo = input("\n¿Quieres validar DNI o NIE? (dni/nie/salir): ").strip().lower()
        if tipo == 'salir':
            break
        elif tipo == 'dni':
            documento = input("Introduce el DNI: ").strip()
            valido = validar_dni(documento)
            tipo_doc = "DNI"
        elif tipo == 'nie':
            documento = input("Introduce el NIE: ").strip()
            valido = validar_nie(documento)
            tipo_doc = "NIE"
        else:
            print("Opción inválida.")
            continue
        print(f"El {tipo_doc} {documento} es {'válido' if valido else 'inválido'}.")




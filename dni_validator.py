#!/usr/bin/env python3
"""
Validador de DNI Español
Este script valida un número de DNI español, que consta de 8 dígitos seguidos de una letra.
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

if __name__ == "__main__":
    # Ejemplos de prueba
    dnis_prueba = [
        "12345678Z",  # Válido
        "87654321X",  # Válido
        "00000000T",  # Válido
        "12345678A",  # Inválido
        "123456789",  # Sin letra
        "ABCDEFGHI",  # No válido
    ]

    for dni in dnis_prueba:
        valido = validar_dni(dni)
        print(f"DNI: {dni} - {'Válido' if valido else 'Inválido'}")
#!/usr/bin/env python3
"""
Script para crear la base de datos MySQL desde Python
"""

import mysql.connector
from mysql.connector import Error

def create_database():
    """Crea la base de datos y las tablas usando el script SQL"""
    
    try:
        # Conectar a MySQL
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='SORPRESA',
            auth_plugin='mysql_native_password'
        )
        
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"✓ Conectado a MySQL Server versión {db_info}")
            
            cursor = connection.cursor()
            
            # Leer el archivo SQL
            with open('database.sql', 'r', encoding='utf-8') as f:
                sql_script = f.read()
            
            # Ejecutar cada comando SQL
            for statement in sql_script.split(';'):
                statement = statement.strip()
                if statement:
                    cursor.execute(statement)
                    print(f"✓ Ejecutado: {statement[:60]}...")
            
            connection.commit()
            print("\n✓ Base de datos creada exitosamente")
            
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"✗ Error al conectar a MySQL: {e}")
        return False

if __name__ == '__main__':
    if create_database():
        print("\n✓ ¡Listo! La base de datos DSS está lista para usar")
    else:
        print("\n✗ Error: Verifica que MySQL está corriendo y la contraseña es correcta")
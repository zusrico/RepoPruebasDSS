#!/usr/bin/env python3
"""
Backend Flask para DSS - Diseño de Sistemas Software
Conecta la aplicación web con la base de datos MySQL
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Inicializar Flask
app = Flask(__name__)
CORS(app)

# Configuración de MySQL
DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', 'password'),
    'database': os.getenv('MYSQL_DB', 'dss_project'),
    'auth_plugin': 'mysql_native_password'
}

def get_db_connection():
    """Crea una conexión a MySQL"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# ==================== RUTAS DE USUARIOS ====================

@app.route('/api/users', methods=['GET'])
def get_users():
    """Obtiene la lista de todos los usuarios"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'status': 'error', 'message': 'No se pudo conectar a la base de datos'}), 500
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT id, username, email, full_name, university FROM users')
        users = cursor.fetchall()
        cursor.close()
        connection.close()
        
        return jsonify({'status': 'success', 'data': users}), 200
    except Error as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Obtiene los detalles de un usuario específico"""
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT id, username, email, full_name, university FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()
        cursor.close()
        
        if user:
            return jsonify({'status': 'success', 'data': user}), 200
        return jsonify({'status': 'error', 'message': 'Usuario no encontrado'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/users', methods=['POST'])
def create_user():
    """Crea un nuevo usuario"""
    try:
        data = request.json
        
        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO users (username, email, password, full_name, university)
            VALUES (%s, %s, %s, %s, %s)
        ''', (data['username'], data['email'], data['password'], data['full_name'], data.get('university')))
        
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'status': 'success', 'message': 'Usuario creado correctamente'}), 201
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400


# ==================== RUTAS DE PROYECTOS ====================

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """Obtiene la lista de todos los proyectos"""
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''
            SELECT p.id, p.user_id, p.title, p.description, p.category, p.status, 
                   p.created_at, u.username
            FROM projects p
            JOIN users u ON p.user_id = u.id
            ORDER BY p.created_at DESC
        ''')
        projects = cursor.fetchall()
        cursor.close()
        return jsonify({'status': 'success', 'data': projects}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/projects', methods=['POST'])
def create_project():
    """Crea un nuevo proyecto"""
    try:
        data = request.json
        
        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO projects (user_id, title, description, category, status)
            VALUES (%s, %s, %s, %s, %s)
        ''', (data['user_id'], data['title'], data.get('description'), 
              data.get('category'), data.get('status', 'En Progreso')))
        
        mysql.connection.commit()
        project_id = cursor.lastrowid
        cursor.close()
        
        return jsonify({'status': 'success', 'message': 'Proyecto creado', 'project_id': project_id}), 201
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """Obtiene los detalles de un proyecto"""
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''
            SELECT p.*, u.username
            FROM projects p
            JOIN users u ON p.user_id = u.id
            WHERE p.id = %s
        ''', (project_id,))
        project = cursor.fetchone()
        cursor.close()
        
        if project:
            return jsonify({'status': 'success', 'data': project}), 200
        return jsonify({'status': 'error', 'message': 'Proyecto no encontrado'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    """Actualiza un proyecto existente"""
    try:
        data = request.json
        
        cursor = mysql.connection.cursor()
        cursor.execute('''
            UPDATE projects 
            SET title = %s, description = %s, category = %s, status = %s
            WHERE id = %s
        ''', (data.get('title'), data.get('description'), data.get('category'), 
              data.get('status'), project_id))
        
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'status': 'success', 'message': 'Proyecto actualizado'}), 200
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400


# ==================== RUTAS DE VALIDACIÓN DE DOCUMENTOS ====================

@app.route('/api/validate-document', methods=['POST'])
def validate_document():
    """Valida un documento (DNI/NIE) y lo almacena en la BD"""
    try:
        from dni_validator import validar_dni, validar_nie
        
        data = request.json
        document_type = data['document_type'].upper()
        document_number = data['document_number'].upper()
        user_id = data.get('user_id')
        
        # Validar el documento
        if document_type == 'DNI':
            is_valid = validar_dni(document_number)
        elif document_type == 'NIE':
            is_valid = validar_nie(document_number)
        else:
            return jsonify({'status': 'error', 'message': 'Tipo de documento no válido'}), 400
        
        # Guardar en la base de datos
        if user_id:
            cursor = mysql.connection.cursor()
            cursor.execute('''
                INSERT INTO document_validations (user_id, document_type, document_number, is_valid)
                VALUES (%s, %s, %s, %s)
            ''', (user_id, document_type, document_number, is_valid))
            mysql.connection.commit()
            cursor.close()
        
        return jsonify({
            'status': 'success', 
            'document_type': document_type,
            'document_number': document_number,
            'is_valid': is_valid,
            'message': f'Documento válido' if is_valid else 'Documento inválido'
        }), 200
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/documents/<int:user_id>', methods=['GET'])
def get_user_documents(user_id):
    """Obtiene los documentos validados de un usuario"""
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''
            SELECT * FROM document_validations 
            WHERE user_id = %s
            ORDER BY validated_at DESC
        ''', (user_id,))
        documents = cursor.fetchall()
        cursor.close()
        return jsonify({'status': 'success', 'data': documents}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ==================== RUTAS DE ESTADÍSTICAS ====================

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Obtiene estadísticas generales del proyecto"""
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Total de usuarios
        cursor.execute('SELECT COUNT(*) as total_users FROM users')
        total_users = cursor.fetchone()['total_users']
        
        # Total de proyectos
        cursor.execute('SELECT COUNT(*) as total_projects FROM projects')
        total_projects = cursor.fetchone()['total_projects']
        
        # Proyectos por estado
        cursor.execute('''
            SELECT status, COUNT(*) as count 
            FROM projects 
            GROUP BY status
        ''')
        projects_by_status = cursor.fetchall()
        
        # Total de validaciones
        cursor.execute('SELECT COUNT(*) as total_validations FROM document_validations')
        total_validations = cursor.fetchone()['total_validations']
        
        cursor.close()
        
        return jsonify({
            'status': 'success',
            'data': {
                'total_users': total_users,
                'total_projects': total_projects,
                'projects_by_status': projects_by_status,
                'total_validations': total_validations
            }
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ==================== RUTAS DE SALUD ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verifica el estado de la API"""
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT 1')
        cursor.close()
        return jsonify({'status': 'success', 'message': 'API y base de datos funcionando correctamente'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error de conexión: {str(e)}'}), 500


# ==================== MANEJO DE ERRORES ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'status': 'error', 'message': 'Ruta no encontrada'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'status': 'error', 'message': 'Error interno del servidor'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
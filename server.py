#!/usr/bin/env python3
"""
Backend Flask Simplificado para DSS
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', 'password'),
    'database': os.getenv('MYSQL_DB', 'dss_project'),
    'auth_plugin': 'mysql_native_password'
}

def get_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"Error: {e}")
        return None

@app.route('/api/health', methods=['GET'])
def health():
    conn = get_connection()
    if conn:
        conn.close()
        return jsonify({'status': 'success', 'message': 'API funcionando'}), 200
    return jsonify({'status': 'error', 'message': 'Error BD'}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_connection()
    if not conn:
        return jsonify({'status': 'error'}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, username, email, full_name FROM users LIMIT 10')
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({'status': 'success', 'data': users}), 200

@app.route('/api/statistics', methods=['GET'])
def get_stats():
    conn = get_connection()
    if not conn:
        return jsonify({'status': 'error'}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT COUNT(*) as total FROM users')
    total_users = cursor.fetchone()['total']
    cursor.execute('SELECT COUNT(*) as total FROM projects')
    total_projects = cursor.fetchone()['total']
    cursor.close()
    conn.close()
    return jsonify({'status': 'success', 'data': {'users': total_users, 'projects': total_projects}}), 200

if __name__ == '__main__':
    print("\n" + "="*50)
    print("DSS - Diseño de Sistemas Software")
    print("="*50)
    print("✓ Backend Flask iniciando...")
    print(f"✓ Base de datos: {DB_CONFIG['database']}")
    print(f"✓ Servidor: http://localhost:5000")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
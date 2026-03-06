-- Base de datos para el proyecto DSS
-- Diseño de Sistemas Software

CREATE DATABASE IF NOT EXISTS dss_project;
USE dss_project;

-- Tabla de Usuarios (Estudiantes)
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    university VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla de Proyectos/Prácticas
CREATE TABLE projects (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    status ENUM('En Progreso', 'Completado', 'En Revisión') DEFAULT 'En Progreso',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabla de Validaciones de Documentos (DNI/NIE)
CREATE TABLE document_validations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    document_type ENUM('DNI', 'NIE') NOT NULL,
    document_number VARCHAR(20) NOT NULL,
    is_valid BOOLEAN,
    validated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabla de Estadísticas/Analytics
CREATE TABLE activity_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    action VARCHAR(100),
    resource_type VARCHAR(50),
    resource_id INT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Tabla de Comentarios/Feedback
CREATE TABLE comments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    user_id INT NOT NULL,
    comment_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabla de Archivos/Recursos
CREATE TABLE project_files (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500),
    file_type VARCHAR(50),
    file_size INT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- Tabla de Notificaciones
CREATE TABLE notifications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(200),
    message TEXT,
    notification_type VARCHAR(50),
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Índices para optimizar búsquedas
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_project_user ON projects(user_id);
CREATE INDEX idx_comment_project ON comments(project_id);
CREATE INDEX idx_activity_user ON activity_logs(user_id);
CREATE INDEX idx_document_user ON document_validations(user_id);
CREATE INDEX idx_file_project ON project_files(project_id);
CREATE INDEX idx_notification_user ON notifications(user_id);

-- Insertar datos de ejemplo
INSERT INTO users (username, email, password, full_name, university) VALUES
('zusrico', 'jesus.garcia@universidad.edu', 'hashed_password_1', 'Jesús García Sánchez', 'Universidad de Jerez'),
('estudiante1', 'estudiante1@universidad.edu', 'hashed_password_2', 'Juan Pérez López', 'Universidad de Jerez'),
('estudiante2', 'estudiante2@universidad.edu', 'hashed_password_3', 'María González García', 'Universidad de Jerez');

INSERT INTO projects (user_id, title, description, category, status) VALUES
(1, 'Validador de DNI/NIE', 'Sistema de validación de documentos españoles', 'Validación', 'Completado'),
(1, 'Dashboard de Análisis', 'Dashboard interactivo para análisis de datos', 'Análisis', 'En Progreso'),
(2, 'Predicción de Tendencias', 'Modelo predictivo usando machine learning', 'Análisis', 'En Progreso'),
(3, 'Optimización de Recursos', 'Algoritmo de optimización de recursos', 'Optimización', 'En Revisión');

INSERT INTO document_validations (user_id, document_type, document_number, is_valid) VALUES
(1, 'DNI', '12345678Z', TRUE),
(2, 'NIE', 'X1234567L', TRUE),
(3, 'DNI', '87654321X', TRUE);
/**
 * API Client para DSS - Diseño de Sistemas Software
 * Cliente JavaScript para comunicarse con el backend Flask
 */

class DSSAPIClient {
    constructor(baseURL = 'http://localhost:5000') {
        this.baseURL = baseURL;
        this.headers = {
            'Content-Type': 'application/json'
        };
    }

    /**
     * Método auxiliar para hacer peticiones
     */
    async request(endpoint, method = 'GET', data = null) {
        const url = `${this.baseURL}${endpoint}`;
        const options = {
            method: method,
            headers: this.headers
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(url, options);
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.message || `Error ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // ==================== USUARIOS ====================

    async getUsers() {
        return this.request('/api/users');
    }

    async getUser(userId) {
        return this.request(`/api/users/${userId}`);
    }

    async createUser(userData) {
        return this.request('/api/users', 'POST', userData);
    }

    // ==================== PROYECTOS ====================

    async getProjects() {
        return this.request('/api/projects');
    }

    async getProject(projectId) {
        return this.request(`/api/projects/${projectId}`);
    }

    async createProject(projectData) {
        return this.request('/api/projects', 'POST', projectData);
    }

    async updateProject(projectId, projectData) {
        return this.request(`/api/projects/${projectId}`, 'PUT', projectData);
    }

    // ==================== VALIDACIÓN DE DOCUMENTOS ====================

    async validateDocument(documentType, documentNumber, userId = null) {
        const data = {
            document_type: documentType,
            document_number: documentNumber
        };
        if (userId) {
            data.user_id = userId;
        }
        return this.request('/api/validate-document', 'POST', data);
    }

    async getUserDocuments(userId) {
        return this.request(`/api/documents/${userId}`);
    }

    // ==================== ESTADÍSTICAS ====================

    async getStatistics() {
        return this.request('/api/statistics');
    }

    // ==================== SALUD ====================

    async checkHealth() {
        return this.request('/api/health');
    }
}

// Crear instancia global del cliente
const dssAPI = new DSSAPIClient();

/**
 * Ejemplos de uso:
 * 
 * // Obtener todos los usuarios
 * dssAPI.getUsers().then(data => console.log(data));
 * 
 * // Crear un nuevo usuario
 * dssAPI.createUser({
 *     username: 'juan',
 *     email: 'juan@ejemplo.com',
 *     password: 'hashed_password',
 *     full_name: 'Juan Pérez',
 *     university: 'Universidad XYZ'
 * }).then(data => console.log(data));
 * 
 * // Validar un documento
 * dssAPI.validateDocument('DNI', '12345678Z', 1)
 *     .then(data => console.log(data.is_valid ? 'Válido' : 'Inválido'));
 * 
 * // Obtener estadísticas
 * dssAPI.getStatistics().then(data => console.log(data));
 */
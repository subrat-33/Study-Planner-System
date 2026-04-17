// Centralized API Utility for Smart Study Planner

const API_BASE_URL = '/api';

const api = {
    // Helper to get auth headers
    getHeaders() {
        const token = localStorage.getItem('access_token');
        return {
            'Content-Type': 'application/json',
            ...(token ? { 'Authorization': `Bearer ${token}` } : {})
        };
    },

    // Generic request handler
    async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const config = {
            ...options,
            headers: {
                ...this.getHeaders(),
                ...options.headers
            }
        };

        try {
            const response = await fetch(url, config);
            
            // Handle unauthorized - clear token and redirect to login
            if (response.status === 401) {
                localStorage.removeItem('access_token');
                if (!window.location.pathname.includes('/login')) {
                    window.location.href = '/login';
                }
            }

            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || 'Something went wrong');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    // Convenience methods
    get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    },

    post(endpoint, body) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(body)
        });
    },

    put(endpoint, body) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(body)
        });
    },

    delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }
};

// Global User Info management
const auth = {
    saveToken(token) {
        localStorage.setItem('access_token', token);
    },
    
    getToken() {
        return localStorage.getItem('access_token');
    },
    
    saveUser(user) {
        localStorage.setItem('user_info', JSON.stringify(user));
    },

    getUser() {
        const user = localStorage.getItem('user_info');
        return user ? JSON.parse(user) : null;
    },

    logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_info');
        window.location.href = '/login';
    },

    isAuthenticated() {
        return !!localStorage.getItem('access_token');
    }
};

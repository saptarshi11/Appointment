// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

// Helper function to build API URLs
export const getApiUrl = (endpoint) => {
  // Remove leading slash if present
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint.slice(1) : endpoint;
  const url = `${API_BASE_URL}/${cleanEndpoint}`;
  
  // Debug logging (remove in production)
  console.log(`API Call: ${url}`);
  console.log(`VITE_API_URL: ${import.meta.env.VITE_API_URL}`);
  
  return url;
};

// Export the base URL for direct use
export { API_BASE_URL };

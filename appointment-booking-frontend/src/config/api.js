// API Configuration for single deployment
// In single deployment, API calls can use relative URLs
const API_BASE_URL = '';

// Helper function to build API URLs
export const getApiUrl = (endpoint) => {
  // For single deployment, just return the endpoint as-is
  return endpoint;
};

// Export the base URL for direct use
export { API_BASE_URL };

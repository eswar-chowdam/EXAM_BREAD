const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

function getAuthHeaders() {
  const token = localStorage.getItem('exam_bread_token');
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function registerUser({ full_name, email, password }) {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ full_name, email, password }),
  });

  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    throw new Error(payload.detail || 'Unable to register user.');
  }

  const data = await response.json();
  localStorage.setItem('exam_bread_token', data.token);
  return data;
}

export async function loginUser({ email, password }) {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    throw new Error(payload.detail || 'Unable to log in.');
  }

  const data = await response.json();
  localStorage.setItem('exam_bread_token', data.token);
  return data;
}

export async function getCurrentUser() {
  const response = await fetch(`${API_BASE_URL}/auth/me`, {
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    return null;
  }

  return response.json();
}

export async function fetchDemoDbmsData() {
  const response = await fetch(`${API_BASE_URL}/demo/dbms`);
  if (!response.ok) {
    throw new Error('Unable to load the demo dataset.');
  }
  return response.json();
}

export async function analyzeUploadedPdf(file) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/analysis/upload`, {
    method: 'POST',
    body: formData,
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    throw new Error('Unable to analyze the uploaded PDF.');
  }

  return response.json();
}

export async function generateStudyPlan(analysis) {
  const response = await fetch(`${API_BASE_URL}/planner/from-analysis`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
    body: JSON.stringify({ analysis }),
  });

  if (!response.ok) {
    throw new Error('Unable to generate the study plan.');
  }

  return response.json();
}

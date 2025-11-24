const API_BASE_URL = 'http://localhost:8000';

export const subscriptionsApi = {
  // Get all subscriptions
  async getAll() {
    const response = await fetch(`${API_BASE_URL}/subscriptions`);
    if (response.status === 404) {
      return [];
    }
    if (!response.ok) {
      throw new Error('Failed to fetch subscriptions');
    }
    return await response.json();
  },

  // Get a subscription by ID
  async getById(id) {
    const response = await fetch(`${API_BASE_URL}/subscriptions/${id}`);
    if (!response.ok) {
      throw new Error('Failed to fetch subscription');
    }
    return await response.json();
  },

  // Create a new subscription
  async create(email, eventUrl) {
    const response = await fetch(`${API_BASE_URL}/subscriptions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: email,
        event_url: eventUrl,
      }),
    });
    if (!response.ok) {
      throw new Error('Failed to create subscription');
    }
    return await response.json();
  },

  // Toggle subscription active status
  async toggleStatus(id) {
    const response = await fetch(`${API_BASE_URL}/subscriptions/${id}/flip_status`, {
      method: 'PATCH',
    });
    if (!response.ok) {
      throw new Error('Failed to toggle subscription status');
    }
    return await response.json();
  },

  // Delete a subscription
  async delete(id) {
    const response = await fetch(`${API_BASE_URL}/subscriptions/${id}`, {
      method: 'DELETE',
    });
    if (response.status !== 204) {
      throw new Error('Failed to delete subscription');
    }
  },
};

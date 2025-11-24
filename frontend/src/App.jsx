import { useState, useEffect } from 'react';
import SubscriptionForm from './components/SubscriptionForm';
import SubscriptionList from './components/SubscriptionList';
import { subscriptionsApi } from './api/subscriptions';

function App() {
  const [subscriptions, setSubscriptions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  // Load subscriptions on mount
  useEffect(() => {
    loadSubscriptions();
  }, []);

  const loadSubscriptions = async () => {
    try {
      setIsLoading(true);
      setError('');
      const data = await subscriptionsApi.getAll();
      setSubscriptions(data);
    } catch (err) {
      setError('Failed to load subscriptions. Make sure the backend is running.');
      console.error('Error loading subscriptions:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateSubscription = async (email, eventUrl) => {
    const newSubscription = await subscriptionsApi.create(email, eventUrl);
    setSubscriptions((prev) => [...prev, newSubscription]);
  };

  const handleToggleStatus = async (id) => {
    try {
      const updated = await subscriptionsApi.toggleStatus(id);
      setSubscriptions((prev) =>
        prev.map((sub) => (sub.id === id ? updated : sub))
      );
    } catch (err) {
      alert('Failed to toggle subscription status');
      console.error('Error toggling status:', err);
    }
  };

  const handleDelete = async (id) => {
    try {
      await subscriptionsApi.delete(id);
      setSubscriptions((prev) => prev.filter((sub) => sub.id !== id));
    } catch (err) {
      alert('Failed to delete subscription');
      console.error('Error deleting subscription:', err);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">TicketBot</h1>
          <p className="text-lg text-gray-600">
            Monitor TicketMaster events and get notified when tickets become available
          </p>
        </header>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md mb-6">
            {error}
          </div>
        )}

        <div className="space-y-6">
          <SubscriptionForm onSubscriptionCreated={handleCreateSubscription} />
          <SubscriptionList
            subscriptions={subscriptions}
            onToggleStatus={handleToggleStatus}
            onDelete={handleDelete}
            isLoading={isLoading}
          />
        </div>

        <footer className="mt-12 text-center text-sm text-gray-500">
          <p>TicketBot monitors TicketMaster Ireland for ticket availability</p>
          <p className="mt-1">Make sure the backend is running on http://localhost:8000</p>
        </footer>
      </div>
    </div>
  );
}

export default App;

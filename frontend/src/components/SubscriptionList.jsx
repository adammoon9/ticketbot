export default function SubscriptionList({
  subscriptions,
  onToggleStatus,
  onDelete,
  isLoading
}) {
  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Your Subscriptions</h2>
        <div className="text-center py-8 text-gray-500">Loading subscriptions...</div>
      </div>
    );
  }

  if (subscriptions.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Your Subscriptions</h2>
        <div className="text-center py-8 text-gray-500">
          No subscriptions yet. Create one above to get started!
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">
        Your Subscriptions ({subscriptions.length})
      </h2>

      <div className="space-y-3">
        {subscriptions.map((subscription) => (
          <div
            key={subscription.id}
            className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
          >
            <div className="flex items-start justify-between">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-2">
                  <span
                    className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      subscription.active
                        ? 'bg-green-100 text-green-800'
                        : 'bg-gray-100 text-gray-800'
                    }`}
                  >
                    {subscription.active ? 'Active' : 'Inactive'}
                  </span>
                  <span className="text-sm text-gray-500">ID: {subscription.id}</span>
                </div>

                <div className="space-y-1">
                  <p className="text-sm text-gray-600">
                    <span className="font-medium">User ID:</span> {subscription.user_id}
                  </p>
                  <p className="text-sm text-gray-600">
                    <span className="font-medium">Event ID:</span> {subscription.event_id}
                  </p>
                </div>
              </div>

              <div className="flex gap-2 ml-4">
                <button
                  onClick={() => onToggleStatus(subscription.id)}
                  className={`px-3 py-1 text-sm font-medium rounded-md transition-colors ${
                    subscription.active
                      ? 'bg-yellow-100 text-yellow-800 hover:bg-yellow-200'
                      : 'bg-green-100 text-green-800 hover:bg-green-200'
                  }`}
                  title={subscription.active ? 'Pause subscription' : 'Activate subscription'}
                >
                  {subscription.active ? 'Pause' : 'Activate'}
                </button>

                <button
                  onClick={() => {
                    if (window.confirm('Are you sure you want to delete this subscription?')) {
                      onDelete(subscription.id);
                    }
                  }}
                  className="px-3 py-1 text-sm font-medium bg-red-100 text-red-800 rounded-md hover:bg-red-200 transition-colors"
                  title="Delete subscription"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

import React, { useState, useEffect } from 'react';
import { getHealthStatus } from '../utils/api';

function Dashboard() {
  const [systemStatus, setSystemStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchSystemStatus();
  }, []);

  const fetchSystemStatus = async () => {
    try {
      setLoading(true);
      const data = await getHealthStatus();
      setSystemStatus(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const quickActions = [
    { name: 'Upload Clothing', icon: '📸', link: '/wardrobe', color: 'bg-blue-500' },
    { name: 'Get Recommendations', icon: '✨', link: '/recommendations', color: 'bg-purple-500' },
    { name: 'Try On AR', icon: '👕', link: '/ar-tryon', color: 'bg-pink-500' },
    { name: 'Browse Catalogue', icon: '🛍️', link: '/catalogue', color: 'bg-green-500' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            StyleSense.AI Dashboard
          </h1>
          <p className="text-gray-600">Your AI-powered fashion companion</p>
        </div>

        {/* System Status */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <h2 className="text-2xl font-semibold mb-4">System Status</h2>
          {loading ? (
            <p className="text-gray-500">Loading...</p>
          ) : error ? (
            <div className="bg-red-50 border border-red-200 rounded p-4">
              <p className="text-red-800">Error: {error}</p>
              <button
                onClick={fetchSystemStatus}
                className="mt-2 bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
              >
                Retry
              </button>
            </div>
          ) : systemStatus ? (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-green-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600">Status</p>
                <p className="text-lg font-semibold text-green-700 capitalize">
                  {systemStatus.status}
                </p>
              </div>
              <div className="bg-blue-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600">Database</p>
                <p className="text-lg font-semibold text-blue-700 capitalize">
                  {systemStatus.database}
                </p>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600">ML Models</p>
                <p className="text-lg font-semibold text-purple-700 capitalize">
                  {systemStatus.ml_models}
                </p>
              </div>
            </div>
          ) : null}
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-semibold mb-6">Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {quickActions.map((action, index) => (
              <button
                key={index}
                className={`${action.color} text-white p-6 rounded-lg shadow hover:shadow-lg transform hover:-translate-y-1 transition-all duration-200`}
                onClick={() => {
                  // Navigation would be handled by router in real app
                  alert(`Navigating to ${action.name}`);
                }}
              >
                <div className="text-4xl mb-2">{action.icon}</div>
                <div className="font-semibold">{action.name}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-white rounded-lg shadow-lg p-6 mt-8">
          <h2 className="text-2xl font-semibold mb-4">Recent Activity</h2>
          <div className="space-y-3">
            <div className="flex items-center p-3 bg-gray-50 rounded">
              <span className="text-2xl mr-3">✅</span>
              <div>
                <p className="font-medium">Uploaded new item</p>
                <p className="text-sm text-gray-500">2 hours ago</p>
              </div>
            </div>
            <div className="flex items-center p-3 bg-gray-50 rounded">
              <span className="text-2xl mr-3">✨</span>
              <div>
                <p className="font-medium">Generated outfit recommendations</p>
                <p className="text-sm text-gray-500">5 hours ago</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;

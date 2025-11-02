import React, { useState } from 'react';
import { getRecommendations } from '../utils/api';

function Recommendations() {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    occasion: 'casual',
    weather: 'moderate',
  });

  const occasions = ['casual', 'formal', 'party', 'workout', 'business'];
  const weatherOptions = ['hot', 'cold', 'rainy', 'moderate'];

  const fetchRecommendations = async () => {
    try {
      setLoading(true);
      const data = await getRecommendations({
        user_id: 'default_user',
        ...filters,
      });
      setRecommendations(data.recommendations || []);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 to-purple-50 p-6">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-800 mb-8">
          Outfit Recommendations
        </h1>

        {/* Filters */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <h2 className="text-2xl font-semibold mb-4">Preferences</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Occasion
              </label>
              <select
                value={filters.occasion}
                onChange={(e) => setFilters({ ...filters, occasion: e.target.value })}
                className="block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
              >
                {occasions.map((occ) => (
                  <option key={occ} value={occ}>
                    {occ.charAt(0).toUpperCase() + occ.slice(1)}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Weather
              </label>
              <select
                value={filters.weather}
                onChange={(e) => setFilters({ ...filters, weather: e.target.value })}
                className="block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
              >
                {weatherOptions.map((weather) => (
                  <option key={weather} value={weather}>
                    {weather.charAt(0).toUpperCase() + weather.slice(1)}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <button
            onClick={fetchRecommendations}
            disabled={loading}
            className="w-full bg-purple-600 text-white py-3 px-4 rounded-lg font-semibold hover:bg-purple-700 disabled:bg-gray-300 transition-colors"
          >
            {loading ? '✨ Generating...' : '✨ Get Recommendations'}
          </button>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-8">
            <p className="text-red-800">Error: {error}</p>
          </div>
        )}

        {/* Recommendations Display */}
        {recommendations.length > 0 && (
          <div className="space-y-6">
            <h2 className="text-2xl font-semibold">
              Recommended Outfits
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {recommendations.map((rec, index) => (
                <div
                  key={index}
                  className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow"
                >
                  <div className="bg-gradient-to-r from-purple-400 to-pink-400 p-4">
                    <h3 className="text-white font-bold text-lg">
                      Outfit #{rec.outfit_id || index + 1}
                    </h3>
                    <p className="text-white text-sm opacity-90">
                      Confidence: {((rec.confidence || 0.75) * 100).toFixed(0)}%
                    </p>
                  </div>

                  <div className="p-4">
                    <p className="text-gray-700 mb-3">
                      {rec.description || 'Perfect outfit for your occasion'}
                    </p>

                    <div className="space-y-2">
                      <p className="text-sm font-medium text-gray-600">Items:</p>
                      {Array.isArray(rec.items) && rec.items.length > 0 ? (
                        <ul className="text-sm text-gray-700 space-y-1">
                          {rec.items.map((item, idx) => (
                            <li key={idx} className="flex items-center">
                              <span className="mr-2">•</span>
                              {typeof item === 'object' ? (
                                <span className="capitalize">
                                  {item.color} {item.item}
                                </span>
                              ) : (
                                <span>{item}</span>
                              )}
                            </li>
                          ))}
                        </ul>
                      ) : (
                        <p className="text-sm text-gray-500">Items not specified</p>
                      )}
                    </div>

                    <div className="mt-4 flex gap-2">
                      <span className="inline-block bg-purple-100 text-purple-800 text-xs px-2 py-1 rounded">
                        {rec.occasion || filters.occasion}
                      </span>
                      <span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                        {rec.weather || filters.weather}
                      </span>
                      {rec.method && (
                        <span className="inline-block bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded">
                          {rec.method}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {!loading && recommendations.length === 0 && !error && (
          <div className="bg-white rounded-lg shadow-lg p-8 text-center">
            <p className="text-gray-500 text-lg">
              Click "Get Recommendations" to see personalized outfit suggestions!
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Recommendations;

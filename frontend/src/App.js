import React from 'react';
import './styles/index.css';
import Dashboard from './components/Dashboard';
import Wardrobe from './components/Wardrobe';
import Recommendations from './components/Recommendations';
import ARTryOn from './components/ARTryOn';
import ProductCatalogue from './components/ProductCatalogue';

function App() {
  const [currentView, setCurrentView] = React.useState('dashboard');

  const navigation = [
    { id: 'dashboard', name: 'Dashboard', icon: '🏠' },
    { id: 'wardrobe', name: 'Wardrobe', icon: '👔' },
    { id: 'recommendations', name: 'Recommendations', icon: '✨' },
    { id: 'ar-tryon', name: 'AR Try-On', icon: '👕' },
    { id: 'catalogue', name: 'Catalogue', icon: '🛍️' },
  ];

  const renderView = () => {
    switch (currentView) {
      case 'dashboard':
        return <Dashboard />;
      case 'wardrobe':
        return <Wardrobe />;
      case 'recommendations':
        return <Recommendations />;
      case 'ar-tryon':
        return <ARTryOn />;
      case 'catalogue':
        return <ProductCatalogue />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation Bar */}
      <nav className="bg-white shadow-lg sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-purple-600">StyleSense.AI</h1>
            </div>
            
            <div className="hidden md:flex space-x-4">
              {navigation.map((item) => (
                <button
                  key={item.id}
                  onClick={() => setCurrentView(item.id)}
                  className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                    currentView === item.id
                      ? 'bg-purple-600 text-white'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  <span className="mr-2">{item.icon}</span>
                  {item.name}
                </button>
              ))}
            </div>

            {/* Mobile Menu Button */}
            <div className="md:hidden">
              <button className="text-gray-700 hover:text-purple-600">
                ☰
              </button>
            </div>
          </div>

          {/* Mobile Navigation */}
          <div className="md:hidden pb-4">
            <div className="flex flex-col space-y-2">
              {navigation.map((item) => (
                <button
                  key={item.id}
                  onClick={() => setCurrentView(item.id)}
                  className={`px-4 py-2 rounded-lg font-medium transition-colors text-left ${
                    currentView === item.id
                      ? 'bg-purple-600 text-white'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  <span className="mr-2">{item.icon}</span>
                  {item.name}
                </button>
              ))}
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main>
        {renderView()}
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="text-center">
            <p className="text-sm">
              © 2024 StyleSense.AI - AI-Powered Fashion Recommendations
            </p>
            <p className="text-xs text-gray-400 mt-2">
              Powered by MediaPipe, Sentence Transformers, and DeepFashion Dataset
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;

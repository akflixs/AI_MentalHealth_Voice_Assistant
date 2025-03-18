import { useState, useEffect } from 'react'
import './App.css'
import LiveKitModal from './components/LiveKitModal';
import mindfulLogo from './assets/mindful-logo.svg'



function App() {
  const [showSupport, setShowSupport] = useState(false);

  const handleSupportClick = () => {
    setShowSupport(true)
  }

  useEffect(() => {
    const favicon = document.querySelector('link[rel="icon"]');
    if (favicon) {
      favicon.href = mindfulLogo;
    } else {
      const newFavicon = document.createElement('link');
      newFavicon.rel = 'icon';
      newFavicon.href = mindfulLogo;
      document.head.appendChild(newFavicon);
    }
  }, []);
  
  return (
    <div className="app">
      <header className="header">
        <div className="logo">MindfulSupport</div>
        <nav>
          <a href="#">Home</a>
          <a href="#">Resources</a>
          <a href="#">About Us</a>
          <a href="#">Contact</a>
        </nav>
      </header>

      <main>
        <section className="hero">
          <h1>Your Mental Health Matters</h1>
          <p>Find support and guidance on your journey to wellness</p>
          <div className="search-bar">
            <input type="text" placeholder='Search for resources or topics'></input>
            <button>Search</button>
          </div>
        </section>

        <section className="categories">
          <div className="category-card">
            <h3>Stress Management</h3>
            <p>Techniques and tools to help manage daily stress</p>
          </div>
          <div className="category-card">
            <h3>Anxiety Support</h3>
            <p>Resources for understanding and managing anxiety</p>
          </div>
          <div className="category-card">
            <h3>Depression</h3>
            <p>Guidance and support for dealing with depression</p>
          </div>
          <div className="category-card">
            <h3>Mindfulness</h3>
            <p>Practices to stay present and improve mental clarity</p>
          </div>
        </section>

        <button className="support-button" onClick={handleSupportClick}>
          Talk to a Support Assistant
        </button>
      </main>

      {showSupport && <LiveKitModal setShowSupport={setShowSupport}/>}
    </div>
  )
}

export default App
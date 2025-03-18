import { useState, useCallback, useEffect } from "react";
import { LiveKitRoom, RoomAudioRenderer } from "@livekit/components-react";
import "@livekit/components-styles";
import SimpleVoiceAssistant from "./SimpleVoiceAssistant";

const DEFAULT_LIVEKIT_URL = "wss://ai-call-center-8xu4i0ft.livekit.cloud";

const LiveKitModal = ({ setShowSupport }) => {
  const [isSubmittingName, setIsSubmittingName] = useState(true);
  const [name, setName] = useState("");
  const [token, setToken] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [liveKitUrl, setLiveKitUrl] = useState("");

  // Set LiveKit URL on component mount
  useEffect(() => {
    // Try to get from environment variable first
    const envUrl = import.meta.env.VITE_LIVEKIT_URL;
    
    if (envUrl) {
      console.log("Using LiveKit URL from environment:", envUrl);
      setLiveKitUrl(envUrl);
    } else {
      console.log("No environment URL found, using default:", DEFAULT_LIVEKIT_URL);
      setLiveKitUrl(DEFAULT_LIVEKIT_URL);
    }
  }, []);

  const getToken = useCallback(async (userName) => {
    if (!userName.trim()) {
      setError("Please enter your name");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      console.log("Requesting token for user:", userName);
      
      // Make the request to the backend
      const response = await fetch(`/api/getToken?name=${encodeURIComponent(userName)}`);
      
      if (!response.ok) {
        throw new Error(`Server error: ${response.status} ${response.statusText}`);
      }
      
      const tokenText = await response.text();
      
      if (!tokenText || tokenText.length < 10) {
        throw new Error("Invalid token received from server");
      }
      
      console.log("Token received successfully");
      setToken(tokenText);
      setIsSubmittingName(false);
    } catch (err) {
      console.error("Error getting token:", err);
      setError(`Could not connect: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const handleNameSubmit = (e) => {
    e.preventDefault();
    getToken(name);
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <button
          className="close-button"
          onClick={() => setShowSupport(false)}
        >
          ×
        </button>
        <div className="support-room">
          {isSubmittingName ? (
            <form onSubmit={handleNameSubmit} className="name-form">
              <h2>Start Your Mental Health Support Session</h2>
              <p>Enter your name to connect with our support assistant</p>
              
              {error && (
                <div className="error-message">{error}</div>
              )}
              
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Your name"
                required
                disabled={isLoading}
              />
              
              <button type="submit" disabled={isLoading}>
                {isLoading ? "Connecting..." : "Connect"}
              </button>
              
              <button
                type="button"
                className="cancel-button"
                onClick={() => setShowSupport(false)}
                disabled={isLoading}
              >
                Cancel
              </button>
              
              <div className="privacy-note">
                <small>Your conversations are private and confidential.</small>
              </div>
            </form>
          ) : token && liveKitUrl ? (
            <LiveKitRoom
              serverUrl={liveKitUrl}
              token={token}
              connect={true}
              video={false}
              audio={true}
              onConnected={() => {
                console.log("Connected to LiveKit room");
              }}
              onDisconnected={() => {
                console.log("Disconnected from LiveKit room");
                setShowSupport(false);
                setIsSubmittingName(true);
                setToken(null);
              }}
              onError={(connectionError) => {
                console.error("LiveKit connection error:", connectionError);
                setError(`Connection error: ${connectionError.message}`);
                setIsSubmittingName(true);
                setToken(null);
              }}
            >
              <RoomAudioRenderer />
              <SimpleVoiceAssistant />
            </LiveKitRoom>
          ) : (
            <div className="loading">
              <p>Connecting to support assistant...</p>
              {error && <div className="error-message">{error}</div>}
              <button 
                onClick={() => setIsSubmittingName(true)} 
                className="retry-button"
              >
                Retry
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default LiveKitModal;
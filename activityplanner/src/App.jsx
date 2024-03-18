import { useState } from 'react';
import './App.css';

function App() {
  const [inputText, setInputText] = useState('');
  const [activities, setActivities] = useState([]);
  const [showInput, setShowInput] = useState(true);
  const [showActivity, setShowActivity] = useState(false);

  const handleButtonClick = async () => {
    setShowInput(!showInput);
    setShowActivity(!showActivity);
    try {
      const response = await fetch('http://localhost:3000', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputText }),
      });
  
      if (!response.ok) {
        throw new Error('Failed to send data');
      }
  
      // Parse the response body as JSON
      const data = await response.json();
  
      // Update the activities state with the received activities
      setActivities(data.activities);
  
      // Reset input field after successful POST request
      setInputText('');
    } catch (error) {
      console.error('Error:', error);
    }
  };
  

  const handleInputChange = (event) => {
    setInputText(event.target.value);
  };


  return (
    <>
      {showInput &&(<div className="card">
        <input
          type="text"
          value={inputText}
          onChange={handleInputChange}
        />
        <button onClick={handleButtonClick}>Send Text</button>
      </div>
      )}
      {/* Render the received activities */}
      {showActivity && (<div className="activities">
        <h2>Activities</h2>
        <div>
          {activities.map((activity, index) => (
            <div key={index}>
              <strong>Name:</strong> {activity.name}, <strong>Cost:</strong> {activity.cost}, <strong>Duration:</strong> {activity.duration}
            </div>
          ))}
        </div>
        <button onClick={handleButtonClick}>Go Back</button>
      </div>
      
      )}
    </>
  );
}

export default App;

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
      const response = await fetch('http://192.168.247.109:8000/backend/recommend/', {
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
    <header className="header">       
        <div className="text-box">
            <h1 className="heading-primary">
                <span className="heading-primary-main">Vacation Planner<br></br></span>
                <span className="heading-primary-sub">make  your vacation easier</span>
            </h1>
            <p><br></br></p>
    </div>
    </header>
      {showInput &&(<div className="card">
        <div className="box">
          <form id="planner-form">
              <div className="input-container">      
                  <input value = {inputText} onChange = {handleInputChange} type="text" id="destination" class="form__field" required=""/>
                  <label htmlFor="destination">where to?</label>
              </div>
          </form>
        </div>
        <button onClick = {handleButtonClick}type="submit" className="custom-button">Plan My Vacation</button>
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

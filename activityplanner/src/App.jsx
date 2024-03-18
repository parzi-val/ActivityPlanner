import { useState } from 'react';
import './App.css';
import React from 'react';
import Collapsible from 'react-collapsible';
import { Link } from 'react-router-dom'
function ActivityBox({ activity }) {
  return (
    <div className="activitybox">
      <Collapsible trigger={`v`}>
        <div id="additional" className="additional-content">
          <p>{activity.categoryName}</p>
          <p>Address: {activity.address}</p>
          <a target = "_blank" href={activity.url}>Google maps</a>
          <p>Ph: {activity.phone}</p>
        </div>
      </Collapsible>
      <div className="time-frame">{activity.time} HOURS</div>
      <div className="activity">{activity.title}</div>
      <div>$ {activity.price}</div>
    </div>
  );
}

function App() {
  const [inputText, setInputText] = useState('');
  const [activities, setActivities] = useState([]);
  const [showInput, setShowInput] = useState(true);
  const [showActivity, setShowActivity] = useState(false);

  const handleButtonClick = async () => {
    setShowInput(!showInput);
    setShowActivity(!showActivity);
    try {
      const response = await fetch('http://127.0.0.1:8000/backend/recommend/', {
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
      let data = await response.json();
      data = JSON.parse(data);
      // Update the activities state with the received activities
      console.log(data);
      setActivities(data["activities"]);
  
      // Reset input field after successful POST request
      setInputText('');
    } catch (error) {
      console.error('Error:', error);
    }
  };
  

  const handleInputChange = (event) => {
    setInputText(event.target.value);
    setActivities([]);
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
                  <input value = {inputText} onChange = {handleInputChange} type="text" id="destination" className="form__field" required=""/>
                  <label htmlFor="destination">where to?</label>
              </div>
          </form>
        </div>
        <button onClick = {handleButtonClick}type="submit" className="custom-button">Plan My Vacation</button>
      </div>
      )}
      {/* Render the received activities */}
      {showActivity && activities && (
        <div className="activities">
          <h2>Activities</h2>
          <div>
            {activities.length > 0 ? (
              activities.map((activity, index) => (
                <ActivityBox key={index} activity={activity} />
              ))
            ) : (
              <p>Activities Loading...</p>
            )}
          </div>
          <button onClick={handleButtonClick}>Go Back</button>
        </div>
      )}
    </>
  );
}

export default App;

import { useState } from 'react';
import './App.css';

function App() {
  const [inputText, setInputText] = useState('');
  const handleButtonClick = async () => {
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
      <div className="card">
        <input
          type="text"
          value={inputText}
          onChange={handleInputChange}
        />
        <button onClick={handleButtonClick}>Send Text</button>
      </div>
    </>
  );
}

export default App;
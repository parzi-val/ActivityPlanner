const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const app = express();
const PORT = 3000;
app.use(cors());
// Middleware to parse JSON request bodies
app.use(bodyParser.json());
app.get('/', (req, res) => {
    res.send('hello');
  });
// POST endpoint
app.post('/', (req, res) => {
  const { text } = req.body;
  console.log('Received text:', text);
  res.json({
    "activities": [
      {"name": "Activity 1", "cost": 100, "duration": "1 hour"},
      {"name": "Activity 2", "cost": 50, "duration": "30 minutes"},
      {"name": "Activity 3", "cost": 200, "duration": "2 hours"}
    ]
  });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});

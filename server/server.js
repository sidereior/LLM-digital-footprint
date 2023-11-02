const express = require('express');
const cors = require('cors');
const app = express();
const helmet = require('helmet');
app.use(helmet());

// Enable CORS for client-side
app.use(cors());

// Parse JSON bodies
app.use(express.json());

// Define a simple route
app.get('/', (req, res) => {
  res.send('Hello from the backend!');
});

app.post('/getUserInfo', async (req, res) => {
  const { name, additionalInfo } = req.body;
  if (!name) {
    return res.status(400).send('Name is required');
  }

  try {
    // Here you will implement the logic to call OpenAI's GPT-4 and Lang Chain
    const result = await getUserInfoFromAI(name, additionalInfo);
    res.json(result);
  } catch (error) {
    console.error('Error fetching user info:', error);
    res.status(500).send('Internal Server Error');
  }
});

// Start the server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

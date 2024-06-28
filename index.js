const express = require('express');
const app = express();

const PORT = process.env.PORT || 3000;

// Define a route handler for the root path
app.get('/', (req, res) => {
  res.send('Hello World!');
});

// Start the server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server is running on port ${PORT}`);
});

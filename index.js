const express = require('express');
const app = express();
const path = require('path');

const PORT = process.env.PORT || 3000;

// Serve static files from the directory where your static files are located
app.use(express.static(path.join(__dirname, 'containers', 'django', 'src', 'playpong', 'static')));

// Define a route handler for the root path
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'containers', 'django', 'src', 'playpong', 'static', 'index.html'));
});

// Start the server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server is running on port ${PORT}`);
});

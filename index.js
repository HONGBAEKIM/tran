// const express = require('express');
// const app = express();
// const port = 8080;

// app.get('/', (req, res) => {
//   res.send('Hello World!');
// });

// app.listen(port, () => {
//   console.log(`App listening at http://localhost:${port}`);
// });

const express = require('express');
const app = express();

const PORT = process.env.PORT || 3000;

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server is running on port ${PORT}`);
});


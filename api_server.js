const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 5000;

// Endpoint para obter dados do DB.json
app.get('/data', (req, res) => {
  const filePath = path.join(__dirname, 'DB.json');
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      return res.status(500).send('Erro ao ler o arquivo DB.json');
    }
    res.json(JSON.parse(data));
  });
});

app.listen(PORT, () => {
  console.log(`API rodando em http://localhost:${PORT}`);
});

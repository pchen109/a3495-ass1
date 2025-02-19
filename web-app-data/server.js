const express = require('express');
const mysql = require('mysql2/promise');
const axios = require('axios');
const app = express();
app.use(express.json());

const pool = mysql.createPool({
    host: process.env.MYSQL_HOST,
    user: process.env.MYSQL_USER,
    password: process.env.MYSQL_PASSWORD,
    database: process.env.MYSQL_DATABASE
});

app.post('/data', async (req, res) => {
    const auth = await axios.post(`${process.env.AUTH_SERVICE_URL}/auth`, req.body);
    if (!auth.data.authenticated) return res.status(401).send('Unauthorized');
    
    await pool.query('INSERT INTO temperatures (value) VALUES (?)', [req.body.value]);
    res.send('Data saved');
});

app.listen(process.env.DATA_PORT, () => console.log(`Data service running on port ${process.env.DATA_PORT}`));
const express = require('express');
const app = express();
const http = require('http').createServer(app);
const io = require('socket.io')(http);
const bodyParser = require('body-parser');
const path = require('path');


app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Store the latest temperature value
let currentWeather = {"altitude": 1642.83, "gas": 2766, "pressure": 830.875, "temperature": 12, "humidity": 57.6608};

app.post('/weather', (req, res) => {
    const newWeather = req.body.weather;
    // Update the current temperature value
    currentWeather = newWeather;
    // Emit the new weather data to the connected clients
    io.emit('newWeatherData', currentWeather);
    res.send("Received Weather");
});

const port = 2345;
http.listen(port, () => {
    console.log(`Server running on port: ${port}`);
});

// Socket.io connection handling
io.on('connection', (socket) => {
    console.log('A client connected');
  
    // Send the initial temperature value to the client
    socket.emit('newWeatherData', currentWeather);
  
    // Handle client disconnection
    socket.on('disconnect', () => {
        console.log('A client disconnected');
    });
});

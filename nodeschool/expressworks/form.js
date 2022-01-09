var express = require('express');
var path = require('path');
var bodyParser = require('body-parser');

var app = express();

app.set("view engine", "jade");
app.set("views", (path.join(__dirname, 'templates')));

app.use(express.static(path.join(__dirname, "public")));

app.use(bodyParser.urlencoded({extended: false}));

app.get('/home', function(req, res) {
    res.render('index', {date: new Date().toDateString()});
});

app.post('/form', function(req, res) {
    res.end(req.body.str.split('').reverse().join(''));
});
app.listen(process.argv[2]);
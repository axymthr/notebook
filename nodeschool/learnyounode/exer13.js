var http = require('http');
var url = require('url');

http.createServer(function (req, res) {
    var result;
    if (req.method === 'GET') {
        var parsedUrl = url.parse(req.url, true);
        var date = new Date(parsedUrl.query.iso);
        if (parsedUrl.pathname === '/api/parsetime') {
            result = parseTime(date);
        } else if (parsedUrl.pathname === '/api/unixtime') {
            result = unixtime(date);
        }
    }
    if (result) {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(result));
    } else {
        res.writeHead(404);
        res.end();
    }

}).listen(process.argv[2]);

function parseTime(date) {
    return {
        "hour" : date.getHours(),
        "minute" : date.getMinutes(),
        "second" : date.getSeconds()
    }
}

function unixtime(date) {
    return {
        "unixtime" : date.getTime()
    }
}
var fs = require('fs');
var http = require('http');

http.createServer(function (req, res) {
	res.writeHead(200, { 'content-type': 'text/plain' });
    fs.createReadStream(process.argv[3]).pipe(res);
}).listen(process.argv[2]);


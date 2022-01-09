var through = require('through2');
var trumpet = require('trumpet');
var tr = trumpet();
tr.select('.loud').createStream().pipe(through(function(chunk, _, next) {
    next(null, chunk.toString().toUpperCase());
}));
process.stdin.pipe(tr);
tr.pipe(process.stdout);

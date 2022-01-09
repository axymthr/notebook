var through = require('through2');

var stream = through(write);

process.stdin.pipe(stream).pipe(process.stdout);

function write(buffer, _, next) {
    next(null, buffer.toString().toUpperCase());
}


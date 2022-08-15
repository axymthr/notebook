var split = require('split');
var through2 = require('through2');

var odd = true;

process.stdin.pipe(split()).
    pipe(through2(function (line, _, next) {
        if (odd) {
            this.push(line.toString().toLowerCase() + '\n');
            odd = false;
        } else {
            this.push(line.toString().toUpperCase() + '\n');
            odd = true;
        }
        next();
    })).pipe(process.stdout);

var combine = require('stream-combiner');
var gzip = require('zlib').createGzip();
var through = require('through2');
var split = require('split');

module.exports = function () {
    var line;
    return combine(
        split(),
        through(flatten, end),
        gzip
    );

    function flatten(row, _, next) {
        if (row.length === 0) return next();
        var data = JSON.parse(row);
        if (data.type === 'genre') {
            if (line) {
                this.push(JSON.stringify(line) + '\n');
            }
            line = {};
            line.books = [];
            line.name = data.name;
        } else if (data.type === 'book') {
            line.books.push(data.name);
        }
        next();
    }

    function end(next) {
        if (line) {
            this.push(JSON.stringify(line) + '\n');
        }
        this.push(null);
        next();
    }
};
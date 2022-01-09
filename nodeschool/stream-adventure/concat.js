var concat = require('concat-stream');

process.stdin.pipe(concat(function(contents) {
    process.stdout.write(contents.toString().split('').reverse().join(''));
}));
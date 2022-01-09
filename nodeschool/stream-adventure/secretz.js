var gunzipper = require('zlib').createGunzip();
var crypto = require('crypto');
var tarParser = require('tar').Parse();
var concat = require('concat-stream');

var decrypter = crypto.createDecipher(process.argv[2], process.argv[3]);
tarParser.on('entry', function (entry) {
    if (entry.type !== 'File') return;
    var md5Hash = crypto.createHash('md5', { encoding: 'hex' });
    entry.pipe(md5Hash).pipe(concat(function(hash) {
        console.log(hash + " " + entry.path);
    }));
});
process.stdin.pipe(decrypter).pipe(gunzipper).pipe(tarParser);
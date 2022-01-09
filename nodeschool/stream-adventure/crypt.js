var crypto = require('crypto');
var decrypter = crypto.createDecipher('aes256', process.argv[2]);
process.stdin.pipe(decrypter).pipe(process.stdout);
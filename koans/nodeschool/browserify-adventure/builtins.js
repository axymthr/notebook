var url = require('url');

var address = prompt('url to parse');
console.log(url.resolve(address, require('querystring').parse(url.parse(address).query).file));


var ndjson = require('./ndjson');
console.log(ndjson.parse(prompt('string to parse')));
console.log(ndjson.stringify(prompt('array to serialize')));
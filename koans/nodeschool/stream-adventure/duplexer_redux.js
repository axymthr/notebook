var duplexer = require('duplexer2'),
    through = require('through2').obj;

module.exports = function (counter) {
    var countries = {};
    var input = through(write, end);
    var duplex = duplexer(input, counter);
    return duplex;

    function write(obj, _, done) {
        countries[obj.country] = (countries[obj.country] || 0) + 1;
        done();
    }

    function end(done) {
        counter.setCounts(countries);
        done();
    }
};

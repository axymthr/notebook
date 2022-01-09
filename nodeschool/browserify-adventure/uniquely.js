var uniq = require('uniq');

module.exports = function(input) {
    return uniq(input.split(','));
};

var domify = require('domify');

var elem = domify('<div>Hello <span class="name"></span>!</div>');

module.exports = function() {
    this.setName = function(str) {
        elem.querySelector('.name').textContent = str;
    };
    this.appendTo = function(target) {
        target.appendChild(elem);
    };
    return this;
};
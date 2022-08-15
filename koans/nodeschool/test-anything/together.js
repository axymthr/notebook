var fancify = require(process.argv[2]);
var test = require('tape');

test("fancify('Hello') returns ~*~Hello~*~", function (t) {
    t.equal(fancify('Hello'), "~*~Hello~*~");
    t.end();
});

test("fancify('Hello', true) returns ~*~HELLO~*~", function (t) {
    t.equal(fancify('Hello', true), "~*~HELLO~*~");
    t.end();
});

test("fancify('Hello', false, '!') returns ~!~Hello~!~", function (t) {
    t.equal(fancify('Hello', false, '!'), "~!~Hello~!~");
    t.end();
});

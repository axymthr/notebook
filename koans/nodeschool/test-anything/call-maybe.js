var repeatCallback = require(process.argv[2]);
var test = require('tape');

test("repeatCallback(n, cb)", function (t) {
    t.plan(3);
    repeatCallback(3, function () {
        t.pass("callback called");
    });
});
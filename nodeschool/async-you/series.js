var http = require('http'),
    async = require('async');

async.series({
    requestOne: function(done){
        request(process.argv[2], done);
    },
    requestTwo: function(done){
        request(process.argv[3], done);
    }
}, function(err, results){
    console.log(results);
});

function request(url, done) {
    var body = '';
    http.get(url, function(res){
        res.on('data', function(chunk){
            body += chunk.toString();
        });
        res.on('end', function(){
            done(null, body);
        });
    }).on('error', function(err) {
        done(err);
    });
}
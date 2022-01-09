const http = require('http');

const isValid = (pod) => {
  // validate pod here
};

const server = http.createServer((request, response) => {
  var json = '';
  request.on('data', (data) => {
    json += data;
  });
  request.on('end', () => {
    var admissionReview = JSON.parse(json);
    var pod = admissionReview.request.object;

    var review = {
      kind: 'AdmissionReview',
      apiVersion: 'admission/v1beta1',
      response: {
        allowed: isValid(pod)
      }
    };
    response.end(JSON.stringify(review));
  });
});

server.listen(8080, (err) => {
  if (err) {
    return console.log('admission controller failed to start', err);
  }

  console.log('admission controller up and running.');
});

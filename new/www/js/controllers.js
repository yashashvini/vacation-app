angular.module('starter.controllers', ['ionic'])

.controller('DashCtrl', function($scope,$http) {
  $scope.data = {
    speechText: ''
  };
  $scope.recognizedText = [];
  var accessToken = "8bd3b6024a8e461f8e4e63c181882295";
  var baseUrl = "http://127.0.0.1:5000/";
  

  $scope.speakText = function() {
    alert("speaking");
    window.TTS.speak({
           text: $scope.recognizedText[0],
           locale: 'en-GB',
           rate: 1.5
       }, function (success) {
            $scope.record();
           // Do Something after success
       }, function (reason) {
          alert('some error occurred, speak again');
          $scope.record();
          // Handle the error case
       });
  };

  $scope.record = function() {
    var recognition = new webkitSpeechRecognition();
    alert('calling record');
    recognition.onresult = function(event) {
      if (event.results.length > 0) {
        $scope.recognizedText.unshift(event.results[0][0].transcript);
        $scope.$apply();
        $http({
          method: "POST",
          url: baseUrl,
          contentType: "application/json; charset=utf-8",
          dataType: "json",
          headers: {
            "Authorization": "Bearer " + accessToken
          },
          data: JSON.stringify({ query: $scope.recognizedText[0], lang: "en", sessionId: "somerandomthing" }),
        }).then(function successCallback(response) {
            $scope.recognizedText.unshift(response.data.result.speech);
            alert('speaking');
            $scope.speakText();
          }, function errorCallback(response) {
            // called asynchronously if an error occurs
            // or server returns response with an error status.
            alert('unkown error occurred, speak again');
            $scope.record();
        });
      }
    };
    recognition.start();
  };
})


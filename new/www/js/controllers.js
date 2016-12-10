angular.module('starter.controllers', ['ionic'])

.controller('DashCtrl', function($scope,$http) {
  $scope.data = {
    speechText: ''
  };
  $scope.recognizedText = [];
  var accessToken = "96a5eba7687d4fb8884f595edfbb78cd";
  var subscriptionKey = "4ff074a867ab4d71a8f12eb5fd20822d";
  var baseUrl = "https://api.api.ai/v1/";
  

  $scope.speakText = function() {
    alert("speaking");
    window.TTS.speak({
           text: $scope.recognizedText[0],
           locale: 'en-GB',
           rate: 1.5
       }, function () {
           // $scope.record();
           // Do Something after success
       }, function (reason) {
          //$scope.record();
          // Handle the error case
       });
  };
  
  $scope.recognizeSpeech = function() {
    var maxMatches = 5;
    var language = "en-US"; // Optional
    var txt = "";
    window.continuoussr.startRecognize(function(result){
        //alert(result);
        console.log(result);
        $scope.recognizedText.unshift(result[0]);
        txt = result[0];
        $scope.$apply()
        $http({
          method: "POST",
          url: baseUrl + "query/",
          contentType: "application/json; charset=utf-8",
          dataType: "json",
          headers: {
            "Authorization": "Bearer " + accessToken
          },
          data: JSON.stringify({ query: txt, lang: "en", sessionId: "somerandomthing" }),
        }).then(function successCallback(response) {
            console.log(response.data.result.speech);
            alert(response.data.result.speech);
            $scope.recognizedText.unshift(response.data.result.speech);
            
            alert("calling speak");

            $scope.speakText();
            $scope.apply();
          }, function errorCallback(response) {
            alert("error");
            // called asynchronously if an error occurs
            // or server returns response with an error status.
        });
    }, function(errorMessage){
        alert("Error message: " + errorMessage);
    }, maxMatches, language);
  };

  $scope.record = function() {
    var recognition = new SpeechRecognition();
    console.log("hmm");
    recognition.onresult = function(event) {
      console.log(event);
      if (event.results.length > 0) {
        $scope.recognizedText = event.results[0][0].transcript;
        $scope.$apply()
        $http({
          method: "POST",
          url: baseUrl + "query/",
          contentType: "application/json; charset=utf-8",
          dataType: "json",
          headers: {
            "Authorization": "Bearer " + accessToken
          },
          data: JSON.stringify({ query: $scope.recognizedText, lang: "en", sessionId: "somerandomthing" }),
        }).then(function successCallback(response) {
            console.log(response.data.result.speech);
            $scope.recognizedText = response.data.result.speech;
            $scope.speakText();
          }, function errorCallback(response) {
            // called asynchronously if an error occurs
            // or server returns response with an error status.
        });
      }
    };
    recognition.start();
  };
})


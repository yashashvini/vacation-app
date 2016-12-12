angular.module('starter.controllers', ['ionic'])

.controller('DashCtrl', function($scope,$http,$ionicModal) {
  $scope.data = {
    speechText: ''
  };
  $scope.recognizedText = [];
  var accessToken = "8bd3b6024a8e461f8e4e63c181882295";
  var baseUrl = "https://cookingasst.herokuapp.com/";
  
  $ionicModal.fromTemplateUrl('my-modal.html', {
      scope: $scope,
      animation: 'slide-in-up'
   }).then(function(modal) {
      $scope.modal = modal;
   });

  $scope.speakText = function() {
    window.TTS.speak({
           text: $scope.recognizedText[0].text,
           locale: 'en-GB',
           rate: 1.5
       }, function (success) {
            $scope.record();
           // Do Something after success
       }, function (reason) {
          //alert('some error occurred, speak again');
          $scope.record();
          // Handle the error case
       });
  };

  $scope.record = function() {
    var recognition = new SpeechRecognition();
    recognition.continuous = true;
    //recognition.interimResults = true;
    console.log('calling record');
    recognition.onresult = function(event) {
      console.log("result");
      if (event.results.length > 0) {
        var displayObjClient = {
          text : '',
          origin : 'client'
        };
        displayObjClient.text = event.results[0][0].transcript;
        $scope.recognizedText.unshift(displayObjClient);
        $scope.$apply();
        $http({
          method: "POST",
          url: baseUrl,
          contentType: "application/json; charset=utf-8",
          dataType: "json",
          headers: {
            "Authorization": "Bearer " + accessToken
          },
          data: JSON.stringify({ query: $scope.recognizedText[0].text, lang: "en", sessionId: "somerandomthing" }),
        }).then(function successCallback(response) {
          var displayObjServer = {
            text : '',
            origin : 'server'
          };
          displayObjServer.text = response.data;
          $scope.recognizedText.unshift(displayObjServer);
            $scope.speakText();
          }, function errorCallback(response) {
            // called asynchronously if an error occurs
            // or server returns response with an error status.
            //alert('unkown error occurred, speak again');
            $scope.record();
        });
      }
    };
    recognition.onstart = function(event){
      //$scope.modal.show();
    };

    recognition.onend = function(event){
      //$scope.modal.hide();
    };
    recognition.start();
  };
})


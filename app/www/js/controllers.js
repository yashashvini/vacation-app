angular.module('starter.controllers', ['ionic'])

.controller('DashCtrl', function($scope,$http,$ionicModal) {
  $scope.data = {
    speechText: ''
  };
  $scope.vacation = "";
  $scope.recognizedText = [];
  var accessToken = "1e4bd06b41b745b9b49c47318de85bb2";
  var baseUrl = "https://homeawayvacation.herokuapp.com/";
  $scope.text = "Tap here and say Hello";
  
  $ionicModal.fromTemplateUrl('my-modal.html', {
      scope: $scope,
      animation: 'slide-in-up'
   }).then(function(modal) {
      $scope.modal = modal;
   });

  $scope.speakText = function() {
    window.speechSynthesis.speak($scope.msg);
    // console.log($scope.recognizedText[0].text)
    // window.TTS.speak({
    //        text: $scope.recognizedText[0].text,
    //        locale: 'en-GB',
    //        rate: 1.5
    //    }, function (success) {
    //         //$scope.record();
    //        // Do Something after success
    //    }, function (reason) {
    //       //alert('some error occurred, speak again');
    //       //$scope.record();
    //       // Handle the error case
    //    });
  };

  $scope.record = function(signal) {
    var recognition = new webkitSpeechRecognition();
    //recognition.continuous = true;
    //recognition.interimResults = true;
    //console.log('calling record');
    recognition.onresult = function(event) {
      //console.log("result");
      if (event.results.length > 0) {
        var displayObjClient = {
          text : '',
          origin : 'user'
        };
        displayObjClient.text = event.results[0][0].transcript;
        //console.log(displayObjClient.text);
        $scope.recognizedText.unshift(displayObjClient);
        $scope.$apply();

        $http({
          method: "POST",
          url: baseUrl,
          //+ "query/?v=20170715&amp;",
          contentType: "application/json; charset=utf-8",
          dataType: "json",
          // headers: {
          //   "Authorization": "Bearer " + accessToken,
          // },
          data: $scope.recognizedText[0].text
          //data: JSON.stringify({ query: $scope.recognizedText[0].text, lang: "en", sessionId: "873fdf8a-aae9-41af-a453-8450622d578d",timezone:'2017-07-15T11:03:10-0500' }),
        }).then(function successCallback(response) {
          var displayObjServer = {
            text : '',
            origin : 'system'
          };
          displayObjServer.text = response.data;
          //console.log(response.data);
          if(response.data.msg){
              displayObjServer.text = response.data.msg;
              $scope.vacation = response.data.vacations;
          }
          var msg = displayObjServer.text;
          var utterThis = new SpeechSynthesisUtterance(msg);
          $scope.recognizedText.unshift(displayObjServer);
          window.speechSynthesis.speak(utterThis);
          //$scope.speakText();
          }, function errorCallback(response) {
            // called asynchronously if an error occurs
            // or server returns response with an error status.
            //alert('unkown error occurred, speak again');
            $scope.record();
        });
      }
    };
    recognition.onstart = function(event){
      $scope.text = "Listening";
      $scope.$apply();
    };

    recognition.onend = function(event){
      $scope.text = "Vacations";
      $scope.$apply();
    };
    recognition.start();
  };
})


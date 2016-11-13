angular.module('starter.controllers', ['ionic'])

.controller('DashCtrl', function($scope,$http) {
  $scope.data = {
    speechText: ''
  };
  $scope.recognizedText = '';
  var accessToken = "7853febc373644728bc5d5f9e6d0282d";
  var subscriptionKey = "4ff074a867ab4d71a8f12eb5fd20822d";
  var baseUrl = "https://api.api.ai/v1/";
  

  $scope.speakText = function() {
    TTS.speak({
           text: $scope.recognizedText,
           locale: 'en-GB',
           rate: 1.5
       }, function () {
           // Do Something after success
       }, function (reason) {
           // Handle the error case
       });
  };
 
  $scope.record = function() {
    var recognition = new SpeechRecognition();
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
                "Authorization": "Bearer " + accessToken,
                "ocp-apim-subscription-key": subscriptionKey
              },
              data: JSON.stringify({ q: $scope.recognizedText, lang: "en" }),
            }).then(function successCallback(response) {
                console.log(response.data.result.speech);
                $scope.recognizedText = response.data.result.speech;
              }, function errorCallback(response) {
                // called asynchronously if an error occurs
                // or server returns response with an error status.
              });
        }
    };
    recognition.start();
  };
})

.controller('ChatsCtrl', function($scope, Chats) {
  // With the new view caching in Ionic, Controllers are only called
  // when they are recreated or on app start, instead of every page change.
  // To listen for when this page is active (for example, to refresh data),
  // listen for the $ionicView.enter event:
  //
  //$scope.$on('$ionicView.enter', function(e) {
  //});

  $scope.chats = Chats.all();
  $scope.remove = function(chat) {
    Chats.remove(chat);
  };
})

.controller('ChatDetailCtrl', function($scope, $stateParams, Chats) {
  $scope.chat = Chats.get($stateParams.chatId);
})

.controller('AccountCtrl', function($scope) {
  $scope.settings = {
    enableFriends: true
  };
});

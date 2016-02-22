(function() {
  'use strict';

  var app = angular
                .module('virtualQueue')
                .controller('NewController', NewController);
 
  function NewController($http, $log, $scope, $state, $location) {
    
    var org_domain = $location.search().orgId;
    var vm = this;
    var org_domain = 'scotia.virtualqueue.com';
    vm.group_list = [];
    vm.queue_list = [];
    var queue_items = [];

    $scope.myInstructions = "Choose a location";
    $scope.qStyle = {'visibility': 'hidden'}; // then button will hidden.
    $scope.phoneStyle = {'visibility': 'hidden'};
    $scope.gStyle = {'visibility': 'visible'};
    $scope.resetStyle = {'visibility': 'hidden'};
      
    //Get Group Detail for dropdown list
    $http({
      method: 'GET',
      url:'http://169.45.236.176:4000/api/v1/organization/?org_domain=' + org_domain
    //url: '../food.json'
    })
    .success(function (data) {
            vm.group_list = data.data.org_queue_groups;
            $log.debug(data.data.org_queue_groups);
    })
    .error(function () {
        // something went wrong :(
    });
    
      
    //Get Selected Group & load Queue Details
    $scope.stepOne = function(myGroupSelect) {
        $log.debug("Index selcted " + myGroupSelect);
        $log.debug(vm.group_list[parseInt(myGroupSelect)]);
        vm.queue_list = vm.group_list[parseInt(myGroupSelect)-1].group_queues; 
        $scope.qStyle = {'visibility': 'visible'};
        $scope.gStyle = {'display': 'none'};
        $scope.myInstructions = "What do you want to do?";
        $scope.resetStyle = {'visibility': 'visible'};
    }
    
    //Get Selected Queue & display queue count
    $scope.stepTwo = function(myQueueSelect) {
        $http({
          method: 'GET',
          url:'http://169.45.236.176:4000/api/v1/queues/?org_domain='+ org_domain+'&queue_id='+myQueueSelect
        //url: '../junk.json'
        })
        .success(function (data) {
            queue_items = data.data.queue_data;
            $scope.myInstructions = "Please enter your number"
            $scope.phoneStyle = {'visibility': 'visible'};
            $scope.qStyle = {'display': 'none'};
            $scope.myMessage = queue_items.length+" person/s are currently in line.";
            vm.queue_id = myQueueSelect;
        })
        .error(function () {
            // something went wrong :(
        });
    }
    $scope.stepThree = function() {
        var tel = $scope.telNumber;
        $log.debug(tel);
        if(typeof tel === 'undefined'){
            $scope.myMessage = "Incorrect Number Format";
        } else {
            $http({
            method: 'POST',
            data: $.param({phone_number: tel,queue_id:vm.queue_id}),
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            url: 'http://169.45.236.176:4000/api/v1/queues/users/'
          //url: '../junk.json'
            })
            .success(function (data) {
                $log.debug(data);
                vm.queue_number = data.data.queue_position;
                $scope.myInstructions = "You have been added to the line!";
                $scope.myNumber = "#"+vm.queue_number;
                $scope.phoneStyle = {'display': 'none'};
                $scope.myMessage = "";
            })
            .error(function () {
                $scope.myInstructions = "Oops something went wrong! :(";
                // something went wrong :(
            });
        }
    }
    $scope.reset = function() {
        $state.reload();
    }
  }
})();

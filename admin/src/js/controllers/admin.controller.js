(function () {
    'use strict';
    var apiUrl = 'http://169.45.236.176:4000';
    angular
        .module('virtualQueueApp')
        .controller('AdminController', ['$scope', '$stateParams', '$location', '$http', '$uibModal', AdminController])
        .controller('CreateModalInstanceController', ['$scope', '$uibModalInstance', ModalController])
        .controller('UpdateModalInstanceController', ['$scope', '$uibModalInstance', ModalController]);
        
    /* @ngInject */
    function ModalController($scope, $uibModalInstance) {
        $scope.submit = function () {
            $uibModalInstance.close($scope.queueName);
        };

        $scope.cancel = function () {
            $uibModalInstance.dismiss('cancel');
        };
    }
    /* @ngInject */
    function AdminController($scope, $stateParams, $location, $http, $uibModal) {
        $scope.orgDomain = $location.search().orgId;
        $scope.queues = [];


        var getOrg = function (orgDomain) {
            return $http({
                method: 'GET',
                url: apiUrl + '/api/v1/organization/',
                params: { 'org_domain': orgDomain }
            });
        };

        console.log($scope.orgDomain);
        getOrg($scope.orgDomain).then(function (response) {
            console.log(response.data);
            $scope.org = response.data.data;
        }, function (err) {
            console.log('Error making request: ' + err);
        });

        var serializeData = function (data) { 
            // If this is not an object, defer to native stringification.
            if (!angular.isObject(data)) {
                return ((data == null) ? "" : data.toString());
            }

            var buffer = [];

            // Serialize each key in the object.
            for (var name in data) {
                if (!data.hasOwnProperty(name)) {
                    continue;
                }

                var value = data[name];

                buffer.push(
                    encodeURIComponent(name) + "=" + encodeURIComponent((value == null) ? "" : value)
                    );
            }

            // Serialize the buffer and clean it up for transportation.
            var source = buffer.join("&").replace(/%20/g, "+");
            return (source);
        }
        $scope.deleteQueue = function (queue) {
            console.log(queue);
            $http({
                method: 'DELETE',
                url: apiUrl + '/api/v1/queues/',
                data: serializeData({
                    queue_id: queue.queue_id,
                    org_domain: $scope.orgDomain
                })

            }).success(function (data) {
                console.log(data);
            });
        }

        $scope.updateQueue = function (queue) {
            console.log(queue);
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'templates/update-queue.html',
                controller: 'UpdateModalInstanceController'
            });
            modalInstance.result.then(function (queueName) {

                console.log(queueName);
                var queueObj = {
                    'org_domain': $scope.orgDomain,
                    'queue_name': queueName,
                    'queue_id': queue.queue_id
                };
                $http({
                    method: 'PUT',
                    url: apiUrl + '/api/v1/queues/',
                    data: serializeData(queueObj),
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                }).success(function (data) {
                    console.log(data);
                });

            });
        };
        $scope.createModal = function () {

            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'templates/create-queue.html',
                controller: 'CreateModalInstanceController'
            });

            modalInstance.result.then(function (queueName) {

                console.log(queueName);
                var queueObj = {
                    'org_domain': $scope.orgDomain,
                    'queue_name': queueName,
                    'queue_group_id': 1
                };
                $http({
                    method: 'POST',
                    url: apiUrl + '/api/v1/queues/',
                    data: serializeData(queueObj),
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                }).success(function (data) {
                    console.log(data);
                });
                
                // $.ajax({
                //     url: apiUrl + '/api/v1/queues/',
                //     data: queueObj,
                //     method: 'POST',
                //     success: function (data) {
                //         console.log(data);
                //     }
                // });
            });
        };
        

        //  $scope.queues = queues;
       
    }
})();
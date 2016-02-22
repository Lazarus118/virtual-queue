'use strict';

/**
 * Route configuration for the RDash module.
 */
angular.module('virtualQueueApp').config(['$stateProvider', '$urlRouterProvider',
    function ($stateProvider, $urlRouterProvider) {

        // For unmatched routes
        $urlRouterProvider.otherwise('/admin/queues?orgId=scotia.virtualqueue.com');

        // Application routes
        $stateProvider
            .state('admin', {
                url: '/admin/queues?orgId',
                templateUrl: 'templates/admin.html',
                controller: 'AdminController'
            });
    }
]);
(function() {
  'use strict';

  angular
    .module('virtualQueue')
    .config(routerConfig);

  /** @ngInject */
  function routerConfig($stateProvider, $urlRouterProvider) {
    $stateProvider
      .state('home', {
        url: '/Side',
        templateUrl: 'app/main/main.html',
        controller: 'MainController',
        controllerAs: 'main'
      })
      $stateProvider
            .state('new', {
                url: '/New',
                templateUrl: 'app/main/newqueue.html',
                controller: 'NewController'
    })
    $urlRouterProvider
        .otherwise('/');
  }

})();

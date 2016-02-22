(function() {
  'use strict';

  angular
    .module('virtualQueue')
    .config(config);

  /** @ngInject */
  function config($logProvider, toastrConfig, ngIntlTelInputProvider) {
    // Enable log
    $logProvider.debugEnabled(true);

    // Set options third-party lib
    ngIntlTelInputProvider.set({defaultCountry: 'us'});
    toastrConfig.allowHtml = true;
    toastrConfig.timeOut = 3000;
    toastrConfig.positionClass = 'toast-top-right';
    toastrConfig.preventDuplicates = true;
    toastrConfig.progressBar = true;
  }

})();

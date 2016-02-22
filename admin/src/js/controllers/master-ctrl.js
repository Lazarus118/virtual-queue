/**
 * Master Controller
 */

angular.module('virtualQueueApp')
    .controller('MasterCtrl', ['$scope', '$cookieStore', '$location', MasterCtrl]);

function MasterCtrl($scope, $cookieStore, $location) {
    /**
     * Sidebar Toggle & Cookie Control
     */
    var mobileView = 992;

    $scope.getWidth = function() {
        return window.innerWidth;
    };

    $scope.$watch($scope.getWidth, function(newValue, oldValue) {
        if (newValue >= mobileView) {
            if (angular.isDefined($cookieStore.get('toggle'))) {
                $scope.toggle = ! $cookieStore.get('toggle') ? false : true;
            } else {
                $scope.toggle = true;
            }
        } else {
            $scope.toggle = false;
        }

    });

    $scope.isActive = function(bar) {
        var path = $location.path();
        console.log('Path', path, bar);
        if (bar === path) {
            return true;
        } else {
            return false;
        }
    }

    $scope.toggleSidebar = function() {
        $scope.toggle = !$scope.toggle;
        $cookieStore.put('toggle', $scope.toggle);
    };

    window.onresize = function() {
        $scope.$apply();
    };
}
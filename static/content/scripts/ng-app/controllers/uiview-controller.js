(function (ng) {

    function _uiViewCtrl($scope, $state, $titleSrv) {

        $scope.sidebar = {
            isCollapsed: false,
            menuItems: [
                { state: 'my.st', isActive: false },
                { state: 'my.cst', isActive: false },
                { state: 'my.clb', isActive: false },
                { state: 'my.gscpt', isActive: false }
            ],

            toggle: function () {
                this.isCollapsed = !this.isCollapsed;
            }
        };

        function setActiveState () {
            $scope.sidebar.menuItems.forEach(function (state) {
                state.isActive = $state.includes(state.state);
            })
        }

        /**
         * State change success event
         * https://github.com/angular-ui/ui-router/wiki#state-change-events
         * @param event
         * @param toState
         * @param toParams
         * @param fromState
         * @param fromParams
         */
        function onStateChangeSuccess (event, toState, toParams, fromState, fromParams) {
            setActiveState();
            $titleSrv.setTitle(toState.data.title)
        }

        $scope.$on('$stateChangeSuccess', onStateChangeSuccess);

        setActiveState();
    }

    _uiViewCtrl.$inject = ['$scope', '$state', '$titleSrv'];

    ng.module('mainApp')
        .controller('UiViewCtrl', _uiViewCtrl)

})(angular);

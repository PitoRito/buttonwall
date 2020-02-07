var simulator = angular.module('simulator', ['websocket', 'buttonwall.button']);

simulator.controller('buttonController', function($scope, $interval, $websocket) {
    $scope.buttons = {};

    $scope.$on("websocket.button.connect", function(event, buttons) {
        console.log(buttons);
        for (let [id, color] of Object.entries(buttons)) {
            id = parseInt(id);

            if(typeof $scope.buttons[id] === 'undefined') {
                $scope.buttons[id] = {id, color};
            }
            else {
                $scope.buttons[id].color = color;
            }
        }
        $scope.$apply();
    })

    $scope.$on("websocket.button.color", function(event, button) {
        button[0] = parseInt(button[0]);
        console.log(button);
        if(typeof $scope.buttons[button[0]] === 'undefined') {
            $scope.buttons[button[0]] = {id: button[0], color: button[1]};
        }
        else {
            $scope.buttons[button[0]].color = button[1];
        }
        $scope.$apply();
    })
});


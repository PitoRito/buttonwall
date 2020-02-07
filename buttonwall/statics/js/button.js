var lasergameGear = angular.module('buttonwall.button', []);
lasergameGear.component('bw', {
        templateUrl: "templates/button.tpl.html",
        bindings: {
            data: '<'
        },
        controller: function($scope, $websocket) {

            this.press = function() {
                $websocket.send({
                    button: this.data.id,
                    action: 'press',
                })
            }

            this.release = function() {
                $websocket.send({
                    button: this.data.id,
                    action: 'release',
                })
            }
        }
    }
);


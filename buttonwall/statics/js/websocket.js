var websocket = angular.module('websocket', []);
websocket.provider('$websocket', [function() {
    if(location.protocol === 'http:')
        this._url = `ws://${location.host}/api/websocket`;
    else
        this._url = `wss://${location.host}/api/websocket`;

    this.url = function(url) {
        _this._url = url;
    };


    this.$get = function($rootScope, $interval) {
        // console.log(this._url);

        class WebSock {
            constructor(url) {
                this._url = url;
                this._closed = true;
                $interval(this.checkConnection.bind(this), 1000);
            }

            start() {
                this._socket = new WebSocket(this._url);
                this._socket.onopen = this.open.bind(this);
                this._socket.onmessage = this.message.bind(this);
                this._socket.onclose = this.close.bind(this);
            }

            open() {
                this._closed = false;
                console.log("webSocket openened");
            }

            close() {
                this._closed = true;
            }

            checkConnection() {
                if(this._closed) {
                    console.log("Reconection: ", this._closed);
                    this.start();
                }
            }

            message(message) {
                // console.log("New data", message);
                let data = angular.fromJson(message.data);

                if (data.action === 'connect')
                    $rootScope.$broadcast('websocket.button.connect', data.body);

                if (data.action === 'color') {
                    $rootScope.$broadcast('websocket.button.color', [data.button, data.body]);
                }
            }

            send(data) {
                let msg = JSON.stringify(data);
                this._socket.send(msg);
            }
        }

        return new WebSock(this._url);
    };
}]);




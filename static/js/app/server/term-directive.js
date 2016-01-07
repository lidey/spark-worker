angular.module('app')
    .directive('term', ['$animate', function ($animate) {
        return {
            restrict: 'E',
            template: '<div></div>',
            replace: true,
            link: function ($scope, $element, $attrs) {
                var options = {};

                function WSSHClient() {
                }

                WSSHClient.prototype.connect = function (options) {

                    var endpoint = $attrs.uri;

                    if (window.WebSocket) {
                        this._connection = new WebSocket(endpoint);
                    }
                    else {
                        options.onError('WebSocket Not Supported');
                        return;
                    }

                    this._connection.onopen = function () {
                        options.onConnect();
                    };

                    this._connection.onmessage = function (evt) {
                        var data = JSON.parse(evt.data.toString());
                        if (data.error !== undefined) {
                            options.onError(data.error);
                        }
                        else {
                            options.onData(data.data);
                        }
                    };

                    this._connection.onclose = function (evt) {
                        options.onClose();
                    };
                };

                WSSHClient.prototype.send = function (data) {
                    this._connection.send(JSON.stringify({'data': data}));
                };

                var client = new WSSHClient();

                var term = new Terminal({
                    cols: 80,
                    rows: 24,
                    screenKeys: true
                });
                term.on('data', function (data) {
                    client.send(data);
                });
                term.open($element[0]);
                term.write('Connecting...');

                client.connect($.extend(options, {
                    onConnect: function () {
                        term.write('\r');
                    },
                    onData: function (data) {
                        term.write(data);
                    },
                    onError: function (error) {
                        term.write('Error: ' + error + '\r\n');
                    },
                    onClose: function () {
                        term.write('Connection Reset By Peer');
                        term.destroy();
                    }
                }));
            }
        };
    }]);
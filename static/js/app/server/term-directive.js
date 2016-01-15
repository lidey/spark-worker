angular.module('app')
    .directive('term', ['$animate', function ($animate) {
        return {
            restrict: 'E',
            template: '<div></div>',
            replace: true,
            link: function ($scope, $element, $attrs) {
                var options = {
                    endpoint: $attrs.uri
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
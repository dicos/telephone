(function (ng) {

    function _stCtrl($scope, $apiSrv, uiGridConstants) {

        $scope.stat = {
            period: {
                start: new Date().toRightDatetimeString(),
                end: new Date().toRightDatetimeString()
            },
            types: [],
            calls: [],
            stat: {}
        };
        $scope.gridOptions = {
            enableHorizontalScrollbar: 0,
            enableVerticalScrollbar: 0,
            enablePaginationControls: false,
            paginationPageSizes: [20],
            paginationPageSize: 20,
            rowHeight: 40,
            columnDefs: [
                { name: 'num', maxWidth: 20, displayName: '', enableColumnMenu: false, cellTemplate: '<div class="ui-grid-cell-contents">[[ grid.renderContainers.body.visibleRowCache.indexOf(row) + 1 ]]</div>' },
                { name: 'date', displayName: 'Дата', enableColumnMenu: false, cellTemplate: '<div class="ui-grid-cell-contents">[[ row.entity.date|date:"dd.MM.yyyy HH:mm:ss":"+0000" ]]</div>' },
                { name: 'call_type', maxWidth: 20, displayName: '', enableColumnMenu: false, cellTemplate: '<div class="ui-grid-cell-contents"><span class="[[ grid.appScope.formatType(grid, row) ]]" title="[[ grid.appScope.formatTypeLoclze(grid, row) ]]"></span></div>' },
                { name: 'sip', minWidth: 200, displayName: 'Номер звонящего', enableColumnMenu: false, cellTemplate: '<div popover ng-click="grid.appScope.cbPopover($event, row)" class="pointer ui-grid-cell-contents" ng-class="{\'text-bold\': row.entity.is_first_call}">[[ row.entity.sip ]]</div>' },
                { name: 'destination', displayName: 'Номер ответа', enableColumnMenu: false },
                { name: 'bill_seconds', displayName: 'Время разговора', enableColumnMenu: false, cellTemplate: '<div class="ui-grid-cell-contents">[[ grid.appScope.formatSec(grid, row) ]]</div>' },
                { name: 'rec', maxWidth: 80, minWidth: 80,  displayName: '', enableColumnMenu: false, cellTemplate: '<div data-call-id="[[ row.entity.call_id ]]">' +
		                    '<button class="btn-xs-wt btn btn-default margin-tb-10 margin-r-5" onclick="audio.action(event)"><span onclick="audio.action(event)" class="icon-play"></span></button>' +
		                    '<button class="btn-xs-wt btn btn-default margin-tb-10" onclick="audio.download(event)"><span class="icon-download"></span></button>' +
		                '</div>' },
                { name: 'cost', displayName: 'Цена минуты', enableColumnMenu: false },
                { name: 'bill_cost', displayName: 'Стоимость', enableColumnMenu: false },
                { name: 'description', displayName: 'Описание', enableColumnMenu: false }
            ],
            onRegisterApi: function (gridApi) {
                $scope.gridApi2 = gridApi;
            }
        };

        $scope.cbPopover = function ($event, row) {
            _initPopover();
        };

        $scope.changeStatType = function (type) {
            var index = $scope.stat.types.indexOf(type);
            if (index > -1) {
                $scope.stat.types.splice(index, 1);
            } else {
                $scope.stat.types.push(type);
            }
        };

        $scope.getPagesArr = function (totalPages) {
            return new Array(totalPages);
        };

        $scope.formatTypeLoclze = function (grid, row) {
            var disp = row.entity.disposition;
            switch (disp) {
                case 'answered':
                    return 'Отвечен';
                case 'busy':
                    return 'Занято';
                case 'cancel':
                    return 'Отменен';
                case 'no answer':
                    return 'Нет ответа';
                case 'failed':
                    return 'Неудачный';
                case 'no money':
                    return 'Нет средств';
                case 'unallocated number':
                    return 'Номара не существует';
                case 'no limit':
                    return 'Превышен лимит';
                case 'no day limit':
                    return 'Превышен дневной лимит';
                case 'line limit':
                    return 'Превышен лимит линии';
                default:
                    return '';
            }
        };

        $scope.formatType = function (grid, row) {
            var type = row.entity.call_type;
            var disp = row.entity.disposition;

            var icon = 'icon-' + (type === 'incoming' ? 'arrow-down' : (type === 'coming' ? 'arrow-up' : 'loop'));
            var status = 'text-' + (disp === 'answered' ? 'success' : 'error');

            return icon + ' ' + status;
        };

        $scope.formatSec = function(grid, row) {
            var value = row.entity.bill_seconds;
            var min = Math.floor(value / 60);
            var sec = value - min * 60;
            return (min > 0 ? min + ' мин ' : '') + (sec + ' сек');
        };

        $scope.getTableHeight = function() {
            var rowHeight = 40; // your row height
            var headerHeight = 40; // your header height
            return {
                height: ($scope.gridOptions.data.length * rowHeight + headerHeight) + "px"
            };
        };

        $scope.loadStat = function () {
            loadStat()
        };

        function onGetStatSuccess(response) {
            $scope.gridOptions.data = [];
            $scope.stat.calls = response.calls || [];
            $scope.gridOptions = { data: $scope.stat.calls };
        }

        function onGetStatError() {

        }

        function loadStat() {
            var status = $('input.pseudo-hidden[name=status]').val();
            var params = [
                'start=' + $scope.stat.period.start || new Date().toRightDatetimeString(),
                'end=' + $scope.stat.period.end || new Date().toRightDatetimeString(),
                'status=' + (Number(status).toString() == 'NaN' ? status : (status == 0 ? 2 : status - 1)),
                'call_type=' + $scope.stat.types.join(' ')
            ];
            var q = '?' + params.join('&');

            $apiSrv.getStat(q)
                .success(onGetStatSuccess)
                .error(onGetStatError);
        }

        loadStat();
    }

    _stCtrl.$inject = ['$scope', '$apiSrv', 'uiGridConstants'];

    ng.module('mainApp')
        .controller('StCtrl', _stCtrl)

})(angular);


function _initPopover() {
    $('[id^=webuiPopover]').remove();
    var elements = $('[popover]');
    for (var i = 0; i < elements.length; i++) {
        var el = $(elements[i]);
        var number = el.text();
        number = number[0] === '+' ? number.slice(1) : number;
        el.webuiPopover({
            cache: false,
            width: 185,
            animation: 'pop',
            placement: 'right',
            content: function (data) {
                var btn = '<button class="btn btn-sm-wt btn-default" type="button" style="width: 100%">Позвонить</button>' +
                    '<input type="hidden" value="' + data.phone + '" />';
                if (data.notAvalible) {
                    return '<div style="margin-bottom: 10px;" align="center">Не доступно</div>' + btn;
                }
                return '<div style="margin-bottom: 10px;">Стоимость: <strong>' + data.price.toFixed(2) + ' ' + data.currency + '</strong></div>' + btn;

            },
            type: 'async',
            url: '/getCallCost/?n=' + number
        })
            .on('shown.webui.popover', function (e, target) {
                target.find('button').on('click', function () {
                    $(this).attr('disabled', true).text('Соединение...');
                    setTimeout(function () {
                        services.call(target.find('input[type="hidden"]').val())
                            .then(function (result) {
                                message.success('Запрос отправлен. Ожидайте звонка')
                            })
                            .fail(function () {
                                message.error('Произошла ошибка. Повторите попытку');
                            })
                            .always(function () {
                                $('td[data-target="' + target.attr('id') + '"]').webuiPopover('hide')
                            });
                    }, 2000)
                })
            });
    }
}
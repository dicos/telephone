(function (services) {
    var costs = {
        to: undefined,
        from: undefined
    };

    function _getCallCost (phoneNumber, onSuccess, onFail) {
        var self = this;
        if (phoneNumber != '' && phoneNumber.match(/[0-9]{9,}/)) {
            $.get('/getCallCost/?n=' + phoneNumber, function (result) {
                services.executeCallback(onSuccess, [result, self])
            }).fail(function () {
                services.executeCallback(onFail)
            })
        }
    }

    function _onGetCallCostSuccess (params) {
        var result = params[0];
        var ctx = params[1];
        var direction = $(ctx).attr('id') === 'cbToNumber' ? 'to' : 'from';
        for (var i in result) {
            if (result.hasOwnProperty(i)) {
                var target = $('#call-' + direction +'-info-' + i);
                if (target.length > 0) {
                    target.text(result[i])
                }
            }
        }
        costs[direction] = result.price;
        if (costs.to != undefined && costs.from != undefined) {
            $('#total-cost').text((costs.to + costs.from) + ' RUB')
        }
        $('#error.error-text').text('')
    }

    function _call() {
        var cbToNumber = $('#cbToNumber').val();
        var cbFromNumber = $('#cbFromNumber').val();
        if (cbToNumber == '' || !cbToNumber.match(/[0-9]{9,}/) || cbFromNumber == '' || !cbFromNumber.match(/[0-9]{9,}/)) {
            $('#error.error-text').text('Неправильный номер телефона');
            return false;
        }
        $('#call-status').attr('style', 'display: block');
        setTimeout(function () {
            $.get('/requestCallback/?cbFromNumber=' + cbFromNumber + '&cbToNumber=' + cbToNumber)
                .then(function (result) {
                    message.success('Запрос отправлен. Ожидайте звонка')
                })
                .fail(function (err) {
                    message.error('Произошла ошибка. Повторите попытку');
                }).always(function () {
                    $('#modal').modal('toggle');
                })
        }, 4000)

    }

    function _onElementBlur (e) {
        var number = $(this).val();
        _getCallCost.apply(this, [number, _onGetCallCostSuccess]);
    }

    $(document).ready(function () {
        var cbToNumberElement = $('#cbToNumber');
        var cbFromNumberElement = $('#cbFromNumber');

        cbFromNumberElement.on('blur', _onElementBlur);
        cbToNumberElement.on('blur', _onElementBlur);

        var number = cbToNumberElement.val();
        _getCallCost.apply(cbToNumberElement[0], [number, _onGetCallCostSuccess]);

        var callbackBtn = $('#callback-call');
        callbackBtn.on('click', function () {
            _call();
        })
    })
})(services);
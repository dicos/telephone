/**
 * Convert date to string formatted as 'dd.mm.yyyy'
 * @returns {string}
 */
Date.prototype.toRightDatetimeString = function () {
    var day = this.getDate().toString();
    var month = (this.getMonth() + 1).toString();
    var date = [
        day.length < 2 ? '0{0}'.format(day) : day ,
        month.length < 2 ? '0{0}'.format(month) : month,
        this.getFullYear().toString()
    ];
    return String(date.join('.'));
};

/**
 * Creates an instance of Date class with current date value
 * @returns {Date}
 */
Date.getNowDate = function () {
    return new Date(Date.now());
};

/**
 * Extends String prototype with format function. Template: {number}
 * @returns {string}
 */
String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) {
        return typeof args[number] != 'undefined' ? args[number] : match;
    });
};

$.prototype.showElement = function (delay) {
    this.fadeIn(delay || 200);
};

$.prototype.hideElement = function (delay, onEnd) {
    this.fadeOut(delay || 200, onEnd);
};

$.prototype.setVisible = function (delay) {
    this.animate({
        opacity: 1
    }, delay || 200)
};

$.prototype.setInvisible = function (delay, onEnd) {
    this.animate({
        opacity: 0
    }, delay || 200, onEnd)
};

function Period(from, to, maxDate) {
    this._maxDate = maxDate || new Date(Date.now());
    this._from = from || new Date(Date.now());
    this._to = to || new Date(Date.now());
}

Period.prototype = {
    constructor: Period,

    getMaxDate: function () {
        return this._maxDate;
    },

    getFromDate: function () {
        return this._from;
    },

    getToDate: function () {
        return this._to;
    },

    setToDate: function (value) {
        if (value instanceof Date) {
            this._to = value;
        } else {
            throw new TypeError('value is not an instance of Date');
        }
    },

    getDatesDifferent: function () {
        var timeDiff = this._to.getTime() - this._from.getTime();
        return Math.ceil(timeDiff / (1000 * 3600 * 24));
    },

    toPeriodString: function (locale) {
        if (this._from.toDateString() == new Date(Date.now()).toDateString()) {
            return 'сегодня';
        }
        if (this._from.toDateString() == this._to.toDateString()) {
            return this._from.toRightDatetimeString()
        }
        return 'период с ' + this._from.toRightDatetimeString() + ' по ' + this._to.toRightDatetimeString();
    }
};

function ApiParams(params) {
    this._params = {
        // Start date: 'YYYY-MM-dd HH:mm:ss' *Required*
        'start': Date.getNowDate().toRightDatetimeString(),
        // End date (inclusively): 'YYYY-MM-dd HH:mm:ss' *Required*
        'end': Date.getNowDate().toRightDatetimeString()
    };

    this._init(params);
}

ApiParams.prototype = {
    constructor: ApiParams,

    _init: function (params) {
        for (var param in params) {
            if (params.hasOwnProperty(param)) {
                this._params[param] = params[param];
            }
        }
    },

    setParams: function (params) {
        this._init(params);
    },

    getRequestString: function () {
        var str = '?';
        for (var param in this._params) {
            if (this._params.hasOwnProperty(param)) {
                str += param + '=' + this._params[param] + '&';
            }
        }
        return str.slice(0, -1);
    }
};
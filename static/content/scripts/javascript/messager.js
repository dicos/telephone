var message = (function () {
    function Message () {
        this._element = {};
        this._id = 'messager';
        this._template = '<div id="' + this._id + '" align="center" style="display: none; cursor: pointer"></div>'
        this._timeoutId = null;
    }

    Message.prototype = {
    	constructor: Message,

        _initElement: function () {
            var element = $('#' + this._id);
            if (element[0]) {
                this._element = element;
                this._element.on('click', this._hide.bind(this));
                return 0;
            }
            $('header').prepend(this._template);
            this._initElement();
        },

        _setValues: function (text, type) {
            this._element.addClass('message-' + type);
            this._element.text(text);
        },

        _hide: function (e) {
            this._initElement();
            if (this._element.attr('style').indexOf('display: none') == -1) {
                this._element.fadeOut(200, function () {
                    this._element.removeClass();
                    this._element.text('');
                    if (this._timeoutId) {
                        clearTimeout(this._timeoutId);
                        this._timeoutId = null;
                    }
                }.bind(this));
            }
        },

        _show: function (text, type) {
            this._initElement();
            this._setValues(text, type);
            var _that = this;
            this._element.fadeIn(200, function () {
                _that._timeoutId = setTimeout(function () { _that._hide.apply(_that) }, 7000);
            });
        },

        success: function (text) {
            this._show(text, 'success');
        },

        warning: function (text) {
            this._show(text, 'warning');
        },

        error: function (text) {
            this._show(text, 'error');
        },

        info: function (text) {
            this._show(text, 'info');
        }
    };

    return new Message();
})();
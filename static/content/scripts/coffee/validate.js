// Generated by CoffeeScript 1.9.3
var validate;

validate = (function() {
  var errorElementCssClass, errorMessageCssClass, isElementHasError;
  errorElementCssClass = 'error';
  errorMessageCssClass = 'error-text';
  isElementHasError = function(element) {
    return element.hasClass(errorElementCssClass);
  };
  return {
    getErrorMessageHTML: function(arr) {
      var errorsHTML;
      errorsHTML = '';
      arr.forEach(function(error) {
        errorsHTML += '<span class="' + errorMessageCssClass + '">' + error + '</span>';
      });
      return errorsHTML;
    },
    showError: function(element, errorHTML) {
      if (isElementHasError(element)) {
        this.hideError(element);
      }
      element.addClass(errorElementCssClass);
      element.after(errorHTML);
    },
    hideError: function(element) {
      var nextElement;
      if (isElementHasError(element)) {
        element.removeClass(errorElementCssClass);
        nextElement = element.next();
        if (nextElement.hasClass(errorMessageCssClass)) {
          nextElement.remove();
        }
      }
    }
  };
})();

//# sourceMappingURL=validate.js.map

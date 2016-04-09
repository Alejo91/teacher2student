/**
 * The functions below will create a header with csrftoken
 */
var django_csrf_tools = {
    'getCookie' : function (name) {
        // This function gets cookie with a given name
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },
    'csrfSafeMethod': function (method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
};

$(document).ready (function () {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!django_csrf_tools.csrfSafeMethod(settings.type)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken",  django_csrf_tools.getCookie('csrftoken'));
            }
        }
    });
});

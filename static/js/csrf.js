// Pulls django csrf token from page for use with ajax requests

// Code Credit: Emad Mokhtar @ stackoverflow
// https://stackoverflow.com/questions/35112451/forbidden-csrf-token-missing-or-incorrect-django-error/35113457
// CSRF token for django

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != "") {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == name + "=") {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie("csrftoken");

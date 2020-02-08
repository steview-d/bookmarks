/*
Tooltip configuration and customisation using the tippy.js library
https://github.com/atomiks/tippyjs
*/

$(document).ready(function() {

    // show full bookmark description text
    tippy('.tippy-desc', {
        allowHTML: false,
        delay: 700,
        theme: 'dark',
        onShow(instance) {
            instance.setContent(instance.reference.innerText);
        }
    });

    // show help text for register account form fields
    tippy('.tippy-register-help', {
        onShow(instance) {
            const el = $(instance.reference.nextElementSibling).find('.tippy-help-text');
            instance.setContent(el[0].dataset.helptext);
        }
    });
});

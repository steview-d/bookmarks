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
        theme: 'dark',
        onShow(instance) {
            const el = $(instance.reference.nextElementSibling).find('.tippy-help-text');
            instance.setContent(el[0].dataset.helptext);
        }
    });

    // show help text for set password form field
    tippy('.tippy-set-pw-help', {
        theme: 'dark',
        onShow(instance) {
            const el = $(instance.reference.nextElementSibling).find('.tippy-help-text');
            instance.setContent(el[0].dataset.helptext);
        }
    });
});

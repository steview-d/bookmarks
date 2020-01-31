/*
Tooltip configuration and customisation using the tippy.js library
https://github.com/atomiks/tippyjs
*/

$(document).ready(function() {

    tippy('.tippy-desc', {
        content: 'Fetching description',
        allowHTML: false,
        delay: 700,
        theme: 'dark',
        onShow(instance) {
            instance.setContent(instance.reference.innerText);
        }
    });

});
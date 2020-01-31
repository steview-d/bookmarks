/*
Tooltip configuration and customisation using the tippy.js library
https://github.com/atomiks/tippyjs
*/

$(document).ready(function() {

    tippy('.tippy', {
        content: 'Fetching description',
        delay: 500,
        onShow(instance) {
            instance.setContent(instance.reference.innerText);
        }
    });

});
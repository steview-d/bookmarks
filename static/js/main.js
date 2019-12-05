$(document).ready(function () {

    // sidebar toggler
    $('.sidebarToggle').on('click', function () {
        $('#sidebar, #content').toggleClass('display-switch');
    });

    // add new page form toggle
    $('#add-page-btn').on('click', function() {
        $(this).next().slideToggle(200);
    });
});

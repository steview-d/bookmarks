$(document).ready(function () {

    // sidebar toggler
    $('.sidebarToggle').on('click', function () {
        $('#sidebar, #content').toggleClass('display-switch');
    });

    // 'add new page' form toggle
    $('#add-page-btn').on('click', function() {
        $(this).next().slideToggle(200);
    });

    // 'edit page' form toggle
    $('.edit-page-btn').on('click', function() {
        $(this).parent().parent().next().slideToggle(200);
    });

    // submit 'delete page form' from modal
    $('#delete-page-form').on('click', function() {
        $(this).submit();
    });

    // submit 'delete collection form' from modal
    $('#delete-collection-form').on('click', function() {
        $(this).submit();
    });
});

// --------------------------------

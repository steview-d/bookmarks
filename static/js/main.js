$(document).ready(function() {
    // sidebar toggler
    $(".sidebarToggle").on("click", function() {
        $("#sidebar, #content").toggleClass("display-switch");
    });

    // 'add new page' form toggle
    $("#add-page-btn").on("click", function() {
        $(this)
            .next()
            .slideToggle(200);
    });

    // 'edit page' form toggle
    $(".edit-page-btn").on("click", function() {
        // $('.qqq')
        $('.edit-page-form').slideToggle(200);
    });

    // submit 'delete page form' from modal
    $("#delete-page-form").on("click", function() {
        $(this).submit();
    });

    // submit 'delete collection form' from modal
    $("#delete-collection-form").on("click", function() {
        $(this).submit();
    });

    // --------------------------------
    // Page Sorting
    // --------------------------------
    $("#page-titles").sortable({
        containment: "#page-sort-container", // Need to make bigger
        // containment: ui.item.parent().attr('id'),
        cursor: "grabbing",
        axis: "y",
        stop: function() {
            var data = $(this).sortable("serialize");
            data = data.split("[]=.");
            data.pop();

            var newOrder = data.map(i => {
                return i.replace("&", "");
            });

            postData = newOrder.join(",");

            $.ajax({
                // data: postData,
                type: "POST",
                dataType: "json",
                data: {
                    new_page_order: postData,
                    csrfmiddlewaretoken: csrftoken
                },
                url: "page_sort",
                success: function(data) {
                    if (data.success) {
                        location.reload();
                    }
                }
            });
        }
    });

});

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
        $(".edit-page-form").slideToggle(200);
    });

    // submit 'delete page form' from modal
    $("#delete-page-form").on("click", function() {
        $(this).submit();
    });

    // submit 'delete collection form' from modal
    $("#delete-collection-form").on("click", function() {
        $(this).submit();
    });

    // Page Sorting
    // Use jQueryUI to sort page names then send new order
    // for processing using ajax
    $("#page-titles").sortable({
        containment: "#page-sort-container",
        delay: 200,
        cursor: "grabbing",
        axis: "y",
        stop: function() {
            let data = $(this).sortable("serialize");
            data = data.split("[]=.");
            data.pop();

            let newOrder = data.map(i => {
                return i.replace("&", "");
            });

            postData = newOrder.join(",");

            $.ajax({
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

    var qqq = [[], [], [], [], []];
    function buildList(columnNum, columnData) {
        qqq[columnNum-1] = columnData;
        return;
    }

    function collection_order_ajax_call() {
        // tbc....
    }

    // Collection Sorting
    $("#column-1").sortable({
        containment: "#collections-container",
        cursor: "grabbing",
        connectWith: ['#column-1, #column-2', '#column-3', '#column-4', '#column-5'],
        deactivate: function() {
            let data = $(this).sortable("serialize");
            data = data.split("[]=.");
            data.pop();

            let newOrder = data.map(i => {
                return i.replace("&", "");
            });
            columnData = newOrder.join(",");
            buildList(1, columnData);
        },
        stop: function() {
            postData = JSON.stringify(qqq);
            console.log("HERE!!!!: ", postData);
            console.log(typeof(postData));

            $.ajax({
                type: "POST",
                dataType: "json",
                data: {
                    new_collection_order: postData,
                    csrfmiddlewaretoken: csrftoken
                },
                url: "collection_sort",
                success: function(data) {
                    if (data.success) {
                        location.reload();
                    }
                }
            });
        }

    });
    $("#column-2").sortable({
        containment: "#collections-container",
        connectWith: ['#column-1, #column-2', '#column-3', '#column-4', '#column-5'],
        deactivate: function() {
            let data = $(this).sortable("serialize");
            data = data.split("[]=.");
            data.pop();

            let newOrder = data.map(i => {
                return i.replace("&", "");
            });
            columnData = newOrder.join(",");
            buildList(2, columnData);
        },
        stop: function() {
            console.log(qqq);
        }

    });
    $("#column-3").sortable({
        containment: "#collections-container",
        connectWith: ['#column-1, #column-2', '#column-3', '#column-4', '#column-5'],
        deactivate: function() {
            let data = $(this).sortable("serialize");
            data = data.split("[]=.");
            data.pop();

            let newOrder = data.map(i => {
                return i.replace("&", "");
            });
            columnData = newOrder.join(",");
            buildList(3, columnData);
        },
        stop: function() {
            console.log(qqq);
        }

    });
    $("#column-4").sortable({
        containment: "#collections-container",
        connectWith: ['#column-1, #column-2', '#column-3', '#column-4', '#column-5'],
        deactivate: function() {
            let data = $(this).sortable("serialize");
            data = data.split("[]=.");
            data.pop();

            let newOrder = data.map(i => {
                return i.replace("&", "");
            });
            columnData = newOrder.join(",");
            buildList(4, columnData);
        },
        stop: function() {
            console.log(qqq);
        }

    });
    $("#column-5").sortable({
        containment: "#collections-container",
        connectWith: ['#column-1, #column-2', '#column-3', '#column-4', '#column-5'],
        deactivate: function() {
            let data = $(this).sortable("serialize");
            data = data.split("[]=.");
            data.pop();

            let newOrder = data.map(i => {
                return i.replace("&", "");
            });
            columnData = newOrder.join(",");
            buildList(5, columnData);
        },
        stop: function() {
            console.log(qqq);
        }

    });
});

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

    // Page Sorting ---------------------------------------------------------//
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

    // Collection Sorting ---------------------------------------------------//
    // Use jQueryUI to sort collections into preferred columns and positions
    // and then send new order for processing using ajax

    // var new_collection_order = [[], [], [], [], []];
    var new_collection_order = [];
    function buildList(columnNum, columnData) {
        // new_collection_order[columnNum-1] = columnData;
        new_collection_order[columnNum] = columnData;
        console.log(new_collection_order);
        return;
    }

    var column_list = [
        "#column-1",
        "#column-2",
        "#column-3",
        "#column-4",
        "#column-5"
    ];

    column_list.forEach((key, idx) => {
        $(key).sortable({
            containment: "#collections-container",
            cursor: "grabbing",
            connectWith: [
                "#column-1, #column-2",
                "#column-3",
                "#column-4",
                "#column-5"
            ],
            deactivate: function() {
                let data = $(this).sortable("serialize");
                data = data.split("[]=.");
                data.pop();

                let newOrder = data.map(x => {
                    return x.replace("&", "");
                });
                columnData = newOrder.join(",");
                buildList(idx, columnData);
            },
            stop: function() {
                let postData = JSON.stringify(new_collection_order);
                // send the new collection orders to the server
                $.ajax({
                    type: "POST",
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
    });
});

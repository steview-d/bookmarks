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
        // console.log("Build List! ", columnData);
        qqq[columnNum-1] = columnData;
        return qqq;

        
    }

    // Collection Sorting
    $("#column-1").sortable({
        containment: "#collections-container",
        connectWith: ['#column-1, #column-2', '#column-3', '#column-4', '#column-5'],
        deactivate: function(event, ui) {
            let data = $(this).sortable("serialize");
            data = data.split("[]=.");
            data.pop();
            console.log(event, ui);

            let newOrder = data.map(i => {
                return i.replace("&", "");
            });
            columnData = newOrder.join(",");
            console.log("C1: ", columnData);
            buildList(1, columnData);
        },
        stop: function() {
            console.log(columnData);
            console.log(qqq);
        }

    });
    $("#column-2").sortable({
        containment: "#collections-container",
        connectWith: ['#column-1, #column-2', '#column-3', '#column-4', '#column-5'],
        deactivate: function(event, ui) {
            let data = $(this).sortable("serialize");
            data = data.split("[]=.");
            data.pop();
            console.log(event, ui);

            let newOrder = data.map(i => {
                return i.replace("&", "");
            });
            columnData = newOrder.join(",");
            console.log("C2: ", columnData);
            buildList(2, columnData);
        },
        stop: function() {
            console.log(columnData);
            console.log(qqq);
        }

    });
    $("#column-3").sortable({
        containment: "#collections-container",
        connectWith: ['#column-1, #column-2', '#column-3', '#column-4', '#column-5'],
        deactivate: function(event, ui) {
            let data = $(this).sortable("serialize");
            data = data.split("[]=.");
            data.pop();
            console.log(event, ui);

            let newOrder = data.map(i => {
                return i.replace("&", "");
            });
            columnData = newOrder.join(",");
            console.log("C3: ", columnData);
            buildList(3, columnData);
        },
        stop: function() {
            console.log(columnData);
            console.log(qqq);
        }

    });
    $("#column-4").sortable({
        containment: "#collections-container",
        connectWith: ['#column-1, #column-2', '#column-3', '#column-4', '#column-5'],
        deactivate: function(event, ui) {
            let data = $(this).sortable("serialize");
            data = data.split("[]=.");
            data.pop();
            console.log(event, ui);

            let newOrder = data.map(i => {
                return i.replace("&", "");
            });
            columnData = newOrder.join(",");
            console.log("C4: ", columnData);
            buildList(4, columnData);
        },
        stop: function() {
            console.log(columnData);
            console.log(qqq);
        }

    });
    $("#column-5").sortable({
        containment: "#collections-container",
        connectWith: ['#column-1, #column-2', '#column-3', '#column-4', '#column-5'],
        deactivate: function(event, ui) {
            let data = $(this).sortable("serialize");
            data = data.split("[]=.");
            data.pop();
            console.log(event, ui);

            let newOrder = data.map(i => {
                return i.replace("&", "");
            });
            columnData = newOrder.join(",");
            console.log("C5: ", columnData);
            buildList(5, columnData);
        },
        stop: function() {
            console.log(columnData);
            console.log(qqq);
        }

    });
});

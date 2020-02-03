$(document).ready(function() {

    // --------------------------------------------------- Buttons & Toggles //

    // sidebar toggler
    $(".sidebarToggle").on("click", function() {
        $("#sidebar, #content").toggleClass("display-switch");
        $("#content").toggleClass("no-scroll");
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

    // rename collection toggle
    $(".rename-collection").on("click", function() {
        $(this)
            .parent()
            .parent()
            .next()
            .slideToggle(200);
    });

    // bookmark options menu
    $(".bm-icon-toggle").on("click", function(e) {
        e.preventDefault();
        $(this)
            .children(":first")
            .toggleClass("fa-caret-down fa-caret-up");
        $(this)
            .parent()
            .parent()
            .parent()
            .next()
            .slideToggle();
    });

    // Scrape Url button
    $("#scrape-url").on("click", scrapeUrl);


    // ---------------------------------------------------------------- Page //

    /*
    Use jQueryUI 'sortable' to sort elements containing page names. When a page
    has been dropped into it's new position, serialize creates a text string
    which is then formatted and posted to the _page_sort view with ajax.

    '_page_sort' updates the db with the new page position values and on a
    successful return, the page is reloaded with the new page order.
    */

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

            // turn on spinner
            $('#ajax-progress-page').toggleClass("ajax-progress-hide ajax-progress-show");

            $.ajax({
                type: "POST",
                data: {
                    new_page_order: postData,
                    csrfmiddlewaretoken: csrftoken
                },
                url: "/app/_page_sort",
                success: function(data) {
                    if (data.success) {
                        // turn off spinner
                        $('#ajax-progress-page').toggleClass("ajax-progress-hide ajax-progress-show");
                        location.reload();
                    }
                }
            });
        }
    });


    // ---------------------------------------------------------- Collection //

    /*
    Using jQueryUI sortable, multiple columns are linked together and when the
    user moves a collection into a new position, serialize creates a text
    string which is then formatted and posted to the collection_sort view with
    ajax.

    'collection_sort' updates the db with the new collection position values
    and on a successful return, the page is reloaded with the new order.
    */

    let new_collection_order = [];
    function buildList(columnNum, columnData) {
        new_collection_order[columnNum] = columnData;
        return;
    }

    let column_list = [
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
                "#column-1",
                "#column-2",
                "#column-3",
                "#column-4",
                "#column-5"
            ],
            deactivate: function() {
                let data = $(this).sortable("serialize");
                data = data.split("[]=.");
                data.pop();

                let newOrder = data.map(i => {
                    return i.replace("&", "");
                });
                let columnData = newOrder.join(",");
                buildList(idx, columnData);
            },
            stop: function(event, ui) {
                let postData = JSON.stringify(new_collection_order);

                // turn on spinner
                $('#ajax-progress-arrange').toggleClass("ajax-progress-hide ajax-progress-show");

                $.ajax({
                    type: "POST",
                    data: {
                        new_collection_order: postData,
                        collection_id: ui.item[0].id,
                        csrfmiddlewaretoken: csrftoken
                    },
                    url: "collection-sort",
                    success: function(data) {
                        if (data.success) {
                            // turn off spinner
                            $('#ajax-progress-arrange').toggleClass("ajax-progress-hide ajax-progress-show");
                            location.reload();
                        }
                    }
                });
            }
        });
    });


    // ------------------------------------------------------------ Bookmark //

    /*
    Use jQueryUI 'sortable' to sort bookmark elements within a collection.
    When a bookmark has been placed into it's new position, serialize creates a
    text string of the positions for all bookmarks in the collection which is
    then formatted and posted to the 'bookmark_sort_manual' view with ajax.

    'bookmark_sort_manual' updates the db with the new bookmark position values
    and on a successful return, the page is reloaded with the new order.
    */

    $(".bookmark-sort").sortable({
        items: "li",
        containment: "parent",
        delay: 200,
        cursor: "grabbing",
        axis: "y",
        stop: function(event, ui) {
            if ($(this).hasClass("no-manual-sort")) {
                let page = $(this).closest("div.page-name").attr("id");
                let message = `Bookmark sorting is disabled 
                    when not in 'Manual Sort' mode.`;
                window.location = page + "/custom_message/" + message;
            } else {
                let data = $(this).sortable("serialize");
                data = data.split("[]=.");
                data.pop();

                let newOrder = data.map(i => {
                    return i.replace("&", "");
                });

                postData = newOrder.join(",");

                // turn on spinner
                $('#ajax-progress-bookmark').toggleClass("display-toggle");

                $.ajax({
                    type: "POST",
                    data: {
                        new_bookmark_order: postData,
                        collection_name: ui.item
                            .closest("div.collection-name")
                            .attr("id"),
                        page_name: ui.item.closest("div.page-name").attr("id"),
                        csrfmiddlewaretoken: csrftoken
                    },
                    url: "_bookmark_sort_manual",
                    success: function(data) {
                        if (data.success) {
                            // turn off spinner
                            $('#ajax-progress-bookmark').toggleClass("display-toggle");
                            location.reload();
                        }
                    }
                });
            }
        }
    });


    // -------------------------------------------------------- Url Scraping //

    /*
    Sends the url to the server for scraping with BeautifulSoup4. The view will
    return values for the title & description, as well as a message that
    states either the scrape was a success, or the reason why it wasn't.
    */

    function scrapeUrl() {
        let urlToScrape = $("#id_url").val();

        // if url doesn't begin with http(s), prepend it
        let httpRe = new RegExp('^https?://');
        let match = httpRe.test(urlToScrape);
        if (!match) {
            urlToScrape = 'https://' + urlToScrape;
            $("#id_url").val(urlToScrape);
        }

        $("#scrape-url").text('SCRAPING..');
        
        $.ajax({
            type: "POST",
            data: {
                urlToScrape: urlToScrape,
                csrfmiddlewaretoken: csrftoken
            },
            url: "/app/_manual_url_scrape",
            success: function(data) {
                // populate text fields
                $("#id_title").val(data.title);
                $("#id_description").val(data.description);
                $("#scrape-msg").text(data.message);
                $("#id_icon").val('');

                // populate image fields
                if (data.scraped_image) {
                    let base64Str = 'data:image/' + data.image_ext + ';base64,' + data.scraped_image;
                    $("#img-preview").attr('src', base64Str);
                    $("#scraped_img").val(base64Str);
                } else {
                    $("#img-preview").attr('src', '/static/img/icon/no_img_scrape.png');
                    $("#scraped_img").val('');
                }
                $("#scrape-url").text('Scrape URL');
            },
            error: function() {
                $("#scrape-url").text('Scrape URL');
            }
        });
    }

    // ----------------------------- Check URL in '#id_url' is valid //

    /*
    Sends a url to the server with ajax for processing via the python requests
    module and returns 1 of the following responses
    True: URL resolves successfully
    False : URL could not be resolved
    None: Nothing to resolve, most likely an empty field
    */

    let urlTimer;
    let timerLength = 1000;

    $("#id_url").keyup(function() {
        clearTimeout(urlTimer);
        urlTimer = setTimeout(checkURL, timerLength);
    });

    function checkURL() {
        let urlToCheck = $("#id_url").val();

        $.ajax({
            type: "POST",
            data: {
                urlToCheck: urlToCheck,
                csrfmiddlewaretoken: csrftoken
            },
            url: "/app/_check_valid_url",
            success: function(data) {
                switch (data.result) {
                    case true:
                        $("#url-validation-result").text("Url status: Valid");
                        break;
                    case false:
                        $("#url-validation-result").text("Url status: Invalid");
                        break;
                    default:
                        $("#url-validation-result").text(
                            "Url status: URL field is empty"
                        );
                }
            }
        });
    }


    // --------------------------------------------------------------- Other //

    /*
    Listen for changes on the page choice dropdown input. When a change is
    detected, the pk for that page is sent to the server via ajax.

    The server will process this pk by getting the collections for the new page
    and sending them back as an html string. The ajax success call will then
    replace the old html choices with the new ones that were returned.
    */

    $("#id_dest_page").change(function() {
        let newPagePk = $(this).val();
        $.ajax({
            type: "POST",
            data: {
                newPagePk: newPagePk,
                csrfmiddlewaretoken: csrftoken
            },
            url: "/app/_update_collection_list",
            success: function(data) {
                $("#id_dest_collection").html(data.html);
            }
        });
    });

    // Collection Display Mode ajax control

    /*
    Listens for a click on the bookmark display mode buttons. When clicked,
    ajax posts the clicked collection and requested display mode to the server.

    On a successful return, the page is update to show the new display mode.
    */
    $(".coll-display-btn").click(function() {
        let collection = $(this).data("coll-id");
        let mode = $(this).data("display-mode");
        $.ajax({
            type: "POST",
            data: {
                collection: collection,
                mode: mode,
                csrfmiddlewaretoken: csrftoken
            },
            url: "/app/_change_collection_display",
            success: function() {
                location.reload();
            }
        });
    });

    // Image Upload Preview

    /*
    Listens for a change to the file input element, and when a change is
    registered, a preview of the uploaded file is displayed
    */
    $('#id_icon').change(function () {
        if (this.files && this.files[0]) {
            let preview = new FileReader();

            preview.onload = function (e) {
                $('#img-preview').attr('src', e.target.result);
            };

            console.log(this.files);

            preview.readAsDataURL(this.files[0]);
        }
    });
});

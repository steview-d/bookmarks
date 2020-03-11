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
            .parent()
            .next()
            .children()
            .slideToggle(200);
        $(this)
            .children('i')
            .toggleClass('fa-plus fa-chevron-down');
        // $('#page-titles').toggleClass('display-toggle');
    });

    // 'edit page' form toggle
    $(".edit-page-btn").on("click", function() {
        $(".edit-page-form").slideToggle(200);
    });

    // submit 'delete page form' from modal
    // $("#delete-page-form").on("click", function() {
    //     $(this).submit();
    // });

    // submit 'delete collection form' from modal
    // $("#delete-collection-form").on("click", function() {
    //     $(this).submit();
    // });

    // rename collection toggle
    $(".btn--collection-options").on("click", function() {
        $(this)
            .parent()
            .parent()
            .next()
            .slideToggle(200);
    });

    // bookmark options menu
    // can likely delete if not in use
    // used in 2 places - main app display & search page
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
        containment: "parent",
        delay: 200,
        cursor: "grabbing",
        axis: "y",
        handle: ".page-sort-handle",
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

    // When the 'Page Sort' button is toggled, toggle the 'page-sort-handle' class required
    // by sortable to allow sorting of pages. 
    $('#page-sort-btn').on('click', function () {
        $('.page-sort-icon-container').toggleClass('hide-page-sort-icon');
        $('.page-sort-handle-container').toggleClass('page-sort-handle');
        $(this).toggleClass('page-sort-active');
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
        handle: ".bm-sort-handle",
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

    // When the 'Bookmark Sort' button is toggled, toggle the 'bm-sort-handle' class required
    // by sortable to allow sorting of bookmarks. 
    const bmSortButtons = document.querySelectorAll("[id^='bm-sort-btn-']");
    bmSortButtons.forEach((key) => {
        $(key).on('click', function () {
            const el = $(this).parent().parent().parent();
            el.find('.bm-handle-container')
                .toggleClass('bm-sort-handle');
            el.find('.bookmark-styling')
                .toggleClass('bookmark-border');
            el.find('.bm-options-icon')
                .toggleClass('display-toggle');
            $(this).toggleClass('manual-sort-on');

            // check if single column, and add scroll space
            if (typeof num_columns !== 'undefined') {
                if (num_columns == 1) {
                    $(this)
                        .parent()
                        .parent()
                        .parent()
                        .find('.bm-handle-container')
                        .toggleClass('add-scroll-space');
                }
            }
        });
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
                $("#scrape-msg").html(`Autofill result: <strong>` + data.message + `</strong>`);
                // clear icon field file incase of previously selected image
                $("#id_icon").val('');

                // populate image fields
                if (data.scraped_image) {
                    let base64Str = 'data:image/' + data.image_ext + ';base64,' + data.scraped_image;
                    $("#img-preview").attr('src', base64Str);
                    $("#scraped_img").val(base64Str);
                } else {
                    $("#img-preview").attr('src', '/static/img/no_img_scrape.png');
                    $("#scraped_img").val('');
                }
                $("#scrape-url").html('<i class="fa fa-magic" aria-hidden="true"></i>AUTOFILL');

                // if an image is scraped, hide the default icon and show scraped image
                if ($('#edit-bookmark, #add-bookmark, #import-url').length && $('#img-preview')[0].src) {
                    $('#img-preview').removeClass('icon-display-hide');
                    $('#default-icon').addClass('icon-display-hide');
                    // also clear value inside file upload field
                    $("#id_icon").next().text('Choose file');
                    // reset use-default value to prevent default icon
                    // displaying in case of form error
                    $("#use-default").val('');

        }

            },
            error: function() {
                $("#scrape-url").html('<i class="fa fa-magic" aria-hidden="true"></i>Error!');
            }
        });
    }

    // on import-url page load, auto scrape, once only
    if ($('#import-url').length) {
        if ($('#import-url').attr("data-autoscrape") == 'true') {
            scrapeUrl();
        }
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

    // check url timer
    $("#id_url").keyup(function() {
        clearTimeout(urlTimer);
        urlTimer = setTimeout(checkURL, timerLength);
    });

    // Run checkUrl function on page load
    if ($('#edit-bookmark').length){
            checkURL();
    }

    function checkURL() {
        let urlToCheck = $("#id_url").val();

        let httpRe = new RegExp('^https?://');
        let match = httpRe.test(urlToCheck);
        if (!match && urlToCheck) {
            urlToCheck = 'https://' + urlToCheck;
        }

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
                        // $("#url-validation-result").text("Url status: Valid");
                        $("#url-validation-result").html(
                        "Url status: <span class='status status-valid'>Valid</span>"
                        );

                        break;
                    case false:
                        // $("#url-validation-result").text("Url status: Invalid");
                        $("#url-validation-result").html(
                            "Url status: <span class='status status-invalid'>Invalid</span>"
                            );
                        break;
                    default:
                        $("#url-validation-result").text(
                            "Url status: Url field is empty"
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
            preview.readAsDataURL(this.files[0]);

            // on file upload hide default icon and show uploaded icon
            $('#img-preview').removeClass('icon-display-hide');
            $('#default-icon').addClass('icon-display-hide');
            // clear any scraped images if user selects file to upload
            $("#scraped_img").val('');
            // reset use-default value to prevent default icon
            // displaying in case of form error
            $("#use-default").val('');
            // display name of selected file in input field
            var fName = $(this).val().split("\\").pop();
            $(this).next().text(fName);
        }
    });


    // nav bar title hide / show on scroll
    function navbarBehaviour () {
        if (window.scrollY > 1) {
            $('.navbar-title').css({ opacity: 0, transition: 'opacity 0.5s' }).slideUp(600);
            $('.mobile-menu').css({ opacity: 0, transition: 'opacity 0.5s' }).slideUp(600, function () {
                $('#pages-nav').addClass('nav-border');
            });
            
        } else {
            $('.navbar-title').css({ opacity: 1}).slideDown(600);
            $('.mobile-menu').css({ opacity: 1}).slideDown(600);
            if (!window.location.href.includes('accounts')) {
                $('#pages-nav').removeClass('nav-border');
            }

        }
    }

    // activate on scroll and initial page load
    $(window).scroll(navbarBehaviour);
    navbarBehaviour();

    // topnav behavior
    function topnavBehaviour () {
        if (window.scrollY > 1) {
            $('#topnav').css({ 'border-bottom': '1px solid #aaaaaa',
                               'background-color': 'rgba(250, 250, 250, 0.9)',
                               'transition': 'all .5s ease'});
        } else {
            $('#topnav').css({ 'border-bottom': '1px solid transparent',
                               'background-color': 'transparent',
                               'transition': 'all .5s ease'});
        }
    }

    // activate on scroll and initial page load
    $(window).scroll(topnavBehaviour);
    topnavBehaviour();


    // on click, toggle 'plus' icon for each entry on faq page
    $(".collapse")
        .on("show.bs.collapse", function() {
            $(this)
                .parent()
                .find(".fa-plus-square-o")
                .toggleClass('fa-plus-square-o fa-plus-square');
        })
        .on("hide.bs.collapse", function() {
            $(this)
                .parent()
                .find(".fa-plus-square")
                .toggleClass('fa-plus-square-o fa-plus-square');

        });

    // reset contact form button
    $('#contact-form-reset').on('click', function() {
        $('#id_name, #id_email, #id_message').val('');
    });

    // close sidebar on swipe - uses third party swipe.js script
    $('#sidebar').onSwipe((result)=>{
        if(result.left == true && window.innerWidth <= 767) {
            $("#sidebar, #content").toggleClass("display-switch");
            $("#content").toggleClass("no-scroll");
        }
    });



    // Create a default icon when displaying icons on add / edit / import page
    $('#use-default-icon').on('click', function () {
        $('#img-preview').addClass('icon-display-hide');
        $('#default-icon').removeClass('icon-display-hide');
        $("#id_icon, #scraped_img").val('');
        $('#use-default').val('true');
        //clear value inside file upload field
        $("#id_icon").next().text('Choose file');
        updateDefaultIcon();
    });


    // -------------------------- Update letter for default icon on title change //

    const lettersUpper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const colorsList = [
        '#698396',
        '#a9c8c0',
        '#dbbc8e',
        '#ae8a8c',
        '#f7f6cf',
        '#e6a57e'];

    let titleTimer;
    let titleTimerLength = 1000;

    // check title timer
    $("#id_title").keyup(function() {
        clearTimeout(titleTimer);
        titleTimer = setTimeout(updateDefaultIcon, titleTimerLength);
    });

    function updateDefaultIcon() {

        // set icon letter for default icon
        let title = $('#id_title').val();
        let firstLetter = title.charAt(0).toUpperCase();
        $('#default-icon').find('span').text(firstLetter);

        // set background color for default icon
        let idx = lettersUpper.indexOf(firstLetter) + 1;
        let bgColor = colorsList[idx % 6];
        $('#default-icon').find('.no-icon').css({"background-color": bgColor});
    }

    // update default-icon on page load
    if ($('#add-bookmark, edit-bookmark, #import-url').length){
        updateDefaultIcon();
    }

    // close window after import
    $('#close-page').on('click', function () {
        window.close();
    });

    // add new collection
    $(".btn--add-collection").on("click", function() {
        $(this)
            .parent()
            .next()
            .slideToggle(200);
        $(this)
            .children()
            .toggleClass('fa-chevron-circle-down fa-plus-circle');
    });

    // testing
    if (typeof num_columns !== 'undefined') {
        console.log(num_columns);
    }

});
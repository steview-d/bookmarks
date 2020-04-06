$(document).ready(function () {
    // --------------------------------------------------- Buttons & Toggles //

    // 'add new page' icon - toggle form
    $("#add-page-btn").on("click", function () {
        $(this).parent().next().children().slideToggle(200);
        $(this).children("i").toggleClass("fa-plus fa-chevron-down");
    });

    // 'edit page' icon - form toggle
    $(".page-options-btn").on("click", function () {
        $("#page-display-options").slideToggle(200);
    });

    // 'collection options' icon - toggle
    $(".btn--collection-options").on("click", function () {
        $(this).parent().parent().next().slideToggle(200);
    });

    // 'autofill' button
    $("#scrape-url").on("click", scrapeUrl);

    // 'add new collection' icon - toggle form
    $(".btn--add-collection").on("click", function () {
        $(this).parent().next().slideToggle(200);
        $(this).children().toggleClass("fa-chevron-circle-down fa-plus-circle");
    });

    // clear values inside contact form if users clicks the reset button
    $("#contact-form-reset").on("click", function () {
        $("#id_name, #id_email, #id_message").val("");
    });

    // FAQ '+' icon toggle
    $(".collapse")
        .on("show.bs.collapse", function () {
            $(this)
                .parent()
                .find(".fa-plus-square-o")
                .toggleClass("fa-plus-square-o fa-plus-square");
        })
        .on("hide.bs.collapse", function () {
            $(this)
                .parent()
                .find(".fa-plus-square")
                .toggleClass("fa-plus-square-o fa-plus-square");
        });

    // sidebar toggler
    $(".sidebarToggle").on("click", function () {
        $("#sidebar, #content").toggleClass("display-switch");
        $("#content").toggleClass("no-scroll");
    });

    // close sidebar on swipe - uses third party swipe.js script
    $("#sidebar").onSwipe((result) => {
        if (result.left == true && window.innerWidth <= 767) {
            $("#sidebar, #content").toggleClass("display-switch");
            $("#content").toggleClass("no-scroll");
        }
    });

    // ------------------------------------- Navbar Behaviour on Page Scroll //

    // Intro Pages - About, Pricing, FAQ & User Auth
    function navbarBehaviour() {
        if (window.scrollY > 1) {
            $(".navbar-title")
                .css({ opacity: 0, transition: "opacity 0.5s" })
                .slideUp(600, function () {
                    $("#pages-nav").addClass("nav-border");
                });
            if ($("#login, #register, .pw-control").length) {
                $("#pages-nav").css({
                    "background-color": "rgba(250, 250, 250, 0.9)",
                    transition: "background-color 1s",
                });
            }
        } else {
            $(".navbar-title").css({ opacity: 1 }).slideDown(600);
            if (!window.location.href.includes("accounts")) {
                $("#pages-nav").removeClass("nav-border");
            }
            if ($("#login, #register, .pw-control").length) {
                $("#pages-nav").css({
                    "background-color": "rgba(250, 250, 250, 1)",
                    transition: "background-color 1s",
                });
            }
        }
    }

    // activate on scroll...
    $(window).scroll(navbarBehaviour);
    // and initial page load
    if ($(".navbar-title").length) {
        navbarBehaviour();
    }

    // Main App & Settings
    function topnavBehaviour() {
        if (window.scrollY > 1) {
            $("#topnav").css({
                "border-bottom": "1px solid #aaaaaa",
                "background-color": "rgba(250, 250, 250, 0.9)",
                transition: "all .5s ease",
            });
        } else {
            $("#topnav").css({
                "border-bottom": "1px solid transparent",
                "background-color": "transparent",
                transition: "all .5s ease",
            });
        }
    }

    // activate on scroll...
    $(window).scroll(topnavBehaviour);
    // and initial page load
    topnavBehaviour();

    // -------------------------------------------------------- Page Sorting //

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
        stop: function () {
            let data = $(this).sortable("serialize");
            data = data.split("[]=.");
            data.pop();

            let newOrder = data.map((i) => {
                return i.replace("&", "");
            });

            postData = newOrder.join(",");

            $("#ajax-progress-spinner").toggleClass("display-toggle");

            $.ajax({
                type: "POST",
                data: {
                    new_page_order: postData,
                    csrfmiddlewaretoken: csrftoken,
                },
                url: "/app/_page_sort",
                success: function (data) {
                    if (data.success) {
                        location.reload();
                    }
                },
            });
        },
    });

    /*
    To prevent pages being moved by accident, for example if a user is trying
    to scroll through a long list of pages names, the app requires the user to
    'turn on' page sorting.
    The 'Page Sort' button toggles the 'page-sort-handle' class, which is the
    handle required by .sortable for sorting pages.
    */

    $("#page-sort-btn").on("click", function () {
        $(".page-sort-icon-container").toggleClass("hide-page-sort-icon");
        $(".page-sort-handle-container").toggleClass("page-sort-handle");
        $(this).toggleClass("page-sort-active");
    });

    // -------------------------------------------------- Collection Sorting //

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

    const column_list = [
        "#column-1",
        "#column-2",
        "#column-3",
        "#column-4",
        "#column-5",
    ];

    column_list.forEach((key, idx) => {
        $(key).sortable({
            containment: "#collections-container",
            cursor: "grabbing",
            connectWith: column_list,
            deactivate: function () {
                let data = $(this).sortable("serialize");
                data = data.split("[]=.");
                data.pop();

                let newOrder = data.map((i) => {
                    return i.replace("&", "");
                });
                let columnData = newOrder.join(",");
                buildList(idx, columnData);
            },
            stop: function (event, ui) {
                let postData = JSON.stringify(new_collection_order);

                $("#ajax-progress-spinner").toggleClass("display-toggle");

                $.ajax({
                    type: "POST",
                    data: {
                        new_collection_order: postData,
                        collection_id: ui.item[0].id,
                        csrfmiddlewaretoken: csrftoken,
                    },
                    url: "collection-sort",
                    success: function (data) {
                        if (data.success) {
                            location.reload();
                        }
                    },
                });
            },
        });
    });

    // ---------------------------------------------------- Bookmark Sorting //

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
        stop: function (event, ui) {
            if ($(this).hasClass("no-manual-sort")) {
                let page = $(this).closest("div.page-name").attr("id");
                let message = `Bookmark sorting is disabled 
                    when not in 'Manual Sort' mode.`;
                window.location = page + "/custom_message/" + message;
            } else {
                let data = $(this).sortable("serialize");
                data = data.split("[]=.");
                data.pop();

                let newOrder = data.map((i) => {
                    return i.replace("&", "");
                });

                postData = newOrder.join(",");

                $("#ajax-progress-spinner").toggleClass("display-toggle");

                $.ajax({
                    type: "POST",
                    data: {
                        new_bookmark_order: postData,
                        collection_name: ui.item
                            .closest("div.collection-name")
                            .attr("id"),
                        page_name: ui.item.closest("div.page-name").attr("id"),
                        csrfmiddlewaretoken: csrftoken,
                    },
                    url: "_bookmark_sort_manual",
                    success: function (data) {
                        if (data.success) {
                            location.reload(false);
                        }
                    },
                });
            }
        },
    });

    /*
    To prevent bookmarks being moved by accident, for example if a user is
    trying to scroll through a long list of bookmarks, the app requires the
    user to 'turn on' bookmark sorting.
    The 'Bookmark Sort' button toggles the 'bm-sort-handle' class, which is the
    handle required by .sortable for sorting bookmarks.
    */

    const bmSortButtons = document.querySelectorAll("[id^='bm-sort-btn-']");
    bmSortButtons.forEach((key) => {
        $(key).on("click", function () {
            const el = $(this).parent().parent().parent();
            el.find(".bm-handle-container").toggleClass("bm-sort-handle");
            el.find(".bookmark-styling").toggleClass("bookmark-border");
            el.find(".bm-options-icon").toggleClass("display-toggle");
            $(this).toggleClass("manual-sort-on");

            /*
            When in sort mode on smaller display widths where only 1 column is
            displayed, this usually means the user is using a touch device.
            This makes it difficult to scroll through large lists of bookmarks
            without accidently dragging a bookmark instead.

            To fix this, when in sort mode and only 1 column is displayed,
            the width of the bookmark is reduced and blank space is added to
            the right, creating a space for the user to scroll up and down the
            list.
            */

            if (typeof numColumns !== "undefined") {
                if (numColumns == 1) {
                    $(this)
                        .parent()
                        .parent()
                        .parent()
                        .find(".bm-handle-container")
                        .toggleClass("add-scroll-space");
                }
            }
        });
    });

    // ------------------------- Url Status: Check URL in '#id_url' is valid //

    /*
    Sends a url to the server with ajax for processing via the python requests
    module and returns 1 of the following responses
    True: URL resolves successfully
    False : URL could not be resolved
    None: Nothing to resolve, most likely an empty field
    */

    let urlTimer;
    // time in ms to wait from last key release to checking of url
    let timerLength = 1000;

    // check url timer
    $("#id_url").keyup(function () {
        clearTimeout(urlTimer);
        urlTimer = setTimeout(checkURL, timerLength);
    });

    // Run checkUrl function on page load when editing a bookmark
    if ($("#edit-bookmark").length) {
        checkURL();
    }

    function checkURL() {
        let urlToCheck = $("#id_url").val();

        let httpRe = new RegExp("^https?://");
        let match = httpRe.test(urlToCheck);

        // If url doesn't contain http:// or https:// prepend it to
        // the url to be checked
        if (!match && urlToCheck) {
            urlToCheck = "https://" + urlToCheck;
        }

        $.ajax({
            type: "POST",
            data: {
                urlToCheck: urlToCheck,
                csrfmiddlewaretoken: csrftoken,
            },
            url: "/app/_check_valid_url",
            success: function (data) {
                switch (data.result) {
                    case true:
                        $("#url-validation-result").html(
                            `Url status: <span class='status status-valid'>
                                Valid</span>`
                        );

                        break;
                    case false:
                        $("#url-validation-result").html(
                            `Url status: <span class='status status-invalid'>
                                Invalid</span>`
                        );
                        break;
                    default:
                        $("#url-validation-result").text(
                            "Url status: Url field is empty"
                        );
                }
            },
        });
    }

    // -------------------------------------------------------- Url Scraping //

    /*
    Sends the url to the server for scraping with BeautifulSoup4. The view will
    attempt to return values for the title & description along with an image
    encoded as a base64 string. Additionally, it will return a message that
    states either the scrape was a success, or the reason why it wasn't.
    */

    function scrapeUrl() {
        let urlToScrape = $("#id_url").val();

        // if url doesn't begin with http(s), prepend it
        let httpRe = new RegExp("^https?://");
        let match = httpRe.test(urlToScrape);
        if (!match) {
            urlToScrape = "https://" + urlToScrape;
            $("#id_url").val(urlToScrape);
        }

        $("#scrape-url").text("SCRAPING..");

        $.ajax({
            type: "POST",
            data: {
                urlToScrape: urlToScrape,
                csrfmiddlewaretoken: csrftoken,
            },
            url: "/app/_manual_url_scrape",
            success: function (data) {
                // populate text fields
                $("#id_title").val(data.title);
                $("#id_description").val(data.description);

                // Feedback result of scrape to user
                $("#scrape-msg").html(
                    `Autofill result: <strong>` + data.message + `</strong>`
                );

                // clear icon field file incase of previously selected image
                $("#id_icon").val("");

                // populate icon field
                if (data.scraped_image) {
                    // display base64 encoded image
                    let base64Str =
                        "data:image/" +
                        data.image_ext +
                        ";base64," +
                        data.scraped_image;
                    $("#img-preview").attr("src", base64Str);
                    $("#scraped_img").val(base64Str);
                } else {
                    // if no image could be scraped, display default image
                    // to show no image available
                    $("#img-preview").attr(
                        "src",
                        "/static/img/no_img_scrape.png"
                    );
                    $("#scraped_img").val("");
                }

                $("#scrape-url").html(
                    "<i class='fa fa-magic' aria-hidden='true'></i>Autofill"
                );

                // if an image is scraped, hide the default icon and
                // show scraped image
                if (
                    $("#edit-bookmark, #add-bookmark, #import-url").length &&
                    $("#img-preview")[0].src
                ) {
                    $("#img-preview").removeClass("icon-display-hide");
                    $("#default-icon").addClass("icon-display-hide");

                    // also clear value inside file upload field
                    $("#id_icon").next().text("Choose file");

                    // reset use-default value to prevent default icon
                    // displaying in case of form error
                    $("#use-default").val("");
                }
            },
            error: function () {
                $("#scrape-url").html(
                    "<i class='fa fa-magic' aria-hidden='true'></i>Error!"
                );
            },
        });
    }

    // on import-url page load, auto scrape, once only
    if ($("#import-url").length) {
        if ($("#import-url").attr("data-autoscrape") == "true") {
            scrapeUrl();
        }
    }

    // ------------------------------------- Destination Collecion Drop Down //

    /*
    Listen for changes on the page choice dropdown input. When a change is
    detected, the pk for that page is sent to the server via ajax.

    The server will process this pk by getting the collections for the new page
    and sending them back as an html string. The ajax success call will then
    replace the old html choices with the new ones that were returned.
    */

    $("#id_dest_page").change(function () {
        let newPagePk = $(this).val();
        $.ajax({
            type: "POST",
            data: {
                newPagePk: newPagePk,
                csrfmiddlewaretoken: csrftoken,
            },
            url: "/app/_update_collection_list",
            success: function (data) {
                $("#id_dest_collection").html(data.html);
            },
        });
    });

    // --------------------------------------------- Collection Display Mode //

    /*
    Listens for a click on the bookmark display mode buttons. When clicked,
    ajax posts the clicked collection and requested display mode to the server.

    On a successful return, the page is updated to show the new display mode.
    */

    $(".coll-display-btn").click(function () {
        let collection = $(this).data("coll-id");
        let mode = $(this).data("display-mode");
        $.ajax({
            type: "POST",
            data: {
                collection: collection,
                mode: mode,
                csrfmiddlewaretoken: csrftoken,
            },
            url: "/app/_change_collection_display",
            success: function () {
                location.reload();
            },
        });
    });

    // -------------------------------------------------Image Upload Preview //

    /*
    Listens for a change to the file input element, and when a change is
    registered, a preview of the uploaded file is displayed
    */

    $("#id_icon").change(function () {
        if (this.files && this.files[0]) {
            let preview = new FileReader();

            preview.onload = function (e) {
                $("#img-preview").attr("src", e.target.result);
            };
            preview.readAsDataURL(this.files[0]);

            // on file upload hide default icon and show uploaded icon
            $("#img-preview").removeClass("icon-display-hide");
            $("#default-icon").addClass("icon-display-hide");

            // clear any scraped images if user selects file to upload
            $("#scraped_img").val("");

            // reset use-default value to prevent default icon
            // displaying in case of form error
            $("#use-default").val("");

            // display name of selected file in input field
            var fName = $(this).val().split("\\").pop();
            $(this).next().text(fName);
        }
    });

    // ------------------------- Create a default icon when displaying icons //
    // ----------------------------------------- on add / edit / import page //

    $("#use-default-icon").on("click", function () {
        $("#use-default").val("true");

        // hide the current image preview & show the default icon
        $("#img-preview").addClass("icon-display-hide");
        $("#default-icon").removeClass("icon-display-hide");

        // remove any stored values for previous images
        $("#id_icon, #scraped_img").val("");

        //clear value inside file upload field
        $("#id_icon").next().text("Choose file");
        updateDefaultIcon();
    });

    // --------- Update icon letter for default icons when the title changes //

    /*
    For default icons, the icon is a colored tile with the first letter from 
    the title in the middle.
    When a user is updating the title field, the default icon should update
    once the user has finished typing.
    */

    const lettersUpper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const colorsList = [
        "#698396",
        "#a9c8c0",
        "#dbbc8e",
        "#ae8a8c",
        "#f7f6cf",
        "#e6a57e",
    ];

    let titleTimer;
    // time in ms to wait from last key release to updating of default icon
    let titleTimerLength = 500;

    // check title timer
    $("#id_title").keyup(function () {
        clearTimeout(titleTimer);
        titleTimer = setTimeout(updateDefaultIcon, titleTimerLength);
    });

    // update default-icon on page load
    if ($("#add-bookmark, edit-bookmark, #import-url").length) {
        updateDefaultIcon();
    }

    function updateDefaultIcon() {
        // set icon letter for default icon
        let title = $("#id_title").val();
        let firstLetter = title.charAt(0).toUpperCase();
        $("#default-icon").find("span").text(firstLetter);

        // set background color for default icon
        let idx = lettersUpper.indexOf(firstLetter) + 1;
        let bgColor = colorsList[idx % 6];
        $("#default-icon")
            .find(".no-icon")
            .css({ "background-color": bgColor });
    }

    // -------------------------- Monitor Display Width vs Number of Columns //

    /*
    Warn user when page width is too small for the current number of
    columns being displayed.
    Give user option to change the number of columns or dismiss this,
    and all future warnings.
    */

    // store initial width of window on page load
    var initialWidth = window.innerWidth;

    // on resize, check width to columns
    $(window).on("resize", function () {
        /*
        Some mobile browsers, when scrolling, adjust the screen height.
        The resize event picks up on this so to avoid false positives, need
        to check current width vs original width and make sure it differs.
        */
        if ($("#app").length && initialWidth != window.innerWidth) {
            widthToColumns(window.innerWidth);
        }
    });

    // also check width on page load
    if ($("#app").length) {
        widthToColumns(window.innerWidth);
    }

    // function to check width is suitable for current number of columns
    function widthToColumns(currentWidth) {
        /*
        if local storage contains 'widthWarning', do not check as user
        has requested to dismiss warnings of this type.
        */
        if (localStorage.getItem("widthWarning") === null) {
            let c = parseInt(numColumns);
            let w = parseInt(currentWidth);
            switch (true) {
                case w < 576 && c > 1:
                    width_warning(numColumns, 1, pageName);
                    break;
                case w >= 576 && w < 992 && c > 2:
                    width_warning(numColumns, 2, pageName);
                    break;
                case w >= 992 && w < 1200 && c > 4:
                    width_warning(numColumns, 4, pageName);
                    break;
            }
        }
    }

    // function to populate width_warning.html
    function width_warning(currentColumns, recMaxColumns, pageName) {
        /*
        Update width_warning.html with values for current
        and recommended number of columns.
        */

        $("#width-warning").removeClass("display-toggle");
        $(".actual-columns").text(currentColumns);

        var columnPlural = recMaxColumns == 1 ? " column." : " columns.";
        $(".rec-columns").text(recMaxColumns + columnPlural);

        // generate link to 'change_num_columns' view
        changeColumnsUrl =
            `/app/_change-num-columns/${pageName}/${recMaxColumns}`;
        $("#width-warning-change").attr("href", changeColumnsUrl);
    }

    // dismiss width warning
    $("#width-warning-dismiss").on("click", function () {
        $("#width-warning").addClass("display-toggle");
        // add item to local storage to signal user wants no further warnings
        localStorage.setItem("widthWarning", "ignore");
    });

    // Settings > Profile > Preferences: Width Warning checkbox - Set value
    if (localStorage.getItem("widthWarning") === null) {
        $("#widthWarningCheck").prop("checked", true);
    } else {
        $("#widthWarningCheck").prop("checked", false);
    }

    // Update local storage value on Width Warning checkbox change
    $("#widthWarningCheck").change(function () {
        if (this.checked) {
            localStorage.removeItem("widthWarning");
        } else {
            localStorage.setItem("widthWarning", "ignore");
        }
    });

    // -------------------------------------------------------- Gif Playback //

    /*
    About Page - Features : gif playback
    Short animated gifs that show certain features in action
    Behaviour is dependant on device:
        Touch :     Click to start/stop gif
        Pointer :   Hover to start/stop gif
    */

    const ddGifPath = "/static/img/pages/about/drag_drop_";
    const daGifPath = "/static/img/pages/about/display_as_";

    // Hover
    $(".drag-drop-gif").hover(
        function () {
            $(this).attr("src", `${ddGifPath}on.gif`);
        },
        function () {
            $(this).attr("src", `${ddGifPath}off.png`);
        }
    );

    $(".display-as-gif").hover(
        function () {
            $(this).attr("src", `${daGifPath}on.gif`);
        },
        function () {
            $(this).attr("src", `${daGifPath}off.png`);
        }
    );

    // Touch
    $(".drag-drop-gif").on("touchstart", function () {
        if ($(this).attr("src") == `${ddGifPath}on.gif`) {
            $(this).attr("src", `${ddGifPath}off.png`);
        } else {
            $(this).attr("src", `${ddGifPath}on.gif`);
        }
    });

    $(".display-as-gif").on("touchstart", function () {
        if ($(this).attr("src") == `${daGifPath}on.gif`) {
            $(this).attr("src", `${daGifPath}off.png`);
        } else {
            $(this).attr("src", `${daGifPath}on.gif`);
        }
    });
});

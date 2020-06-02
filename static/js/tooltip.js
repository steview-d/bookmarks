/*
Tooltip configuration and customisation using the tippy.js library
https://github.com/atomiks/tippyjs
*/

$(document).ready(function () {
    // initialize tooltips
    // single use non-dynamic tooltips where content is
    // embedded within the html document
    tippy("[data-tippy-content]");

    // show full bookmark description text
    tippy(".tippy-desc", {
        allowHTML: false,
        delay: 700,
        theme: "dark",
        touch: false,
        onShow(instance) {
            instance.setContent(instance.reference.innerText);
        },
    });

    // show help text for password fields on password creation / change
    tippy(".tippy-pw-help", {
        theme: "dark",
        onShow(instance) {
            const el = $(instance.reference.nextElementSibling).find(
                ".tippy-help-text"
            );
            instance.setContent(el[0].dataset.helptext);
        },
    });

    // url validation tooltip
    tippy(".tippy-url-validation", {
        theme: "dark",
        delay: [400, 0],
        placement: "bottom",
        content: `Links will attempt to load the url in the background.
            <ul><li>Valid - The url loaded successfully</li>
            <li>Invalid - The url could not be loaded but can still be saved 
            as a bookmark, and may still load for you.</li></ul>
            Url status should be used as a guide only.`,
    });

    // manual bookmark sort tooltip
    tippy(".tippy-manual-bm-sort", {
        theme: "dark",
        delay: [100, 0],
        content: `Manual sorting of bookmarks is disabled unless<br />
            <strong>Sort By: Manual Sort</strong><br />has been selected.`,
    });

    // add new collection tooltip
    tippy(".tippy-add-new-collection", {
        allowHTML: false,
        delay: 700,
        theme: "dark",
        touch: false,
        content: "Add New Collection",
    });

    // add new page tooltip
    tippy("#add-page-btn", {
        allowHTML: false,
        delay: 700,
        theme: "dark",
        touch: false,
        content: "Add New Page",
    });

    // rearrange page order tooltip
    tippy("#page-sort-btn", {
        allowHTML: false,
        delay: 700,
        theme: "dark",
        touch: false,
        content: "Rearrange Pages",
    });

    // page options tooltip
    tippy("#page-options-btn", {
        allowHTML: false,
        delay: 700,
        theme: "dark",
        touch: false,
        content: "Page Options",
    });

    // bookmark options tooltip
    tippy("#dropdown-bm-options", {
        allowHTML: false,
        delay: 700,
        theme: "dark",
        touch: false,
        content: "Bookmark Options",
    });

    // bookmark options tooltip
    tippy(".add-bookmark-btn-coll", {
        allowHTML: false,
        delay: 700,
        theme: "dark",
        touch: false,
        content: "Add Bookmark",
    });

    // rearrange bookmarks tooltip
    tippy(".rearrange-bookmarks", {
        allowHTML: false,
        delay: 700,
        theme: "dark",
        touch: false,
        content: "Rearrange Bookmarks",
    });

    tippy(".btn--collection-options", {
        allowHTML: false,
        delay: 700,
        theme: "dark",
        touch: false,
        content: "Collection Options",
    });
});

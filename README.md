<p align="center">
  <img src="https://i.imgur.com/wwb33jN.png">
</p>

# Links

Links is a bookmarking app built using Pythons Django framework, and hosted with Heroku.
The main function of the app is to allow users to save the URL's of any website for easy reference. Users can also edit and delete their saved bookmarks, and there are numerous options to allow users to organise and display their collection in a way of their own choosing.

The deployed app can be found at [links-sw.herokuapp.com](https://links-sw.herokuapp.com)

## Contents


1. [UX](#ux)
	- [User Stories](#user-stories)
	- [Design](#design)
	- [Wireframes](#wireframes)

2. [Features](#features)
	- [Current Features](#current-features)
	- [Planned Features](#planned-features)

3. [Technologies Used](#technologies-used)
	- [Languages](#languages)
	- [Frameworks & Libraries](#frameworks-and-libraries)
	- [Tools](#tools)
	- [Hosting](#hosting)

4. [Testing](#testing)
	- For testing, refer to the [testing document](TESTING.md).

5. [Deployment](#deployment)
	- [Local Deployment](#local-deployment)
	- [Deploying To Heroku](#deploying-to-heroku)

6. [Credits](#credits)
	- [Content](#content)
	- [Media](#media)
	- [Code](#code)
	- [Acknowledgements](#acknowledgements)

## UX
The app can be split into 3 distinct sections
1. The 'introductory' pages. These introduce potential users to the app, conveying information such as features, pricing, FAQ's, and providing login / register options.
2. The settings pages. Here users can update their profile, get support, and upgrade to a Premium account.
3. The main app page. This is where users can view, add, edit, organise, and delete their bookmarks.

Section 1 is only available to users who are logged out and unregistered, whilst sections 2 and 3 are only for logged in / registered users. This is intentional, as once a user has committed to creating an account, they should have no need for the initial pages, whose only purpose was to sell the app and encourage registration.

For this reason, the design of the introductory section is intentionally different to the other sections. Whilst they share similar design elements (colors, fonts, logos, etc) the intro pages make use of a single navigation bar at the top, whilst the main app and settings sections use a sidebar for navigation within the current section, and a top navigation bar for other features, such as search and swapping between sections (settings / main app).

### User Stories
#### As a user, I expect to be able to:
- Save a webpage URL so I can revisit the page at a later date
- Store multiple 'bookmarks' within my account
- Organise my bookmarks into collections of similar bookmarks
- Have multiple pages, each containing multiple collections of bookmarks
- Order the bookmarks, pages, and collections in a way of my own choosing
- Edit my existing bookmarks should they need updating
- Move bookmarks from 1 collection and / or page, to another
- Delete bookmarks I no longer require
- Easily import bookmarks from the page I want to save with just a few clicks, without the need for multiple copy/paste actions
- Let the app scrape data from the page I want to save, and automatically create a suitable title and description
- Save an icon with the bookmark so I can easily identify the bookmark at a glance. Additionally, I should be able to choose the icon by either uploading my own, letting the app use the web page icon, or allow the app to create one of its own
- Update my personal details (email / password) if required
- Get support in the event of my being stuck, or if I have questions relating to the app
- Pay to upgrade to a 'Premium' membership tier, giving me access to features otherwise unavailable to users who are using the app for free.
- Have access to this app and my bookmarks across a range of devices and displays

#### As the site admin, I expect to be able to:
- Manage the site and its users through a dedicated backend admin portal
- Be notified of support requests and be able to respond effectively
- Be able to track users who have signed up for a Premium membership
- Easily receive feedback from users

### Design

#### Application Framework
This app uses the Django framework

#### Database
Django uses SQL databases. During development, the Django default sqlite3 database was used. When deployed to Heroku, a PostgreSQL database was used.

![DB Schema](https://i.imgur.com/ohEXTqA.png)

##### Django 'unique_together' model constraints
- Bookmark
	- [collection, position]
- Collection
	- [name, user, page] 
	- [position, name, page, user]
- Page
	- [position, user]
	- [name, user]

#### CSS Framework
The app uses the Bootstrap 4 framework

#### Typography
Only 2 fonts are used throughout the app.
- [Delius Unicase](https://fonts.google.com/specimen/Delius+Unicase?query=delius+un) is used for buttons and headings h1 through h4. A fun comic style font, without being over the top. Great for buttons and headings, it stands out well on the page without being too much.
- [Muli](https://fonts.google.com/specimen/Muli?query=muli) is used for all other text, including h5, h6 and paragraphs. Weight is set to 300, which gives the page a crisp and clean look.

#### Icon Set
Font Awesome 4 has been used throughout the project, across all sections, ranging from icons in the nav bar through to tooltips and everything in between.

### Wireframes
Wireframes were created using [Balsamiq](https://balsamiq.com/) during the initial design phase of this project.
##### Introductory Pages
- [Home](https://i.imgur.com/FErwGWK.png)
- [Pricing](https://i.imgur.com/RHDvlD2.png)
- [FAQ](https://i.imgur.com/JV8epQX.png)
##### Main App
- [Main App](https://i.imgur.com/Fq6VRI0.png)
##### Settings Pages
- [Premium](https://i.imgur.com/V40kQr9.png)
- [Profile](https://i.imgur.com/3E9Zpfd.png)
- [Support](https://i.imgur.com/JhxUUeV.png)
- [About](https://i.imgur.com/i4F26hN.png)

## Features
### Current Features

#### The Sales Pitch
The first pages a user encounters are the 'sales pitch' pages. These 3 pages (index/home, pricing, FAQ's) are designed with a single purpose in mind - to convince the user to create a free account and give the app a try. Each page fulfils the following role as part of the overall pitch
##### Home
Introduces the app and inside of a few short lines gives a high-level overview of what it does. A 4x4 grid of icons from familiar and well-known websites (chosen from a random pool of 100+) is displayed alongside to allow the user to make a connection between this app and (potentially) some of their favourite sites.

The features section is designed to give users a deeper insight into how the app functions, and what they can expect if they sign up. It focuses on customisation options, and lets users know they have a large degree of control over how they choose to use the app. Animated gifs are provided so users can see first-hand how the app works. For users wanting more information on features, there is a link to take them straight to a comparison table on the pricing page.

The next section introduces the Chrome browser extension, and the text focuses on how the extension makes it easier for users to use the app, and how it is free to use. There is a link to take the user to the Chrome Web Store so they can install it quickly and easily.

A user reviews section contains quotes from current users. Each review has been tailored to highlight and promote a specific aspect of the app.

Finally, at the bottom of the page, just before the footer, there is a link to take the user to the login / register screen. This is here as part of the overall effort to make it as easy as possible to create an account from any part of the site.

##### Pricing
This page focuses on the free aspect of the app and assures users the app is fully functioning whether they choose to upgrade to Premium or not.

A comparison table reinforces this by showing the main differences between the 2 tiers. It is laid out in such a way so as to show that Premium membership just means 'bigger, better, more' rather than Free meaning 'limited functionality'.

A 'launch offer' is in place to let users know if they do decide to go for the Premium tier, it is only a 1 off payment for full lifetime access. The limited nature of this offer is designed to encourage users to sign up sooner rather than later.

As with the home page, the final section is a link to the user register / login screens.

##### FAQ
A standard FAQ section, with questions picked that best promote a key aspect of the overall user experience, such as support, feedback, and so on.

Below this is a contact form that non-registered users can use to get in touch with the app's admin. Registered users can use it too, but as there is a dedicated support system in place inside of the app itself, it's expected the vast majority of contacts will be from non-users.

Lastly, as with previous pages, there is a button directing users to register / login.

#### New User Registration
Users can create a new account from this page. There are no restrictions on who can create an account, and it is free to do for all users. Users must provide a unique username and email address, which are checked against existing entries. A password is required, which must be entered twice to check it has been inputted correctly.

Tooltips are next to the username and password fields and provide guidance on how these fields should be completed.

![](https://i.imgur.com/NMjQ44X.png)

In the event of these fields not being filled out correctly, or duplicate data being matched, the app will let the user know what the error is so it can be corrected.

![](https://i.imgur.com/GWdEeCB.png)

Client-side validation has been removed for this form (and all others throughout the app). Form validation is all handled by the app itself. This is to provide consistency for the user across all forms.

Just underneath the 'Create Account' button, there is a link to the login page, should the user find they are trying to login instead.

![](https://i.imgur.com/4hAmCYj.png)

#### Log In System
The login page is identical to the register account page in most ways. The key differences (aside from the end result) are
- The login page only requires a username and password to proceed.
- There is a link to the password reset section for users who have forgotten / lost their password

![](https://i.imgur.com/mc16raI.png)

#### Password Reset
The app uses the built-in password reset system provided by Django, although the pages have been customised to match the design of the rest of the site.

From the login page, a user can access the 'forgot your password' link whereby they provide an email address and if a match is found, they will receive an email with a link allowing them to create a new password.

#### Full Admin Backend for Easy Admin Management
The standard Django admin pages have been customised to make managing the app easier for admins. The look and feel has not been changed as it's not an area a standard user will ever access or even see, but additional layouts, filters, and actions have been added to aid the overall admin experience.

Some examples of admin backend customisation
##### Users
'Groups' has been added to the list of filters, so the user can filter by All / Premium / No Group (Free Tier).

Additionally, a 'Membership Status' column has been added to the user overview page. There is no membership status field in this model, this is handled by Django User Groups, so this had to be defined in the admin<span></span>.py file for the accounts app.

![](https://i.imgur.com/oGHKcYq.png)

##### Bookmarks
The individual bookmark view has been updated to group the different fields into relevant sections using fieldsets.
'added' and 'updated' have been added here too. They would not show up by default due to being read-only fields but have been added to assist with any potential troubleshooting that might be required when dealing with support tickets.

##### Collections & Pages
The overview page for these models have been adjusted to just display the key columns an admin might need when troubleshooting, and to avoid information overload. All field data is viewable when drilling down to individual collections and pages.

##### Contacts
Any time a user completes the 'Get In Touch' form, the form data is stored in the app, rather than emailing admin users. This allows anyone who would deal with these messages to co-ordinate action / responses together, rather than multiple people potentially dealing with the same issue at the same time.

As well as customising the overview columns, a filter for the 'actioned' field has been added to allow an admin to view contacts by All / Yes / No.

Fieldsets are used in the detail page to clearly separate the content of the message from data an admin would need when processing items, such as date created and actioned.

##### Premium Purchases
The detail screen for individual purchases separates payment data (amount, date, id) from the user data such as name and email.

##### Tickets
2 custom actions have been created, 'open selected tickets' & 'close selected tickets' to go alongside the default 'delete....' action.

![](https://i.imgur.com/rsYnnyq.png)

Overview columns show just top-level information and a custom column called 'Admin Comments' has been added. This checks to see if the field 'Admin Comments' contains any data and displays accordingly, allowing admins to see at glance if work has already started on an individual ticket.

![](https://i.imgur.com/zoT6kGC.png)

A filter has been added for the status field to allow an admin to filter by All / Open / Closed.

The individual ticket display has been customised to separate the ticket data into sections to make it easier for admins to quickly focus on the data they need. There are 3 areas, split into user details, ticket details, and admin actions (comments and status).

#### Messages System
The app makes use of the built-in messages framework that comes with Django. Any time the app needs to communicate an important event to the user, such as confirmation of an action's success or failure, the message is flashed at top of the screen, just below the top navigation bar.

![](https://i.imgur.com/gstGn6j.png)
![](https://i.imgur.com/XNjnHAP.png)

The message tag is used to set the bootstrap color class (success green, orange warning, and so on) so the user can immediately tell what type of message it is. Messages can be manually closed, or they will disappear on a new page load / refresh.

#### Built In Support Ticket System
Registered users can open a support ticket to help with anything related to the app. The form is simple, requiring only a title and message, and the ticket will be opened and viewable from within the admin panel. Details of how an admin would manage this ticket can be found in the previous section on the admin backend, specifically [this section on tickets](#tickets).

From a user perspective, once the form is submitted, they will receive an email confirming receipt of their ticket which will also contain a copy of their support request.

<details>
	<summary>Example Support Ticket Email</summary>

![](https://i.imgur.com/XZSWbtS.png)
</details>

#### Upgrade to Premium Tier
Users can upgrade to the Premium tier from the Premium page in the Settings section. The page is designed to first show visitors what Premium gives them over the free tier and then follows it up with the limited lifetime offer to further incentivise the purchase.

When the user is ready to upgrade, a simple form is available for their payment details. Only limited information is collected, just their card details and basic identifying information (name and postcode).

<img src="https://i.imgur.com/uY1GGkK.png" height=300>

This form connects to the Stripe API to process a user's card details. No card details are stored locally or on the server, they are only sent to Stripe and then discarded.

Payments (and Premium functionality) can be tested by upgrading to Premium using Stripes basic test card numbers, which are the following
```
Card Number - 4242 4242 4242 4242
Expiry - Any future date
CVC - Any 3 digits
```

On successful completion a `PremiumPurchase` object is created to record the event and the user is added to the 'Premium' group. This group has no special permissions and is used only to differentiate between Free & Premium users.

#### Premium Functionality for Paying Users
Premium users can do things that users on the free tier cannot, such as access telephone support, remove ads, and have more bookmarks, collections, and pages.

There are 2 functions used to check if a user is a Premium member, and the function used depends on which part of the app needs to know, i.e. the back-end logic, or the front-end templating.

##### is_premium
Updates the context dictionary with a key value pair of ``is_premium: (Boolean)`` and is used the by templating language when deciding which content to display
##### premium_check
Returns a Boolean. When a user tries to perform an action that has the potential to be limited by them being on the Free tier, for example adding a Page, this function checks if this action would cause the user to exceed the limits imposed by the Free tier.

If the check passes, nothing happens and the app works as normal, leaving the user oblivious to the fact a check took place.

If the check fails, the user is informed of this, advised this is due to them being on the Free tier, and is then redirected to the Premium page to encourage them to convert to Premium.

![](https://i.imgur.com/IDpUnEj.png)


#### User Profile Page
The user profile page allows the user to update their email address and password, using 2 separate forms. It is as straight-forward as entering the required information and pressing submit. Providing the form passes the validation checks, the update is immediate.

This page also contains a ``user preferences`` section. Currently this only consists of one entry - an option to set / reset the display warnings when there are too many columns - but this can be expanded as and when more functionality is added.

The final section provides basic data on how many bookmarks, collections, and pages the user has currently. This can eventually be expanded into its own section for [Detailed User Statistics](#detailed-user-statistics)

#### Top Navigation Bar
When logged in, the top navigation bar allows the user to move between different sections of the app (bookmarks, options, log out) and also search their entire collection.

<img src="https://i.imgur.com/mhxYtY0.png" height=50>

The element is fully responsive and adjusts to the current screen width. On widths < 768px the sidebar is hidden from view so the app adds the burger icon / 3 horizontal lines to the left to show the user it can be expanded back out.

Additionally, the ``+ Add Bookmark`` from the sidebar button is no longer visible so the top navigation bar adds a ``+`` icon to allow the user to still easily add a bookmark without having to manually open the sidebar.

<img src="https://i.imgur.com/ii7L9Gm.png" height=50>

On widths < 576px the search bar is replaced by a search icon, again to save space, and when clicked it expands into a search box allowing the user to type in their search query.

<img src="https://i.imgur.com/AXVGTG0.png" height=50> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://i.imgur.com/qYc40r8.png" height=50>

#### Side Navigation Bar
The side navigation bar takes 2 forms depending on whether the user is within the bookmarks or settings section.

##### Bookmarks
Whilst managing bookmarks, the sidebar will contain a list of the  pages.

![](https://i.imgur.com/UOflZRJ.png)

There is a lot of functionality built into this section, allowing a user to:
- Navigate to a different page
- Add a new page <img src="https://i.imgur.com/cvP9EP3.png" height=20>
- Reorder existing pages <img src="https://i.imgur.com/x3QhD6M.png" height=20>
- Edit the current pages' settings <img src="https://i.imgur.com/X3oiz08.png" height=20>
	- Rearrange the collections on the current page
	- Change the number of columns displayed on the current page
	- Rename the current page

##### Settings
A simple list allowing the user to navigate between the different settings pages.

##### Both Sections
Regardless of section, the top of the sidebar will always contain the app logo and ``+ Add Bookmark`` button

#### Search Functionality
Using the search bar at the top of the page, a user can search their entire collection by title, and view all the results in one place.

<img src="https://i.imgur.com/VUI9XWm.png" height=400>

The individual bookmarks are displayed in ``full`` mode (See [Bookmark Display Options](#bookmark-display-options) for more detail on this) and have the same actions available (Edit, Move & Delete) as when viewing from within their respective collections and pages.

Up to 10 results will be displayed per page, and in the event of there being more than 10 results, they will be spread over multiple pages for the user to browse through.

![](https://i.imgur.com/gvU5JKz.png)

Results are displayed in ``date added``  order, earliest first. At a later date, this would be fleshed out more to give the user more control over the search results, in the form of configurable sort orders and more pagination options.

If a user searches with a blank search term, the app will return all bookmarks.

#### Add Bookmark
Adding a bookmark is as straightforward as filling out a form and clicking the ``Add Bookmark`` button.

The user has complete control over this and can enter the information manually or click ``Autofill`` and let the app try and populate the fields itself. The same applies for the bookmark icon; the user can upload their own, scrape the web page, or let the app generate its own

The user should also tell the app where to store the bookmark - the page and collection. The default page is the currently selected page, and the default collection is the first collection on this page, unless the user has chosen to add a bookmark using the `+` icon in the collection header. If they have, the default collection destination will be the collection from which the `+` icon was clicked. If a user comes from, or chooses, a page that currently has no collections, the destination collection drop-down will reflect this by being empty. If the user tries to submit to an empty collection an error message will tell them to choose a page with at least 1 collection

#### URL Validation

![](https://i.imgur.com/thSI2fC.png) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![](https://i.imgur.com/6vvhABb.png)

When adding a bookmark, just underneath the ``URL`` field is a ``URL status`` checker. The purpose of this is to provide real-time feedback on if the URL being entered is valid or not. Using ajax the app will send the URL to the ``check_valid_url`` function and using the Python requests library it will return a Boolean result.

To keep requests at a reasonable level, the function is called only after 1 second has elapsed since the last key release within the URL field.

#### Automatic Scraping of Pages for Bookmark Data

A user can choose to allow the app to scrape the address in the ``URL`` field by clicking the ``Autofill`` button and have the ``title`` and ``description`` field filled in automatically. Where no data can be scraped, the text fields will be filled with a message stating this.

Additionally, ``Autofill`` will also attempt to get the sites icon and if successful this will show in the ``Icon Preview`` area.

After `Autofill` has run, a message just below the button will be displayed to let the user know if it has been successful. Success is determined by the app being able to connect to the site and attempt to scrape, not by what it returns.

<img src="https://i.imgur.com/KbaXYUp.png" height=93>

#### Bookmark Icons
When it comes to storing an icon to go alongside the bookmark, users have 3 options
1. Scrape the site with ``Autofill`` and use whatever image is returned
2. Upload their own
3. Let the app create one

Each time one of the above operations is successful, a preview of the result will be displayed in the `icon preview` section. No further action is required by the user to select this image - the contents of this preview will be saved with the bookmark when the form is submitted.

If a user chooses to let the app create a bookmark for them, nothing is actually created, and the app doesn't store anything in the icon field. Instead, every time the app needs to display a bookmark icon, if it finds an empty field, it then generates the bookmark there and then.

The generated icon is the capitalised first letter in the bookmark title on a colored tile. This is taken care of by the filters contained with `icon_styling.py`. The filters set the size of the icon and text, based on the chosen display option. The tile color is decided by the position of the letter in the alphabet. This way, tile colors and letters are consistent across the entire app.
<p align="center">
  <img src="https://i.imgur.com/wwb33jN.png">
</p>

#### Bookmark Options
Every bookmark has an icon to its right that when clicked, provides a number of bookmark specific options.

<img src="https://i.imgur.com/n26shSR.png" height=300>

##### Edit Bookmark
The `Edit Bookmark` page is similar to the `Add Bookmark` page in both style and functionality. The only differences are
- The form is already filled in with data for that particular bookmark
- The `Destination Page` & `Destination Collection` drop-downs are not shown as the Bookmark isn't moving anywhere.

##### Move Bookmark
The `Move Bookmark` page is almost the opposite of the `Edit Bookmark` page. The only fields are drop-downs for `Destination Page` & `Destination Collection` so the user can choose where to move the bookmark to.

The Bookmark itself is displayed so the user can see at a glance which bookmark is being moved, but there is no option to edit the details.

##### Delete Bookmark
When a user selects the `Delete Bookmark` option, a modal appears asking for confirmation. The user can either choose to delete the Bookmark or cancel the request. All deletions are permanent.

#### Add a New Collection
On any given page, a user has the option to add a new Collection. If the page is currently empty, there is just 1 large box directing the user to create a collection.

<img src="https://i.imgur.com/1qmqVyr.png" height=300>

This is placed prominently as the user can do little else until a page has at least one collection. If a page contains 1 or more collections, the option to add another is still present, but is located a little more discretely and is positioned after the last collection in each column. 

#### Browser Extension for Easy Importing of Bookmarks
Whilst not part of the project submission, a Chrome extension was created to improve the overall UX when adding bookmarks. The repo can be found [here](https://github.com/steview-d/links-ext) and the extension itself is hosted on the [Chrome Web Store](https://chrome.google.com/webstore/detail/links/gogabcimknibfnonhajgpkibeeeppjbp).

Adding bookmarks is easy enough when just copy / pasting a URL into the URL field of the `Add Bookmark` page but I realised early into the project it just was not convenient. Users are not expected to spend a lot of time in the app itself, rather just use it for reference when looking for a particular site or page. It ended up being a real chore using the app if every time you want to save a page for later you had to open a new tab, load the app, select `Add Bookmark` and so on.

This extension streamlines the process massively. Now, users only need to click the extensions icon and it will open the app in a new tab, with the page they were on now in the URL field and the app will also automatically start a scrape to give the user some data to get started with. In many cases, this will be enough and allows a user to save a bookmark and get back to where they were in 3 steps:

	1. Click on the extension icon
	2. Click 'Add Bookmark'
	3. Close the tab once the 'import successful' message is displayed

The `Import URL` page is identical to the `Add Bookmark` page in almost every way, the only differences being:
- The name
- No sidebar or top navigation as the tab is designed to be closed as soon as the import is complete

There is currently 1 unresolved bug with the extension. When the Chrome browser is opened for the first time, the first click of the extension does nothing. All subsequent clicks work as expected. If another new window is opened, the click works first time.

Since discovering this, I haven't yet investigated. It might be an easy fix. It might not. It is likely somewhere in between but it's not a priority as it doesn't affect the app so for now it's on hold.

#### Arrange Collections
Bookmarks are grouped together inside of their own containers, which are called `collections`. These collections can be moved around the page as the user sees fit.

Users can access this functionality from the `Arrange Collections` button, located in the sidebar by clicking the cog icon next to the current page name.

<img src="https://i.imgur.com/YUp7qj8.png" height=400>

Collections are arranged using a drag & drop system and the number of columns being arranged is dependent on the current column setting. The app ensures that when a user rearranges a collection, that arrangement carries over to all column variations. So, if a user makes a change whilst using 5 columns on screen at once, but then decides to switch to a 3 column view, those changes will be represented when switching. It's not perfect, but it's close, and definitely better than forcing the user to have to rearrange their collections manually every time they adjust the number of columns.

#### Bookmark Display Options
The user can choose from 3 different display styles, on a per collection basis.

<img src="https://i.imgur.com/eD8e8YC.png" height=250>

##### Full
![](https://i.imgur.com/aA6ZPAn.png)
On `Full` all 3 information fields are displayed: `URL`, `Title` & `Description`. More often than not, the description contains more text than can be comfortably displayed, so if a user hovers over this area, a tooltip will display showing the full text.

<img src="https://i.imgur.com/ddVy3aJ.png" height=80>

These tooltips only display on devices with a pointer. I considered adding another icon to allow users to click and view the tooltip but felt this added too much clutter to the UI.

###### Normal
![](https://i.imgur.com/Md2GN8Z.png)
`Normal` removes the `Description` (and therefore the tooltip), but still keeps the `Title` & `URL`.

##### Minimal
![](https://i.imgur.com/JORLLPz.png)
`Minimal` displays the `Title` only. Users can still see at a glance exactly what this bookmark is, with the advantage of its small size making it ideal for small screens and collections with a lot of bookmarks.

Regardless of how the user chooses to display their bookmarks, the bookmark and options icons are always visible.

#### Bookmark Sort Options
The user can choose to sort and order their bookmarks in a number of different ways, on a per collection basis.

<img src="https://i.imgur.com/bmOqACp.png" height=300>

##### Predefined Sort Orders

These are `Name`, `Date Added` and `Date Updated` and the user can choose to sort these by ascending or descending. When sorting in one of these modes, manual sorting is disabled. The `Manual Sort` button  <img src="https://i.imgur.com/ErRZuXF.png" height="20"> at the top of the collection is greyed out and disabled. Additionally, a tooltip is added to let the user know they need to re-enable manual sort to use this feature.

##### Manual Sorting
If a user prefers to sort their bookmarks in a particular way (for example, most used first) they can do this. Once the `Manual Sort` button is clicked, the bookmark style changes to show the mode is active.

<img src="https://i.imgur.com/1p48nHg.png" height=160>

Users can then order the bookmarks as they please using drag & drop, and turn it off once complete. On smaller displays, the width of the bookmark in sort mode is reduced to leave a gap to the right so users can scroll up and down the screen without accidently grabbing a bookmark. This is especially useful for large collections.

#### Adverts for Free-Tier Users
A banner advert is displayed at the bottom of most screens for non-Premium users.

Its position has been placed in such a way as to be non-intrusive, but still noticeable enough to generate clicks and to also make the user want to get rid of it via the Premium upgrade.

The only screens that do not display these adverts are screens where no user is logged in (about, pricing, FAQ, user auth) and the `About` page from within the settings section.

#### Multiple Columns & Small Width Displays
Quite soon into development it became apparent this type of app was definitely more suited to desktops and generally the wider the display, the better the experience. This was an issue as the app needed to function well on displays of all sizes, but I didn't want to compromise the UX on medium and large displays, just to make it serviceable on smaller screens.

The main issue was that of multiple columns on small width displays. Taking mobiles as an example, anything more than 1 column looked a mess and, in some cases rendered the app useless. It still worked, but from a user's perspective, it was more trouble than it was worth.

The final solution manages to keep the UX consistent across all screens and works as follows.

For each display width, there is a maximum number of columns at which the app displays well, and choosing to use more columns than this recommendation would impact the overall UX, usually by making elements unreadable due to being squashed on screen.

Min Display Width|Max Display Width|Max Columns
---|---|---
0px|575px|1
576px|991px|2
992px|1199px|3
1200px| Any|5

If the app detects a width and column combination outside of these recommended limits, a warning is displayed, advising the current settings may not provide the best experience.

<img src="https://i.imgur.com/upQISXg.png" height=250>

The user can then choose to either change to the recommended number of columns or dismiss the warning.

If the user opts to change the number of columns, it is assumed the user wants to continue using the app within the recommended limits, and therefore any future width adjustments will trigger a similar warning.

However, one of the key goals of this app has always been to give the user a choice in how they use it. If they want to display more columns than recommended, they can. If they click to dismiss this warning, all future warnings will also be suppressed.

If the user changes their mind and decides they want the warnings back, this can be adjusted from the `settings > profile > user preferences` section of the site.

Additionally, this preference is stored using local storage so if a user chooses to dismiss warnings on desktop, but then accesses the app via their mobile device, they will still continue to receive display warnings, until dismissed.

Another, lesser issue, was that of the sidebar taking up too much space on smaller widths. This was fixed early into development by having the sidebar hide when below a certain width and making it toggleable instead.



### Planned Features
Even though the app already contains a lot of functionality, there are still things I would like to add at a later date. The list is huge, but these are the 3 I'd prioritise first.

#### Recurring Subscriptions
Once a solid user base had been built, with a not insignificant number of Premium members, I'd switch the payment model to a monthly / annual subscription format instead of the current one-off lifetime membership system.

#### Detailed User Statistics
Everyone loves a bar chart, right? The profile page can be expanded so instead of just totalling the user's bookmarks, pages & collections, there could be more detailed stats at the user level and site wide statistics too.

#### Bookmark Sharing
This was actually planned from the beginning and whilst it would have been relatively simple to add, time just ran out. Users would be able to mark individual collections and / or pages as public and each user would have their own public link, along the lines of `/users/[username]`. Users could share this URL with others, including non-users, and make their bookmark collections publicly available.

## Technologies Used
### Languages
- [HTML](https://html.spec.whatwg.org/multipage/) used as the markup language
- [CSS](https://www.w3.org/Style/CSS/) used to style the HTML
- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) used mostly for DOM manipulation
- [Python3](https://www.python.org/) used to run the backend application

### Frameworks and Libraries
- [Bootstrap 4](https://getbootstrap.com/docs/4.0/getting-started/introduction/) provided the CSS framework
- [Font Awesome 4](https://fontawesome.com/v4.7.0/) is used for the various icons throughout the app
- [Google Fonts](https://fonts.google.com/) serves the fonts used in the app
- [jQuery](https://jquery.com/) is used for many things, for example DOM manipulation, buttons, AJAX requests, and more
	- [Swipe.js](https://github.com/dsheedes/swipe) is a small jQuery plugin that detects swipes and is used to hide the sidebar on mobile devices.
- [jQuery UI](https://jqueryui.com/) is used to allow the user to drag and drop elements on the page when sorting bookmarks, collections, and pages
	- [jQueryUI Touch Punch](http://touchpunch.furf.com/) is a jQueryUI hack that makes jQueryUI play nice with touch events
- [Tippy.js](https://atomiks.github.io/tippyjs/) is used to provide tooltips throughout the app
- [Django v2.2](https://docs.djangoproject.com/en/3.0/releases/2.2/) is the Python framework used to power the app itself. Various Python packages have been used and they are listed below.
<details>
	<summary>Python Libraries - click to view</summary>
	
Packages that are only dependencies of others are not included. The full list can be found in the requirements folder.

Package|Version|Description
---|---|---
beautifulsoup4|4.8.2|A library that makes it easy to scrape information from web pages
boto3|1.11.6|The AWS SDK for Python, used to connect to S3 buckets
coverage|4.5.4|Package for measuring code coverage, typically during test execution
dj-database-url|0.5.0|Utilizes the 12factor inspired DATABASE_URL environment variable to configure a Django application.
Django|2.2.7| The Django framework itself
django-appconf|1.0.3|A helper class for handling configuration defaults of packaged Django apps gracefully
django-cleanup|4.0.0|Automatically deletes files for `FileField`, `ImageField` and subclasses
django-crispy-forms|1.8.1| Controls the rendering behaviour of Django forms
django-storages|1.8|Provides a variety of storage backends in a single library, used in this case to connect with AWS S3
favicon|0.7.0|Library that returns URL's for website favicon(s)
gunicorn|20.0.4|A Python WSGI HTTP Server for UNIX
Pillow|7.0.0|Python Imaging Library (Fork) for handling bookmark icons
psycopg2|2.8.4|PostgreSQL database adapter
requests|2.22.0| Simplifies HTTP requests
stripe|2.40.0|Library for Stripe’s API
whitenoise|5.0.1|Simplified static file serving for WSGI applications
</details>

### Tools
-  [Visual Studio Code](https://code.visualstudio.com/) - The IDE used during development
- [AWS S3 Buckets](https://aws.amazon.com/s3/) - Used to host and serve user uploaded / scraped images
- [Stripe](https://stripe.com/) - For accepting payments when users upgrade to Premium
- [Photoshop](https://www.photoshop.com) - Image editing and manipulation
- [TinyPNG](https://tinypng.com/) - To reduce image file sizes
- [Balsamiq](https://balsamiq.com/) - For creating the initial wireframes
- [ScreenToGif](https://www.screentogif.com/) - For recording the animated gifs on the features page
- [StackEdit](https://stackedit.io/) - Markdown editor used for the readme and testing documents
- [Imgur](https://imgur.com/) - Hosting external image files used with this documentation
- [Git](https://git-scm.com/) - For version control
- [GitHub](https://github.com/) - Remote storage and sharing of the apps code
- [Spotify](https://www.spotify.com/) - Because music

### Databases
- [SQLite3](https://www.sqlite.org/index.html) - The default Django database, used during development
- [PostgreSQL](https://www.postgresql.org/) - The production database, provided by, and deployed to, Heroku

### Hosting
- [Heroku](https://www.heroku.com/) - Used to host the deployed version of this app

## Testing
For testing, refer to the [testing document](TESTING.md).

## Deployment
### Local Deployment
The following instructions are based on the user running VSCode on Windows 10. If your IDE / OS is different, your commands may differ slightly, but the process remains the same.

You will need [Python 3](https://www.python.org/downloads/) (ideally the latest version, but 3.5 as a minimum) installed on your machine. You will also need [PIP](https://pypi.org/project/pip/) which comes preinstalled with Python versions 3.4 and later. Having [Git](https://git-scm.com/) is also highly recommended.

The following steps will allow you to deploy locally:
- Save a copy of the repo on your local machine or use ``git clone https://github.com/steview-d/bookmarks.git`` and cd into the correct folder using the terminal.
- Create a virtual environment, using ``python -m venv .venv`` where ``.venv`` is the environment name.
- Activate the virtual environment with ``.venv\Scripts\activate ``
- Install any required modules with ``pip install -r requirements.txt``
- Create a file called `env.py` in the project root and set up the required local environment variables, like below
```
import os

os.environ.setdefault("SECRET_KEY", "<Enter Your Django Secret Key here")
os.environ.setdefault("HOST_NAME", "127.0.0.1")
os.environ.setdefault("DEBUG", "1")

# email
os.environ.setdefault("EMAIL_ADDRESS", "<Email Address App Will Use To Send Emails")
os.environ.setdefault("EMAIL_PASSWORD", "<Password For Above Email Address>")
os.environ.setdefault("EMAIL_HOST",  "<Your outgoing mail server")
os.environ.setdefault("EMAIL_PORT",  "<Your smtp port>")

# stripe keys
os.environ.setdefault("STRIPE_PUBLISHABLE", "<Enter Your STRIPE_PUBLISHABLE value here>")
os.environ.setdefault("STRIPE_SECRET", "<Enter Your STRIPE_SECRET value here>")
```

NOTE: When deploying locally, there is no need to set up AWS S3 buckets as all media files are served locally

- Run `python manage.py runserver` in the terminal. This will create a local sqlite3.db file for us to use.
- Once this has run, close the server with `CTRL + C`
- In the terminal, run `python manage.py migrate` to set up the database. There is no need to `make migrations` as the migration files are already present.
- Create a superuser using `python manage.py createsuperuser` - you will need to enter a username, email address and password (twice).
- Start the server up again with `python manage.py runserver`
- Open the app in a browser window by navigating to `http://127.0.0.1:8000/accounts/login` and login with your newly created superuser.
- Once logged in, navigate to the admin panel at `http://127.0.0.1:8000/admin` and click on `groups`.
- Click `Add Group` (top right corner) and in the first field (`Name`) enter `Premium` (case-sensitive), and press `Save`.
- You will likely want your user to have access to Premium features, and you can do this in one of 2 ways
	- Add them to the `Premium` group from the Admin panel by selecting `Users > 'Your User' > Groups > Premium`. Once Premium has been added to the `Chosen groups` column, just click `Save`.
	- Or sign up for Premium using the Premium upgrade form within `Settings > Premium`. You can use the Stripe test card details found [here](#upgrade-to-premium-tier).

Once these steps have been completed, the app will be up and running on your machine.

### Deploying To Heroku

These instructions make the following assumptions

- The app has been deployed locally, following the above steps, and then pushed to your own GitHub account.
- The env.py should be added to your .gitignore
- You have created and configured an [AWS S3 Bucket](https://aws.amazon.com/s3/) for serving the media files
- You have a [Stripe](https://stripe.com) account

```
There should be no reason to create a Procfile or requirements.txt file.
These files should already be present in the cloned repository.
```

Once all the above is in place, the instructions below will enable you to deploy to Heroku.

- Go to [heroku.com](https://heroku.com) and log in or create an account.
- Add a new app, give it a name, choose a region and click `Create app`.
- On the dashboard, click the `resources` tab. From within the `addons` input field start typing `post` until you can select `Heroku Postgres` and select it.
- In the plan box that pops up, select `Hobby Dev - Free`, then click `Provision`.
- Once set up, click the Postgres database, select the `settings` tab and `Database Credentials` heading. Make a note of the `URI` value, you will need it later. It will start with `postgres://...`
- Go back to the Dashboard, and from the `Setttings` tab, click the `Reveal Config Vars` button and add the following key / value pairs
	- `EMAIL_ADDRESS` - The email address you want the app to send emails from
	- `EMAIL_PASSWORD` - The password for above email address
	- `EMAIL_HOST` - The Outgoing Mail Server for your email, for example `smtp.gmail.com`
	- `EMAIL_PORT` - Your SMTP port, usually `25`, `465`, or `587`
	- `SECRET_KEY` - Use a Django Secret Key Gen, for example [this one](https://miniwebtool.com/django-secret-key-generator/).
	- `HOST_NAME` - The URL you are deploying to, for example `links-sw.herokuapp.com`
	- `STRIPE_PUBLISHABLE` - Your Stripe API `Publishable key`
	- `STRIPE_SECRET` - Your Stripe API `Secret key`
	- `DATABASE_URL` - This should already be here after you created the Postgres db, but if not, it is the Postgres URI you made a note of earlier.
	- `AWS_ACCESS_KEY` - Your AWS Access Key
	- `AWS_SECRET_ACCESS_KEY` - Your AWS Secret Access Key
	- `AWS_STORAGE_BUCKET_NAME` - The name of the Bucket being used for this app
- Prepare the new Postgres db, by following these steps
	- From your local IDE, add the following entry to your env.py file. (The `postgres//....` value can be copied from the Heroku config vars) and restart your IDE to allow the new environment variable for the database to take effect.
		```
		os.environ.setdefault(
			"DATABASE_URL",
			"postgres://<your value here>"
		)
		```
	- Your local deployment should now be connected to the remote Postgres db so you can run:
		- `python manage.py migrate` to set up the database
		- `python manage.py createsuperuser` to set up your admin account.
	- Delete / comment out the `DATABASE_URL` entry in your `env.py` file.
- Back in the Heroku Dashboard, click the `Deploy` tab and scroll down to `Deployment Method`. Select `GitHub` and link your account and repository.
- Scroll down further to `Manual Deploy`, choose the branch you wish to deploy and click `Deploy Branch`
- Wait for the app to build, and once complete, click `view` to launch your app in the browser.
- Log in with the superuser details you created and navigate to the admin panel at `your-deployment-url/admin`
- Repeat the instructions from [Local Deployment](#local-deployment) to add the `Premium` group and give access to your superuser:
	- Click on `Groups` then `Add Group` (top right corner) and in the first field (`Name`) enter `Premium` (case-sensitive), and press `Save`.
	- You will likely want your superuser to have access to Premium features, and you can do this by adding it to the `Premium` group from the Admin panel by selecting `Users > 'Your User' > Groups > Premium`. Once Premium has been added to the `Chosen groups` column, just click `Save`.
		

## Credits
### Content

All content, words, and design are my own, unless otherwise stated below.

### Media
The original bookmark icon was sourced from [favpng.com](https://favpng.com/).

The site icons for this app (favicons, and so on) were generated by [realfavicongenerator.net](https://realfavicongenerator.net/) using a modified version of the original bookmark icon as the source.

The icons in the 4x4 grid on the index were all scraped from their own sites, using this app. The tiled background image used in areas of the app was put together using icons scraped by this app.

The portrait images for the `user reviews` section were used with permission from [Vecteezy]([https://www.vecteezy.com/vector-art/138266-free-headshot-vector](https://www.vecteezy.com/vector-art/138266-free-headshot-vector))

The `FREE` .png image file used on the pricing page was sourced using Google image search.

### Code

##### csrf.js
Used to pull Django csrf tokens from the page for use with ajax requests.
Code sourced from Emad Mokhtar @ [stackoverflow](https://stackoverflow.com/questions/35112451/forbidden-csrf-token-missing-or-incorrect-django-error/35113457)


##### _spinner.scss
Spinner used when processing ajax requests sourced from [https://tobiasahlin.com/spinkit/](https://tobiasahlin.com/spinkit/) and used with minor modifications.

All other code, outside of frameworks and libraries, is my own.

### Acknowledgements
Vitor  Freitas at [https://simpleisbetterthancomplex.com/](https://simpleisbetterthancomplex.com/) - outside of Stack Overflow, this was usually the place that helped me solve some of the bigger problems I encountered. Some great articles that cover key concepts in an easy to understand way.

The [Try Django 2.2](https://www.codingforentrepreneurs.com/projects/try-django-2-2) mini project is a free step-by-step guide to building a blog with Django, and even though Django blog tutorials are ten a penny, this one is highly recommended.

Thanks to [Attila Szaloki](https://github.com/aticodein) for help with testing and feedback.
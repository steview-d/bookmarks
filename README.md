#### WIP - Still needs spellchecking, amongst other things.....

# Links

Links is a bookmarking app built using Pythons Django framework, and hosted with Heroku.
The main function of the app is to allow users to save the urls of any website for easy reference. Users can also edit and delete their saved bookmarks, and there are numerous options to allow users to organise and display their collection in a way of their own choosing.

The deployed app can be found at [links-sw.herokuapp.com](https://links-sw.herokuapp.com)

## Contents


1. [UX](#ux)
-- [User Stories](#user-stories)
-- [Design](#design)
-- [Wireframes](#wireframes)

2. [Features](#features)
-- [Current Features](#current-features)
-- [Planned Features](#planned-features)

3. [Technologies Used](#technologies-used)
-- [Languages](#languages)
-- [Libraries](#libraries)
-- [Tools](#tools)
-- [Hosting](#hosting)

4. [Testing](#testing)
-- For testing, refer to the [testing document](test.md).

5. [Deployment](#deployment)
-- [Local Deployment](#local-deployment)
-- [Deploying To Heroku](#deploying-to-heroku)


6. [Credits](#credits)
-- [Content](#content)
-- [Media](#media)
-- [Code](#code)
-- [Acknowledgements](#acknowledgements)

## UX
The app can be split into 3 distinct sections
1. The 'introductory' pages. These introduce potential users to the app, sharing information such as features, pricing, FAQ's, and providing login / register options.
2. The settings pages. Here users can update their profile, get support, and upgrade to a Premium account.
3. The main app page. This is where users can view, add, edit, organise, and delete their bookmarks.

Section 1 is only available to users who are logged out and unregistered, whilst sections 2 and 3 are only for logged in / registered users. This is intentional, as once a user has committed to creating an account, they should have no need for the initial pages, whose only purpose was to sell the app and encourage registration.

For this reason, the design of the introductory section is intentionally different to the other sections. Whilst they share similar design elements (colors, fonts, logos, etc) the intro pages make use of a single navigation bar at the top, whilst the main app and settings sections use a sidebar for navigation within the current section, and a top navigation bar for other features, such as search and swapping between sections (settings / main app).

### User Stories
#### As a user, I expect to be able to:
- Save a webpage url so I can revisit the page at a later date
- Store multiple 'bookmarks' within my account
- Organise my bookmarks into collections of similar bookmarks
- Have multiple pages, each containing multiple collections of bookmarks
- Order the bookmarks, pages, and collections in a way of my own choosing
- Edit my existing bookmarks should they need updating
- Move bookmarks from 1 collection and / or page, to another
- Delete bookmarks I no longer require
- Easily import bookmarks from the page I want to save with just a few clicks, without the need for needless copy/paste actions
- Let the app scrape data from the page I want to save to automatically create a suitable title and description
- Save an icon with the bookmark so I can easily identify the bookmark at a glance. Additionally, I should be able to choose the icon by either uploading my own, letting the app use the web page icon, or allow the app to create one of its own
- Update my personal details (email / password) if required
- Get support in the event of my being stuck, or if I have questions relating to the app
- Pay to upgrade to a 'Premium' membership tier, giving me access to features otherwise unavaible to users who are using the app for free.
- Have access to this app and my bookmarks across a range of devices and displays

#### As the site admin, I expect to be able to:
- Manage the site and its users through a dedicated backend admin portal
- Be notifed of support requests and be able to respond effectively
- Be able to track users who have signed up for a Premium membership
- Easily receive feedback from users

### Design

#### Application Framework
This app uses the Django framework

#### Database
Django uses SQL databases. During development the Django default sqlite3 database was used. When deployed to Heroku, a PostgreSQL database was used.

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
The first pages a user encounters are the 'sales pitch' pages. These 3 pages (index/home, pricing, faq's) are designed with a single purpose in mind - to convince the user to create a free account and give the app a try. Each page fulfils the following role as part of the overall pitch
##### Home
Introduces the app and inside of a few short lines gives a high level overview of what it does. A 4x4 grid of icons from familiar and well known websites (chosen from a random pool of 100+) is displayed alongside to allow the user to make a connection between this app and (potentially) some of their favorite sites.

The features section is designed to give users a deeper insight into how the app functions, and what they can expect if they sign up. It focuses on customisation options, and lets users know they have a large degree of control over how they choose to use the app. Animated gifs are provided so users can see first hand how the app works. For users wanting more information on features, there is a link to take them straight to a comparison table on the pricing page.

The next section introduces the Chrome browser extension, and the text focuses on how the extension makes it easier for users to use the app, and how it is free to use. There is a link to take the user to the Chrome Web Store so they can install it quickly and easily.

A user reviews section contains quotes from current users. Each review has been tailored to highlight and promote a specific aspect of the app.

Finally, at the bottom of the page, just before the footer, there is a link to take the user to the login / register screen. This is here as part of the overall effort to make it as easy as possible to create an account from any part of the site.

##### Pricing
This page focuses on the free aspect of the app, and assures users the app is fully functioning whether they choose to upgrade to Premium or not.

A comparison table reinforces this by showing the main differences between the 2 tiers. It's laid out in such a way so as to show that Premium membership just means 'bigger, better, more' rather than Free meaning 'limited functionality'.

A 'launch offer' is in place to let users know if they do decide to go for the Premium tier, it's only a 1 off payment for full lifetime access. The limited nature of this offer is designed to encourage users to sign up sooner rather than later.

As with the home page, the final section is a link to the user register / login screens.

##### FAQ
A standard FAQ section, with questions picked that best promote a key aspect of the overall user experience, such as support, feedback, and so on.

Below this is a contact form that non-registered users can use to get in touch with the app's admin. Registered users can use it too, but as there is a dedicated support system in place inside of the app itself, it's expected the vast majority of contacts will be from non users.

Lastly, as with previous pages, there is a button directing users to register / login.

#### New User Registration
Users can create a new account from this page. There are no restrictions on who can create an account, and it is free to do for all users. Users must provide a unique username and email address, whcih are checked against existing entries. A password is required, which must be entered twice to check it has been inputted correctly.

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
The app uses the built in password reset system provided by Django, although the pages have been customised to match the design of the rest of the site.

From the login page, a user can access the 'forgot your password' link whereby they provide an email address and if a match is found, they will recieve an email with a link allowing them to create a new password.

#### Full Admin Backend for Easy Admin Management
The standard Django admin pages have been customised to make make managing the app easier for admins. The look and feel hasn't been changed as it's not an area a standard user will ever access or even see, but additional layouts, filters, and actions have been added to aid the overall admin experience.

Some examples of admin backend customisation
##### Users
'Groups' has been added to the list of filters, so the user can filter by All / Premium / No Group (Free Tier).

Additionally, a 'Membership Status' column has been added to the user overview page. There is no membership status field in this model, this is handled by Django User Groups so this had to be defined in the admin<span></span>.py file for the accounts app.

![](https://i.imgur.com/oGHKcYq.png)

##### Bookmarks
The individual bookmark view has been updated to group the different fields into relevant sections using fieldsets.
'added' and 'updated' have been added here too. They wouldn't show up by default due to being readonly fields but have been added to assist with any potential troubleshooting that might be required when dealing with support tickets.

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

Overview columns show just top level information and a custom column called 'Admin Comments' has been added. This checks to see if the field 'Admin Comments' contains any data and displays accordingly, allowing admins to see at glance if work has already started on an individual ticket.

![](https://i.imgur.com/zoT6kGC.png)

A filter has been added for the status field to allow an admin to filter by All / Open / Closed.

The individual ticket display has been customised to separate the ticket data into sections to make it easier for admins to quickly focus on the data they need. There are 3 areas, split into user details, ticket details, and admin actions (comments and status).

#### Messages System
The app makes use of the built in messages framework that comes with Django. Any time the app needs to communicate an important event to the user, such as confirmation of an actions success or failure, the message is flashed at top of the screen, just below the top navigation bar.
![](https://i.imgur.com/gstGn6j.png)
![](https://i.imgur.com/XNjnHAP.png)

The message tag is used to set the bootstrap color class (success green, orange warning) and so on so the user can immediately tell what type of message it is. Messages can be manually closed, or they will disappear on a new page load / refresh.

#### Built In Support Ticket System
Registered users can open a support ticket to help with anything related to the app. The form is simple, requiring only a title and message, and the ticket will be opened and viewable from within the admin panel. Details of how an admin would manage this ticket can be found in the previous section on the admin backend, specifically [this section on tickets](#tickets).

From a user perspective, once the form is submitted, they will recieve an email confirming receipt of their ticket which will also contain a copy of their support request.

<details>
	<summary>Example Support Ticket Email</summary>

![](https://i.imgur.com/XZSWbtS.png)
<details>

#### Premium Functionality for Paying Users
#### User Profile Page
#### Side Navigation Bar
#### Top Navigation Bar
#### Search Functionality
#### Add Bookmark
#### Automatic Scraping of Pages for Bookmark Data
#### URL Validation
#### Edit Bookmark
#### Move Bookmark
#### Delete Bookmark
#### Browser Extension for Easy Importing of Bookmarks
#### Bookmark Display Options
#### Bookmark Sort Options

### Planned Features
Even though the app already contains a lot of functionality, there are still things I would like to add at a later date. The list is huge, but these are the 3 I'd prioritise first.
#### Recurring Subscriptions
Once a solid user base had been built, with a not insignificant number of Premium members, I'd switch the payment model to a monthly / annual subscription format instead of the current one-off lifetime membership system.
#### Detailed User Statistics
Everyone loves a bar chart, right? The profile page can be expanded so instead of just totalling the users bookmarks, pages & collections, there could be more detailed stats at the user level and site wide statistics too.
#### Bookmark Sharing
This was actually planned from the beginning and whilst it would have been relatively simple to add, time just ran out. Users would be able to mark individual collections and / or pages as public and each user would have their own public link, along the lines of `/users/[username]`. Users could share this url with others, including non-users, and make their bookmark collections publically available.

## Technologies Used
### Languages
- [HTML](https://html.spec.whatwg.org/multipage/) used as the markup language
- [CSS](https://www.w3.org/Style/CSS/) used to style the HTML
- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) used mostly for DOM manipulation
- [Python3](https://www.python.org/) used to run the backend application

### Frameworks & Libraries
- [Bootstrap 4](https://getbootstrap.com/docs/4.0/getting-started/introduction/) provided the CSS framework
- [Font Awesome 4](https://fontawesome.com/v4.7.0/) is used for the various icons throughout the app
- [Google Fonts](https://fonts.google.com/) serves the fonts used in the app
- [jQuery](https://jquery.com/) is used for many things, for example DOM manipulation, buttons, AJAX requests, and more
	- [Swipe.js](https://github.com/dsheedes/swipe) is a small jQuery plugin that detects swipes, and is used to hide the sidebar on mobile devices.
- [jQuery UI](https://jqueryui.com/) is used to allow the user to drag and drop elements on the page when sorting bookmarks, collections, and pages
	- [jQueryUI Touch Punch](http://touchpunch.furf.com/) is a jQueryUI hack that makes jQueryUI play nice with touch events
- [Tippy.js](https://atomiks.github.io/tippyjs/) is used to provide tooltips throughout the app
- [Django v2.2](https://docs.djangoproject.com/en/3.0/releases/2.2/) is the Python framework used to power the app itself. Various Python packages have been used and they are listed below.
<details>
	<summary>Python Libraries - click to view</summary>
	
Packages that are only dependancies of others are not included. The full list can be found in the requirements folder.

Package|Version|Description
---|---|---
beautifulsoup4|4.8.2|A library that makes it easy to scrape information from web pages
boto3|1.11.6|The AWS SDK for Python, used to connect to S3 buckets
coverage|4.5.4|Package for measuring code coverage, typically during test execution
dj-database-url|0.5.0|Utilizes the 12factor inspired DATABASE_URL environment variable to configure a Django application.
Django|2.2.7| The Django framework itself
django-appconf|1.0.3|A helper class for handling configuration defaults of packaged Django apps gracefully
django-cleanup|4.0.0|Automatically deletes files for `FileField`, `ImageField` and subclasses
django-crispy-forms|1.8.1| Controls the rendering behavior of Django forms
django-storages|1.8|Provides a variety of storage backends in a single library, used in this case to connect with AWS S3
favicon|0.7.0|Library that returns the url of a website favicon(s)
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
For testing, refer to the [testing document](test.md).

## Deployment
### Local Deployment
### Deploying To Heroku

## Credits
### Content
### Media
### Code
### Acknowledgements
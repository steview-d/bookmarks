<p align="center">
  <img src="https://i.imgur.com/wwb33jN.png">
</p>

# Testing
Deployed App at [links-sw.herokuapp.com](https://links-sw.herokuapp.com)
Back to main [README.md](README.md)

A mix of manual and automated testing has been used to ensure the app works as intended. Currently, there are no outstanding bugs or issues that I am aware of (famous last words).
If any bugs, issues, or generally undesirable behaviour is found, I'd be grateful if you could take the time to report it to me through the built-in support system [here](https://links-sw.herokuapp.com/accounts/support/).

## Contents
1. [Automated Testing](#automated-testing)
	- [Unit Tests](#unit-tests)
	- [Coverage](#coverage)

2. [Manual Testing](#manual-testing)
	- [Browser Compatibility](#browser-compatibility)
	- [Console Errors & Warnings](#console-errors-and-warnings)
	- [Features Testing](#features-testing)

3. [Code Validation](#code-validation)
	- [Python](#python)
	- [JavaScript](#javascript)
	-  [HTML](#html)
	- [CSS](#css)


## Automated Testing

### Unit Tests
A suite of 80 tests (at last count) are in place to test the app. Approximately half of these were written alongside the project itself, and mainly relate to the individual apps for `accounts`, `support`, `premium`, `intro pages` and so on - basically everything but the ``links`` and ``search`` apps.
The remaining tests for the `links` and `search` apps were written after the app was complete and will be useful for when the app is expanded at a later date.

To run the tests locally (on Windows) use `python manage.py test`

### Coverage
The [Coverage](https://pypi.org/project/coverage/) library was used throughout testing to help keep track of how much of my code was covered by the tests. As it stands, there is 77% coverage across the project. I would have liked to have added more tests, especially ones focused on the main links app and associated helper functions in the utils folder, but time became a factor. However, even without the additional tests, I feel that along with the manual testing I have completed, the app is in good health and works as expected.

To generate your own coverage report (again, on Windows)
- Coverage should already be installed from the `requirements.txt` file, but if not, install with `pip install coverage`
- Run `coverage run manage.py test`
- Then `coverage html` to generate the report
- The report can be viewed in a browser by opening the `index.html` file from inside the `htmlcov` folder.



## Manual Testing

### Browser Compatibility
The app has been tested across a range of different devices, browsers, and screen sizes. These were display tests, to check the pages rendered correctly.
The tables below show what has been tested, along with the results of these tests.

Device | Chrome v80 | Chrome v81 | Firefox v75 | Safari v12 | Safari v13 | Opera v67 | Edge v81 | IE11 v11
---|---|---|---|---|---|---|---|---
Win 10 PC :one:|:heavy_minus_sign:|:heavy_check_mark:|:heavy_check_mark:|:heavy_minus_sign:|:heavy_minus_sign:|:heavy_check_mark:|:heavy_check_mark: :two:|:x: :three:
Apple Mac Book |:heavy_minus_sign:|:heavy_minus_sign:|:heavy_minus_sign:|:heavy_minus_sign:|:heavy_check_mark:|:heavy_minus_sign:|:heavy_minus_sign:|:heavy_minus_sign:
iPad Mini  |:heavy_minus_sign:|:heavy_minus_sign:|:heavy_minus_sign:|:heavy_check_mark: :four:|:heavy_minus_sign:|:heavy_minus_sign:|:heavy_minus_sign:|:heavy_minus_sign:
iPhone 8 |:heavy_minus_sign:|:heavy_minus_sign:|:heavy_minus_sign:|:heavy_check_mark: :four:|:heavy_minus_sign:|:heavy_minus_sign:|:heavy_minus_sign:|:heavy_minus_sign:
Pixel 2 XL |:heavy_check_mark:|:heavy_minus_sign:|:heavy_minus_sign:|:heavy_minus_sign:|:heavy_minus_sign:|:heavy_minus_sign:|:heavy_minus_sign:|:heavy_minus_sign:
Samsung Galaxy Tab A |:heavy_check_mark:|:heavy_minus_sign:|:heavy_minus_sign:|:heavy_minus_sign:|:heavy_minus_sign:|:heavy_minus_sign:|:heavy_minus_sign:|:heavy_minus_sign:

:heavy_check_mark: - Tested, No Issues Found
:x: - Tested & Issues Found, See Notes
:heavy_minus_sign: - Not Tested

:one: Tested on multiple displays of differing widths: 1400px, 1920px, 2560px and 3440px.

:two: Originally tested with Edge v44 (EdgeHTML). The site worked and was fully functional, but there were issues with how flex elements were displayed. They would appear to expand to normal size on page load and whilst this effect was only slight, it was noticeable. More noticeable was how the side bar would pop / slide in to view on each page load. After investigating, it seems these issues come from how EdgeHTML handles flex in general.
EdgeHTML has not been updated since October 2018, so I can't see this ever changing for this version of the Edge browser. However, after updating Edge to use the newer Chromium based version, these issues are no longer present so it's an issue that will fix itself over time as users automatically switch to the new Edge through automatic Windows updates.

:three: I never intended the app to work with IE11, it was more a case of if it works then great, but it most likely won't. And it doesn't. In the most part, the lack of compatibility comes down to IE11 not supporting ES6 and because a lot of the apps functionality is dependent on JavaScript, the console just spits out errors and halts the script.
I could rewrite all the JS to be compatible with IE11, but it would not be time well spent. If there was more time, I would spend it adding more features, not trying to breathe life into a dead browser.

:four: Numerous issues displaying the site properly with the Safari mobile browser. All since fixed, and mostly due to Safari not registering touch events unless the element is a `<div>` or `<a>`. Some issues fixed by changing the element, but most by adding `cursor: pointer` CSS to the element to allow Safari to register a touch event.

### Console Errors and Warnings
The Chrome DevTools console has been used to check for errors and warnings.
No errors have been found.
1 warning is present when accessing the ``Premium`` page from the ``Settings`` sidebar. The error is
```
A cookie associated with a cross-site resource at http://stripe.com/ was set without the `SameSite` attribute. A future release of Chrome will only deliver cookies with cross-site requests if they are set with `SameSite=None` and `Secure`. You can review cookies in developer tools under Application>Storage>Cookies and see more details at https://www.chromestatus.com/feature/5088147346030592 and https://www.chromestatus.com/feature/5633521622188032.
```
I have confirmed this originates from the js script loaded from ``https://js.stripe.com/v2``. Despite the presence of this warning, it has no effect on the app itself.

### Features Testing
For every feature listed in the [features](README.md#current-features) section of the main [README.md](README.md) file, its functionality has been tested to ensure it works as intended.
Tests were initially completed on a PC running Windows 10, and then repeated on an Android mobile with a Pixel 2 XL handset.

#### Top Navigation Bar ( Logged Out )
- Links all go to correct page.
- On scroll down, logo is hidden and just links displayed.
- When scrolled back to the top, logo is shown again.
- On mobile views, `Login` & `Register` are moved to a separate mobile menu with these options contained within a drop-down. Both of these links go to the correct page.
- When scrolling down, a thin border is added to the bottom of the navbar to separate the nav elements from the rest of the page. Removed when scrolled back to the top.

#### Home / About Page
##### Intro Panel & Icon Grid
- 4x4 icon grid should display random icons each time. Multiple page refreshes confirms this.
- `Create Account` button and `or log in here` link both take the user to the correct page.
##### Features Section 
- On non-touch displays, hovering over the images causes the gif to play, and un-hovering causes it to stop and reset to the beginning.
-  On touch devices the behaviour is the same except the gifs activate / deactivate on click as opposed to hover.
The `Compare Features` button takes the user to the feature comparison table on the `Pricing` page.
##### Chrome Extension Panel
- The `Install Extension` button opens a new tab to the Chrome Web Store page for the app extension.
- The large bookmark icon also opens a new tab to the Chrome Web Store page.
##### User Reviews
- The user reviews automatically cycle through all available reviews.
- The buttons to the sides of each review also allow the user to manually move between each review.
##### User Authentication Options
- `Create Account` button and `or log in here` link both take the user to the correct page.

#### Pricing Page
- The `Compare Features` button scrolls down to the feature comparison table.
##### User Authentication Options
- `Create Account` button and `or log in here` link both take the user to the correct page.

#### FAQ Page
##### FAQ Section
- Clicking on the individual questions expands the container to show the answer.
- When a question container opens to show the answer, any currently open containers are closed.
- The `+` icon inverts when its question is active.
##### Contact Form
- When submitted, a `Contact` object is created to store the message details and is viewable in the Admin Back-End.
- All fields are required to be filled out and any missing fields prevent the form from sending.
- If successful, the messages system alerts the user that the message has been sent.
- If unsuccessful, the messages system communicates this and invites the user to review their message and fix the errors.
##### User Authentication Options
- `Create Account` button and `or log in here` link both take the user to the correct page.


#### User Authentication
##### Log In System
- Confirmed login system works for registered users.
- If a user enters incorrect details, this is communicated to them.
- Link for `Forgot Your Password?` goes to the correct page.
- `Need an account? Create one here` correctly links to the register account page.
##### New User Registration
- Confirmed account creation works and upon successful creation of account, user is logged in and taken to the main app page.
- If details are missing or entered incorrectly, no account is created, and the incorrect field(s) tell the user what went wrong.
- Tooltips appear when hovered over or clicked on for touch devices.
- `Already have an account? Log in here` correctly links to the login page.
##### Password Reset
- If something other than an email address is submitted, the user will be informed of this.
- Confirmed email is received when a registered email address is entered.
- Confirmed email link within the sent email works and directs the user to a password reset screen.
- Password reset form checks the passwords match and that the password requirements are met. An error shows if not.
- Tooltip works as expected.
- Confirmed password change works and user is able to log in with new password.

#### Footer
- The 2 links in the footer both open new tabs and link to the correct page.

#### Admin Back-End
##### Users
- User model overview shows custom field view as expected.
- `Membership Status` column correctly shows whether a user is `Standard` or `Premium` by checking if the user has been assigned to the `Premium` group, or not.

##### Bookmarks, Collections & Pages
- All models have been customised to display specific columns to better enable Admin users to manage the app. Confirmed they all display as intended.

##### Contacts
- Confirmed whenever a user successfully submits a contact form, it shows here for the Admins to manage. 

##### Premium Purchases
- Confirmed when a user upgrades to `Premium`, their upgrade details are stored here.

##### Support Tickets
- Confirmed when a registered user opens a support request, a ticket is created and is viewable from the Admin panel.
- Confirmed when an Admin adds comments via the `Admin Comments` field in the Admin panel, the `Tickets` overview successfully shows a Boolean value for whether comments exist or not.
- Confirmed the custom actions of `Close Selected Tickets` & `Open Selected Tickets` update the status fields correctly and work as intended.

#### Top Navigation Bar ( Logged In )
##### Navigation
- `Logout` button successfully logs out the current user.
- The `Settings` icon directs users the settings pages, specifically the `Profile` page.
- The `Bookmark` icon takes the user to the main app. The app correctly loads the last `Page` the user was on before they navigated away.
- The `Search` bar opens the search page with results for the search term that was submitted. If no search term is entered, the app correctly returns all the users bookmarks, regardless of the `Page` they are part of.
- The `Search` icon, when clicked, opens an input field for the user to enter a search term (smaller screens only)
- The `Add Bookmark` icon correctly navigates the user to the correct page.
##### Responsiveness 
- On larger widths, the only icons on display should be the `Bookmark` main app icon, `Settings` cog icon & `Logout` icon.
- As the screen width is reduced, the sidebar will eventually disappear. The sidebar contains the main `Add Bookmark` button so to compensate for this not being present, a `+` icon is added to the top navigation so the user can still easily add bookmarks. Confirmed this works as intended.
- When the width becomes too small to comfortably display a search input field, it is removed and replaced with a search icon. When clicked, this opens an input field for searching. 

#### Side Navigation Bar ( Settings )
- Confirmed circular bookmark icon links to main app view.
- `Add Bookmark` button links to the correct page.
- Individual links to the different settings pages all lead to the correct page.

#### Messages System
- Confirmed system messages display correctly at top of screen.
- The `x` closes these messages when clicked.
- The message displays the correct color for the message type; Green = Success, Red = Warning, and so on.

#### Premium Page
##### Premium Users
- Correctly displays only a simple `Thanks....` message when viewed by users with `Premium` status.
##### Standard Users
- Confirmed the page displays the benefits of becoming a Premium user.
- Tested with Stripes VISA test card numbers to successfully upgrade a user to Premium.
##### Stripe Payments
- Payments can be taken successfully using Stripe Test Card numbers. For testing, I used the below VISA test numbers
```
Card Number - 4242 4242 4242 4242
Expiry - Any future date
CVC - Any 3 digits
```
Initially, all validation was done by Stripe, with Stripe returning either a HTTP 200 to show everything went through fine, or a custom error message to inform the user of the problem. This message is displayed at the top of the form, making it easy for the user to see what the issue is.

During testing, 2 issues were found with how Stripe validates card details when in test mode.

Using the `4242 4242 4242 4242` number pattern would result in a successful payment result, and (almost) any other numbers would return a `YOUR CARD NUMBER IS INCORRECT.` message. However, using `4242 4242 4242` initially resulted in the app throwing an `ISE 500` error.

When reviewing the logs, this message was found
``stripe.error.CardError: Request req_xxxxxxxxxxxxxx: Your card was declined. Your request was in test mode, but used a non test (live) card. For a list of valid test cards, visit: https://stripe.com/docs/testing.``

The issue appeared to be Stripe initially accepting the shortened `4242...` pattern as a valid card, but then denying the request when realising that test mode was active.

The second issue was with the 3-digit security code. If this field was left blank, and a valid test card was used for the card number, then the form would pass, and the test payment would be authorised. The Stripe documentation makes it clear this is intended behaviour, in that it does not require this field to be completed when in test mode. That said, it still didn't seem right to have the app accept an empty field, so a fix was added.

To fix both of these issues, a further validation check was added to `stripe.js`. Once Stripe returns a HTTP 200 status, and before processing the payment, the app checks to make sure the card number is 16 digits and the CVV is 3 digits.

Whilst these checks weren't necessary as this behaviour is only due to how Stripe's test mode functions, it does prevent unwanted errors and behaviour. When the payment system does go live these additional validation checks can be removed as the live system will process the card and CVV numbers as normal.


#### User Profile Page
- Page correctly displays date the user created an account.
- `Premium Member` badge added if user has `Premium` status.
##### Forms
- `Update Email Address` form correctly updates email address when supplied with a valid email.
- Displays error if something other than an email address is entered.
- `Change Password` form correctly updates the users password providing a valid password is entered.
- Displays error if passwords do not match, or password criteria is not met.
##### User Preferences
- Confirmed if `Show warning when.....` box is ticked, then warnings are displayed when there are too many columns for the current display width.
- Equally, confirmed no warnings show when not ticked.
- Confirmed box loses tick if user chooses to dismiss warnings when given the option during normal app use.
##### User Stats
- Checked multiple users to confirm values displayed are correct and accurately represent the users number of Bookmarks, Pages & Collections.

#### Support Page
- Tested `Support Request Form` successfully creates a `Ticket` object.
- Confirmed a copy of this support request is emailed to the user.
- Confirmed if either field is missing, no ticket is created, and user is informed of errors that require correcting.
##### Premium Users
- `Priority Telephone Support` number is displayed if logged in user has `Premium` status.
##### Standard Users
- A button linking to the Premium sign up page is provided in place of the telephone support number when this page is viewed by a standard member.

#### About Page
- Displays the current app version number correctly.
- Correctly displays a different message re: Premium depending on Premium status.
- Link to `Support` page goes to the correct page.

#### Side Navigation Bar ( Main App )
- Confirmed circular bookmark icon links to main app view.
- `Add Bookmark` button links to the correct page.
##### Sort Page Order Button
- When clicked, changes color to show sort mode is active.
- Individual pages are prepended with an icon to signify the pages are sortable.
- Confirmed pages can be sorted and new order is retained when exiting sort mode.
##### Add New Page Button
- On click, `Add New Page` form is displayed.
- Can choose from between 1 and 5 columns, no more no less, which is correct.
- If there is an error with the form, on page reload the error is shown and the form is still visible so the user can immediately see the error.
- On page creation, user is taken to their new page.
##### Links to Different Pages
- Confirmed all page links go to the correct page in the app.
##### Page Options Button
- Clicking the cog icon opens the page options directly below the page name.
###### Arrange Collections Button
- Confirmed `Arrange Collections` button takes the user to the correct page.
###### Change Column Display Button
- Confirmed clicking a `Columns` number button changes the number of columns in view for the current page.
###### Rename Page
- Entering a new name for the page and selecting "Rename" works as intended.
- App returns an error if invalid chars are entered.
- App checks user doesn't already have a page with this name (case-insensitive).
###### Delete Page
- Confirmed `Delete` button deletes the `Page` and all `Collections` & `Bookmarks` contained within.
##### Premium Status
- If a user has upgraded to Premium, this will be displayed below the page names.
- If a user has not upgraded, nothing will be displayed.

#### Search
- Confirm all search results have their own options icon to the right allowing the user to `Edit`, `Move` or `Delete` the bookmark.
- Confirmed all Bookmark options take the user to the correct page or perform the expected action.
##### Pagination
- Confirmed pagination kicks in when search returns more than 10 results.
- Confirmed pagination buttons all work as expected.
- Confirmed pagination options at top and bottom of search results.

#### Main App View
##### Collection Header - Add Bookmark Button
- Confirmed the `+` icon takes the user to the `Add Bookmark` page.
- Confirmed the `destination collection` dropdown value defaults to the collection from which the `+` button was pressed.
##### Collection Header - Manual Sort Button
- When clicked, changes color to show sort mode is active.
- Confirmed `Manual Sort` only activates if collection is in `Manual Sort Mode`
- Confirmed presence of tooltip to explain this when NOT in this mode.
- Individual style of all bookmarks in the collection change to show `Manual Sort` is active.
- On smaller screens, width of bookmark is reduced to leave a gap to allow the user to scroll through large lists of bookmarks without accidently grabbing a bookmark and causing unwanted sorting.
- Confirmed new bookmark order persists after user exits the sort mode.
##### Collection Header - Options Button
- Clicking the cog icon to the right of the collection header element opens the collection options.
###### Sort By
- Confirmed all possible sort options sort the bookmarks as intended.
- When any sort option other than `Manual Sort` is selected, confirmed this prevents the user from activating `Manual Sort` mode.
###### Display As
- Confirmed all 3 `Display As` options correctly adjust the way the individual bookmarks display.
- Confirmed this only affects the selected `Collection` and has no effect on other collections.
###### Rename Collection
- Confirmed collection can be renamed, providing a collection of the same name (case-insensitive) does not already exist on the current page, and no invalid characters are used.
###### Delete Collection
- Confirmed the `Delete` button deletes the `Collection` and all `Bookmarks` contained within.

##### Bookmark Options Button
- Confirmed individual bookmarks have their own `Bookmark Options` icon which activates a drop-down menu on click.
- Confirmed each option in the drop-down takes the user to the correct page or performs the expected action.

##### Bookmark Description Tooltip
- Confirmed tooltip activates when hovering over the bookmark description on individual bookmarks.
- Confirmed tooltip content is the text from the bookmark description field, in full.
- Confirmed that the tooltips do not show on touch devices.
##### Add New Collection
- When clicked, the `Add New Collection` form appears, and if clicked again, the form is hidden.
- Confirmed can create a new `Collection` using form.
- Confirmed errors are returned if user tries to create a collection with a name already in use on the current page (case-insensitive) or if invalid chars are used.
- Tooltip appears if pointer is hovered over the 'Add New Collection' icon for longer than 700ms.

#### Add Bookmark Page
- When form is completed correctly, a Bookmark is added to the specified `Page` & `Collection`.
##### Scraping
- Auto-Fill works as expected and fills in the required fields.
- Where data cannot be scraped, the user is informed.
##### URL Validation
- The `URL Status` updates accordingly depending on the content of the `URL` field.
- The tooltip activates correctly - hover on desktop, touch for touchscreens.
##### Icon Images
- Files can be uploaded for the icon, and a preview image is displayed correctly.
- Confirmed files above a certain pixel size are resized before being saved to the app.
- Files above 2mb are rejected and the user informed.
- Previously entered information is retained within the form, including images, in the event of an error with certain fields.
- The `Use Default Icon` button clears any scraped / uploaded image, allowing the app to generate its own image as and when required. A preview of how this will look is shown in the `Icon Preview` section.
##### Bookmark Destination
- The Bookmark is correctly saved to the specified destination.
- Confirmed if a `Page` has no collections and a user tries to save a `Bookmark` to this page, an error will be returned informing the user to choose a page with an existing ``Collection``.
- Confirmed if a different `Page` is selected, the app will update the `Destination Collection` drop-down with the new `Collection Destination` options.

#### Edit Bookmark Page
Uses the same 2 forms as `Add Bookmark` but pre-fills the fields on page load. All tests completed for `Add Bookmark` completed for `Edit Bookmark` and no issues found.

#### Move Bookmark Page
Uses the same form for the Bookmark destination as the `Add / Edit Bookmark` pages. This form tested in the same way, and no issues found.

#### Delete Bookmark
- Confirmed the `Delete` button correctly deletes the specified `Bookmark`.

#### Import Url Page
`Import Url` uses the same 2 forms as `Add Bookmark` and works in the exact same way. Therefore, the tests completed are the same also. The only differences are
- `Auto-Fill` happens automatically on page load, rather than waiting for the user to select it.
- There is no side-bar or top navigation element, but this has no impact on the testing of this section.

#### Banner Adverts
- Confirmed adverts only show for users not part of the `Premium` group, i.e. those who haven't upgraded to `Premium`.
- When clicked, adverts open a new tab for [google.com](https://www.google.com/), which is correct as the current adverts are not real.
- Confirmed the `Remove Ads!` link under the adverts takes the user to the `Premium` page so they can sign up for `Premium` membership.

#### Premium Functionality
- Confirmed when a standard user tries to add a 3rd `Page`, the app refuses, displays a message informing them that standard users can have 2 pages at most, and redirects the user to the `Premium` page.
- Confirmed when a standard user tries to add more than 20 collections, the app refuses, displays a message informing them that standard users can have 20 collections at most, and redirects the user to the `Premium` page.
- Confirmed when a standard user tries to add more than 10 bookmarks, the app refuses, displays a message informing them that standard users can have 10 bookmarks at most, and redirects the user to the `Premium` page. The actual limit on bookmarks for standard users is 500, but this was reduced to 10 so the logic could be tested and reset to 500 once complete.

#### Accessing Pages Without Permission
All pages have been checked to ensure they are only accessible when the user is authorised to do.
- The main app and associated functions (Add, Edit, Move, Delete, Arrange, Profile, Support, etc) can only be accessed if a user is currently logged in. If these URL's are tried and no user is logged, the app redirects to the login page.
- The intro & authentication pages (About, Pricing, FAQ, Login & Register) are only accessible when no user is logged in. If a logged in user attempts to view these pages, they are automatically redirected the main app page.

#### Custom Error Pages
- Confirmed that the correct custom error pages (404 & 500) display in the event of these errors.

## Code Validation

### Python
All Python code is fully PEP 8 compliant and has been verified at [pep8online.com](http://pep8online.com/).

### JavaScript
All JavaScript has been verified with the online tool [jshint.com](https://jshint.com/).

### HTML
HTML has been run through [validator.w3.org](https://validator.w3.org/). Outside of errors generated by the Django templating language, all other HTML is valid.

### CSS
The CSS is auto prefixed and compiled from multiple .SCSS files using the VS Code [Live Sass Compiler](https://marketplace.visualstudio.com/items?itemName=ritwickdey.live-sass) extension.
The compiled CSS was run through [jigsaw.w3.org/css-validator](https://jigsaw.w3.org/css-validator/) and produced 2 errors and multiple warnings.

#### Errors
```
Property scrollbar-width doesn't exist : none
```
`scrollbar-width: none` is used to hide the scroll bar on the Firefox browser when displaying the sidebar. This property is currently only supported by Firefox v64+. `::-webkit-scrollbar`, used to achieve the same effect with other browsers, is not compatible with Firefox.

```
text is not a background-clip value : text
```
`background-clip: text` is used for styling the custom 404/500 error pages and is needed to achieve the required effect. Unsure why an error is thrown, but it works and [caniuse.com](https://caniuse.com/#feat=background-img-opts) sort of says it's ok.

#### Warnings
The majority of warnings relate to `unknown vendor extensions` that have been added by the auto-prefixer.  All the warnings have been checked, and none are a cause for concern. 

---
Back to main [README.md](README.md)
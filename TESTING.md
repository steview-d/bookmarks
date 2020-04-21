
<p align="center">
  <img src="https://i.imgur.com/wwb33jN.png">
</p>

# Testing
Deployed App at [links-sw.herokuapp.com](https://links-sw.herokuapp.com)
Back to main [README.md](README.md)

A mix of manual and automated testing has been used to ensure the app works as intended. Currently, there are no outstanding bugs or issues that I am aware of (famous last words).
If any bugs, issues, or generally undesirable behaviour is found, I'd be grateful if you could take the time to report it to me through the built in support system [here](https://links-sw.herokuapp.com/accounts/support/).

## Contents
1. [Automated Testing](#automated-testing)
	- [Unit Tests](#unit-tests)
	- [Coverage](#coverage)

2. [Manual Testing](#manual-testing)
	- [Browser Compatibility](#browser-compatibility)
	- [Features Testing](#features-testing)

3. [Code Validation](#code-validation)
	- [Python](#python)
	- [JavaScript](#javascript)
	-  [HTML](#html)
	- [CSS](#css)


## Automated Testing

### Unit Tests
A suite of 80 tests (at last count) are in place to test the app. Approximately half of these were written alongside the project itself, and mainly relate to the individual apps for `accounts`, `support`, `premium`, `intro pages` and so on - basically everything but the main links app itself.
The remaining tests for the `links` and `search` apps were written after the app was complete and will be useful for when the app is expanded at a later date.

To run the tests locally (on Windows) use `python manage.py test`

### Coverage
The [Coverage](https://pypi.org/project/coverage/) library was used throughout testing to help keep track of how much of my code was covered by the tests. As it stands, there is 77% coverage across the project. I would have liked to have added more tests, especially ones focused on the main links app and associated helper functions in the utils folder, but time became a factor. However, even without the additional tests, I feel that along with the manual testing I've completed, the app is in good health and works as expected.

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
EdgeHTML hasn't been updated since October 2018, so I can't see this ever changing for this version of the Edge browser. However, after updating Edge to use the newer Chromium based version, these issues are no longer present so it's an issue that will fix itself over time as users automatically switch to the new Edge through automatic Windows updates.

:three: I never intended the app to work with IE11, it was more a case of if it works then great, but it most likely won't. And it doesn't. In the most part, the lack of compatibility comes down to IE11 not supporting ES6 and because a lot of the apps functionality is dependent on JavaScript, the console just spits out errors and halts the script.
I could rewrite all the JS to be compatible with IE11, but it wouldn't be time well spent. If there was more time, I'd spend it adding more features, not trying to breathe life into a dead browser.

:four: Numerous issues displaying the site properly with the Safari mobile browser. All since fixed, and mostly due to Safari not registering touch events unless the element is a `<div>` or `<a>`. Some issues fixed by changing the element, but most by adding `cursor: pointer` css to the element to allow Safari to register a touch event.

**[ Add Section that reviews and checks warnings on dev tools console ]**

### Features Testing
For every feature listed in the [features](README.md#current-features) section of the main [README.md](README.md) file, it's functionality has been tested to ensure it works as intended.
Tests were initially completed on a PC running Windows 10, and then repeated on an Android mobile with a Pixel 2 XL handset.

#### Top Navigation Bar ( Logged Out )
- Links all go to correct page.
- On scroll down, logo is hidden and just links displayed.
- When scrolled back to the top, logo is shown again.
- On mobile views, `Login` & `Register` are moved to a separate mobile menu with these options contained within a drop-down. Both of these links go to the correct page.
- When scrolling down, add a thin border to the bottom of the navbar to separate the nav elements from the rest of the page. Remove when scrolled back to the top.

#### Home / About Page
##### Intro Panel & Icon Grid
- 4x4 icon grid should display random icons each time. Multiple page refreshes confirms this.
- `Create Account` button and `or log in here` link both take the user to the correct page.
##### Features Section 
- On non-touch displays, hovering over the images causes the gif to play, and un-hovering causes it to stop and reset to the beginning.
-  On touch devices the behaviour is the same except the gifs activate / deactivate ob click as opposed to hover.
The `Compare Features` button takes the user to the feature comparison table on the `Pricing` page.
##### Chrome Extension Panel
- The `Install Extension` button opens a new tab the Chrome Web Store page for the app extension.
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
- The `Contact Form` button scrolls down past the FAQ section and on to the Contact Form.
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
- If details are missing or entered incorrectly, no account is created and the incorrect field(s) tell the user what went wrong.
- Tool-tips appear when hovered over, or clicked on for touch devices.
- `Already have an account? Log in here` correctly links to the login page.
##### Password Reset
- If something other than an email address is submitted, the user will be informed of this.
- Confirmed email is received when a registered email address is entered.
- Confirmed email link within the sent email works and directs the user to a password reset screen.
- Password reset form checks the passwords match meet the password requirements and shows an error if not.
- Tool-tip works as expected.
- Confirmed password change works and can then log in with new password.
- 
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

#### Top Navigation Bar ( Logged In)
##### Navigation
- `Logout` button successfully logs out the current user.
- The `Settings` icon directs users the settings pages, specifically the `Profile` page.
- The `Bookmark` icon takes the user to the main app. The app correctly loads the last `Page` the user was on, before they navigated away.
- The `Search` bar opens the search page with results for the search term that was submitted. If no search term is entered, the app correctly returns all the users bookmarks, regardless of the `Page` they are part of.
- The `Search` icon, when clicked, opens an input field for the user to enter a search term (smaller screens only)
- The `Add Bookmark` icon correctly navigates the user to the correct page.
##### Responsiveness 
- On larger widths, the only icons on display should be the `Bookmark` main app icon, `Settings` cog icon & `Logout` icon. - As the screen width is reduced, the sidebar will eventually disappear. The sidebar contains the main `Add Bookmark` button so to compensate for this not being present, a `+` icon is added to the top navigation so the user can still easily add bookmarks. Confirmed this works as intended.
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
- Payment form is present and works correctly.
- Tested with Stripes VISA test card numbers to successfully upgrade a user to Premium.
- Tested with fake / incorrect numbers to produce expected errors.
- The banner advert is displayed.
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
- Confirmed if either field is missing, no ticket is created and user is informed of errors that require correcting.
##### Premium Users
- `Priority Telephone Support` number is displayed if logged in user has `Premium` status.
##### Standard Users
- A button linking to the Premium sign up page is provided in place of the telephone support number when this page is viewed by a standard member.

#### About Page
- Displays the current app version number correctly.
- Correctly displays a different message re: Premium depending on Premium status.
- Link to `Support` page goes to the correct page.

#### Side Navigation Bar ( Main App )
##### Link to Main App
##### Add Bookmark Button
##### Sort Page Order Button
##### Add New Page Button
##### Links to Different Pages
##### Page Options Button
###### Arrange Collections Button
###### Change Column Display Button
###### Rename Page
###### Delete Page
##### Premium Status

#### Search

#### Main App View
##### Collection Options Button
###### Sort By
###### Display As
###### Rename Collection
###### Delete Collection

##### Manual Sort Button
##### Bookmark Options Button
##### Bookmark Description Tool Tip
##### Add New Collection

#### Edit Bookmark
#### Move Bookmark
#### Delete Bookmark
#### Add Bookmark
#### Import Url
#### Banner Adverts



## Code Validation

### Python
All Python code is fully PEP 8 compliant, and has been verified at [pep8online.com](http://pep8online.com/).

### Javascript
All Javascript has been verified with the online tool [jshint.com](https://jshint.com/).

### HTML
HTML has been run through [validator.w3.org](https://validator.w3.org/). Outside of errors generated by the Django templating language, all other HTML is valid.

### CSS
The CSS is auto-prefixed and compiled from multiple .scss files using the VS Code [Live Sass Compiler](https://marketplace.visualstudio.com/items?itemName=ritwickdey.live-sass) extension.
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
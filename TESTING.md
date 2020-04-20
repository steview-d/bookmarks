
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

**Add version numbers for browsers**

Device & CSS Width :arrow_down_small: | Chrome v81 | Firefox v75 | Safari v0 | Opera v67 | Edge v81 :one: | IE11 v11
---|---|---|---|---|---|---
Windows 10 PC @ 1400|:heavy_check_mark:|:heavy_check_mark:|.|:heavy_check_mark:|:heavy_check_mark:|:x::two:
Windows 10 PC @ 1920|:heavy_check_mark:|:heavy_check_mark:|.|:heavy_check_mark:|:heavy_check_mark:|:x::two:
Windows 10 PC @ 2560|:heavy_check_mark:|:heavy_check_mark:|.|:heavy_check_mark:|:heavy_check_mark:|:x::two:
Windows 10 PC @ 3440|.|.|.|.|.|:x::two:
Apple Mac Book @ x|:heavy_minus_sign:|:heavy_minus_sign:|.|:heavy_minus_sign:|:heavy_minus_sign:|:heavy_minus_sign:
Pixel 2XL @ 411|:heavy_check_mark:|:heavy_minus_sign:|:heavy_minus_sign:|:heavy_minus_sign:|:heavy_minus_sign:|:heavy_minus_sign:
iPhone (IOS?) @ x|:heavy_minus_sign:|:heavy_minus_sign:|.|:heavy_minus_sign:|:heavy_minus_sign:|:heavy_minus_sign:
iPad Mini @ x|:heavy_minus_sign:|:heavy_minus_sign:|.|:heavy_minus_sign:|:heavy_minus_sign:|:heavy_minus_sign:
Samsung Tablet @ x|.|:heavy_minus_sign:|:heavy_minus_sign:|:heavy_minus_sign:|:heavy_minus_sign:|:heavy_minus_sign:

:heavy_check_mark: - Tested, No Issues Found
:x: - Tested & Issues Found, See Notes
:heavy_minus_sign: - Not Tested

:one: Originally tested with Edge v44 (EdgeHTML). The site worked and was fully functional, but there were issues with how flex elements were displayed. They would appear to expand to normal size on page load and whilst this effect was only slight, it was noticeable. More noticeable was how the side bar would pop / slide in to view on each page load. After investigating, it seems these issues come from how EdgeHTML handles flex in general.
EdgeHTML hasn't been updated since October 2018, so I can't see this ever changing for this version of the Edge browser. However, after updating Edge to use the newer Chromium based version, these issues are no longer present so it's an issue that will fix itself over time as users automatically switch to the new Edge through automatic Windows updates.

:two: I never intended the app to work with IE11, it was more a case of if it works then great, but it most likely won't. And it doesn't. In the most part, the lack of compatibility comes down to IE11 not supporting ES6 and because a lot of the apps functionality is dependent on JavaScript, the console just spits out errors and halts the script.
I could rewrite all the JS to be compatible with IE11, but it wouldn't be time well spent. If there was more time, I'd spend it adding more features, not trying to breathe life into a dead browser.

**[ Add Section that reviews and checks warnings on dev tools console ]**



### Features Testing
For every feature listed in the features section of the main readme file, it's functionality has been tested to ensure it works as intended.
Tests were initially completed on a PC running Windows 10, and then repeated on an Android mobile with a Pixel 2 XL handset.

#### Top Navigation Bar ( Logged Out )

#### Home / About Page
##### Intro Panel & Icon Grid
##### Features Section
##### Chrome Extension Panel
##### User Reviews
##### User Authentication Options

#### Pricing Page
##### User Authentication Options

#### FAQ Page
##### FAQ Section
##### Contact Form
##### User Authentication Options


#### User Authentication
##### Log In System
##### New User Registration
##### Password Reset

#### Admin Back-End
##### Users
##### Bookmarks
##### Collections & Pages
##### Contacts
##### Premium Purchases
##### Support Tickets

#### Top Navigation Bar ( Logged In)

#### Side Navigation Bar ( Settings )
##### Link to Main App
##### Add Bookmark Button
##### Links To Settings Pages



#### Messages System
#### User Profile Page
#### Premium Page
#### Support Page
#### About Page

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
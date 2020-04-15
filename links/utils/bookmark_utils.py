from bs4 import BeautifulSoup
from urllib.parse import urlparse

from links.conf import settings
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


from links.models import Collection, Bookmark

import base64
import favicon
import os
import random
import re
import requests as req
import string


def add_bookmark_object(request, bookmark_form):
    """
    Add a new Bookmark object

    Args:
        request (obj): The request object
        bookmark_form (obj): The completed form
    """

    form = bookmark_form.save(commit=False)
    form.user = request.user

    dest_collection = Collection.objects.get(
        id=request.POST.get('dest_collection'))

    form.collection = dest_collection

    # get new position value for bookmark
    dest_position = Bookmark.objects.filter(
        user=request.user, collection=dest_collection
    ).count() + 1

    form.position = dest_position

    if not request.FILES and request.POST.get('scraped_img'):
        # save image from scraped data
        form.icon = create_img_from_base64_str(request)

    form.save()

    return


def delete_bookmark(request):
    """
    Find and delete the requested bookmark using its pk from
    request.POST and then reset the 'position' values for all remaining
    bookmarks within the collection to run in order again.
    """

    # get bookmark that is to be deleted
    bookmark_to_delete = get_object_or_404(
        Bookmark, pk=request.POST.get('bookmark')
    )

    # get collection that bookmark is a part of
    bookmark_collection = get_object_or_404(
        Collection, pk=bookmark_to_delete.collection.id
    )

    bookmark_to_delete.delete()

    # get remaining bookmarks, in position order
    all_bookmarks_in_collection = Bookmark.objects.filter(
        collection=bookmark_collection
    ).order_by('position')

    reorder_bookmarks(all_bookmarks_in_collection)

    return


def reorder_bookmarks(bookmark_qs):
    """
    Iterate through a queryset of bookmarks and apply the .position
    value, in order.

    Args:
        bookmark_qs (qs): A queryset of bookmarks
    """

    for count, bm in enumerate((bookmark_qs), 1):
        bm.position = count
        bm.save()

    return


def scrape_url(request, url):
    """
    Scrape metadata from a URL using BeautifulSoup4

    Args:
        request (obj): The request object
        url (str): The url to scrape

    Returns:
        data (dict): The scraped data
    """

    # default return data
    data = {'message': 'The URL is empty',
            'title': 'Cannot Scrape this URL',
            'description': '',
            'scraped_image': '',
            'image_ext': ''
            }

    if not url:
        return JsonResponse(data)

    try:
        r = req.get(
            url,
            headers=settings.LINKS_HEADERS,
            allow_redirects=True,
            timeout=2
            )
        r.raise_for_status()
    except (req.exceptions.RequestException, UnicodeError):
        # UnicodeError to catch errors caused by this bug:
        # https://bugs.python.org/issue32958
        data['message'] = 'Could not load this URL'

    else:
        soup = BeautifulSoup(r.text, 'html.parser')

        # get the page title
        try:
            scraped_title = soup.title.get_text() if soup.title.get_text() \
                else "Could not retrieve a title"
        except AttributeError:
            scraped_title = "Could not retrieve a title"

        # get the page description from metadata content
        metas = soup.find_all('meta')
        for m in metas:
            if 'name' in m.attrs and m.attrs['name'] == 'description':
                try:
                    scraped_description = m.attrs['content']
                except KeyError:
                    scraped_description = "Sorry, no description found."

        # provide default response for when no metadata available
        try:
            scraped_description
        except UnboundLocalError:
            scraped_description = "Sorry, no metadata available for this URL"

        # handle empty description metadata
        if scraped_description == '':
            scraped_description = "Sorry, no metadata available for this URL"

        # get url for site icon / favicon
        icon_url = get_site_icon(url)

        # convert image at url location to a base64 enc string
        if icon_url:
            # sometimes, favicon will find icons that lead to 404's so this
            # checks for a 200 response from the icon url itself and confirms
            # that item being returned is am image
            try:
                q = req.get(
                    icon_url,
                    headers=settings.LINKS_HEADERS,
                    allow_redirects=True,
                    timeout=2
                    )
                q.raise_for_status()
            except req.exceptions.RequestException:
                # if url won't resolve, using pass as 'scraped_image' and
                # 'image_ext' already set to ''
                pass
            else:
                try:
                    q.headers['Content-Type']
                except KeyError:
                    # if 'content-type' header does not exist, it can't be
                    # checked. Create a fake value to avoid a KeyError during
                    # next check
                    q.headers['Content-Type'] = 'image'
                # at this point, icon_url is url with format type at end as ext
                if q.status_code == 200 and \
                        'image' in q.headers['Content-Type']:
                    data['scraped_image'] = base64.b64encode(
                        q.content).decode('utf-8')

                    # get image format from header
                    data['image_ext'] = 'ico' if 'ico' in q.headers[
                        'Content-Type'] else 'png'

        data['message'] = 'Success'
        data['title'] = scraped_title
        data['description'] = scraped_description

    return data


def get_site_icon(url):
    """
    Use the Favicon library to get an icon from the page that can be
    saved to the Bookmark object.

    Args:
        url (str): The web page to scrape for a suitable icon

    Returns:
        icon_url (str): The url that contains the chosen image, or
                        nothing if no suitable icon found
    """

    icons = ''
    chosen_icon = ''
    icon_url = ''

    # lists of file names and file extensions to check for when scraping.
    # filenames are checked using regex so list items can be either a basic
    # string or a regex statement for more advanced searching.
    file_names = ['apple-touch', 'apple-icon', '180x180', '152x152',
                  '144x144', '120x120', '^(?!.*favicon).*icon.*$', 'favicon',
                  'logo', ]
    ext_order = ['png', 'ico', 'jpg']

    try:
        icons = favicon.get(url,
                            headers=settings.LINKS_HEADERS,
                            timeout=2,
                            allow_redirects=True)
    except req.exceptions.RequestException:
        icons = ''

    if not icons:
        url_comp = urlparse(url)
        url_location = str(url_comp.scheme + '://' + url_comp.netloc)
        try:
            icons = favicon.get(url_location,
                                headers=settings.LINKS_HEADERS,
                                timeout=2,
                                allow_redirects=True)
        except req.exceptions.RequestException:
            icons = ''

    if icons:
        # check for specific file names and formats, in order, then break
        if not chosen_icon:
            for file_name in file_names:
                for ext in ext_order:
                    for i in icons:
                        if re.search(file_name, i.url) and i.format == ext:
                            chosen_icon = i
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break

        # last resort, any image it can find! first ico, png, then jpg
        if not chosen_icon:
            ext_order = ['ico', 'png', 'jpg']
            for ext in ext_order:
                for i in icons:
                    if i.format == ext:
                        chosen_icon = i
                        break
                else:
                    continue
                break

        # Return url of matched icon,
        # or nothing if no suitable icon found
        icon_url = chosen_icon.url if chosen_icon else ''

    return icon_url


def create_img_from_base64_str(request):
    """
    Convert a base64 string to a ContentFile,
    ready to be saved to the db as an image.

    Args:
        request (obj): The request object. This contains 'scraped_img'
                       which is a string representation of the
                       scraped image encoded in base64.

    Returns:
        ContentFile (obj): This is then saved to the icon field of the
                           Bookmark object
    """

    scraped_img = request.POST.get('scraped_img')

    format, base64_str = scraped_img.split(';base64,')
    ext = format.split('/')[-1]
    file_name = ''.join(
        random.choices(string.ascii_letters + string.digits, k=8))
    img_file = ContentFile(
        base64.b64decode(base64_str),
        name='scr_' + file_name + '.' + ext)

    return img_file


def handle_icon_errors(request, bookmark_form):
    """
    Used with forms which add / edit / import Bookmark objects

    Function will generate / preserve an icon submitted by the user
    so in the event of a form error, the icon can be passed back to
    the form to avoid the user having to select the icon again.

    Args:
        request (obj): The request object
        bookmark_form (obj): The completed form

    Returns:
        tuple: values for use_default_icon & saved_icon_data

    """

    saved_icon_data = ""
    use_default_icon = ""

    # if the error is not icon related
    if 'icon' not in bookmark_form.errors:
        if request.POST.get('use-default'):
            use_default_icon = True

        # if a file has been uploaded, save it
        elif request.FILES:
            # create base64 image string to send back and display
            f_name = str(request.FILES['icon']).lower()
            f_ext = os.path.splitext(f_name)[1]

            data = request.FILES['icon'].read()
            img = base64.b64encode(data).decode('utf-8')

            saved_icon_data = f"data:image/{f_ext[1:]};base64,{img}"

        # if a file has been scraped, save it
        elif request.POST.get('scraped_img'):
            saved_icon_data = request.POST.get('scraped_img')

        return use_default_icon, saved_icon_data

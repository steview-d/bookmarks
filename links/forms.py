from django import forms

from .models import Page, Collection, Bookmark, MoveBookmark

import re


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('current_user')
        super(PageForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get('name')

        # check the page name is unique to that user
        if Page.objects.filter(user=self.user).filter(name=name):
            raise forms.ValidationError(
                u'You already have a page with this name')

        # check the page name against a list of reserved names
        reserved_name_list = []  # Add names as / if required
        if name in reserved_name_list:
            raise forms.ValidationError(
                u'Sorry, that name is reserved. Please choose a different one')

        # check page name contains only allowed chars
        allowed_chars = re.compile(r'[^-: a-zA-Z0-9.]')
        char_check = allowed_chars.search(name)
        if char_check:
            raise forms.ValidationError(
                u"Name can only contain letters, numbers, \
                            spaces, hyphens '-', and colons ':'")

        return name


class AddNewPageForm(PageForm):

    NUM_COLUMN_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    num_of_columns = forms.ChoiceField(
        initial=4, label="Columns", choices=NUM_COLUMN_CHOICES
    )

    class Meta:
        model = Page
        fields = ['name', 'num_of_columns']


class EditPageForm(PageForm):
    class Meta:
        model = Page
        fields = ['name']


class AddBookmarkForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea()
    )

    class Meta:
        model = Bookmark
        fields = ['url', 'title', 'description', 'collection']

    def __init__(self, user, page, *args, **kwargs):
        super(AddBookmarkForm, self).__init__(*args, **kwargs)
        self.initial['collection'] = {'position'}
        self.fields['collection'].queryset = Collection.objects.filter(
            user=user, page=page).order_by('position')


class EditBookmarkForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea()
    )

    class Meta:
        model = Bookmark
        fields = ['url', 'title', 'description']


class MoveBookmarkForm(forms.ModelForm):

    class Meta:
        model = MoveBookmark
        fields = ['dest_page', 'dest_collection']

    def __init__(self, user, page, *args, **kwargs):
        super(MoveBookmarkForm, self).__init__(*args, **kwargs)
        self.fields['dest_page'].queryset = Page.objects.filter(
            user=user).order_by('position')
        self.fields['dest_collection'].queryset = Collection.objects.filter(
            user=user, page=page).order_by('position')
        self.fields['dest_collection'].error_messages = {
            'required': "Bookmarks cannot be in a page with no collections, \
                please choose a page with at least one collecion"
            }


class ImportUrlForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea()
    )

    class Meta:
        model = Bookmark
        fields = ['url', 'title', 'description']

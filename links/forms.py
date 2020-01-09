from django import forms

from .models import Page, Collection, Bookmark, MoveBookmark


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('current_user')
        super(PageForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        """check the page name is unique to that user"""
        name = self.cleaned_data.get('name').lower()

        if Page.objects.filter(user=self.user).filter(name=name):
            raise forms.ValidationError(
                u'You already have a page with this name')
        return name


class AddNewPageForm(PageForm):
    num_of_columns = forms.IntegerField(
        initial=4, label="Columns"
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
            'required': "Collection cannot be empty, \
                please choose a page with at least one collecion"
            }


class ImportUrlForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea()
    )

    class Meta:
        model = Bookmark
        fields = ['url', 'title', 'description']

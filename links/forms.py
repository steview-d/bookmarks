from django import forms

from .models import Page, Collection, Bookmark


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

    url = forms.URLField()

    class Meta:
        model = Bookmark
        fields = ['url', 'title', 'description', 'collection']

    def __init__(self, user, page, *args, **kwargs):
        super(AddBookmarkForm, self).__init__(*args, **kwargs)
        self.fields['collection'].queryset = Collection.objects.filter(
            user=user, page=page)

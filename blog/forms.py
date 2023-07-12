from django import forms


class EmailPostForm(forms.Form):
    """
    форма, позволяющая делиться постами
    """
    name = forms.CharField(max_length=25)  # имя человека, отправляющего пост
    email = forms.EmailField()  # адрес электронной почты человека
    to = forms.EmailField()  # адрес электронной почты получателя
    #  для комментариев, которые будут вставляться в электронное письмо
    comments = forms.CharField(required=False, widget=forms.Textarea)

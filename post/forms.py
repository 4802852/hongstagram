from django import forms
from .models import Post


class NewPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewPostForm, self).__init__(*args, **kwargs)
        self.fields["text"].label = "내용"
        self.fields["text"].widget.attrs.update(
            {
                "placeholder": "내용을 입력해주세요.",
                "class": "form-control",
                "autofocus": True,
            }
        )

    class Meta:
        model = Post
        fields = [
            "text",
        ]

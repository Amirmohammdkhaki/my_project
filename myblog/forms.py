from django import forms
from .models import Post_blog, Comment, EmojiReaction

class NewPostForm(forms.ModelForm):
    class Meta:  
        model = Post_blog
        fields = ['title', 'text', 'image', 'status']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'عنوان پست را وارد کنید...',
                'required': True
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 8,
                'placeholder': 'متن پست را اینجا بنویسید...',
                'required': True
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        
        labels = {
            'title': 'عنوان پست',
            'text': 'متن پست',
            'image': 'تصویر شاخص',
            'status': 'وضعیت انتشار'
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("عنوان پست باید حداقل ۵ کاراکتر باشد")
        return title

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text) < 10:
            raise forms.ValidationError("متن پست باید حداقل ۱۰ کاراکتر باشد")
        return text


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'نظر خود را اینجا بنویسید...',
                'rows': 3,
                'style': 'resize: none;'
            }),
        }
        labels = {
            'text': 'نظر شما'
        }

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text.strip()) < 3:
            raise forms.ValidationError("نظر باید حداقل ۳ کاراکتر باشد")
        if len(text) > 1000:
            raise forms.ValidationError("نظر نمی‌تواند بیشتر از ۱۰۰۰ کاراکتر باشد")
        return text


class EmojiReactionForm(forms.ModelForm):
    class Meta:
        model = EmojiReaction
        fields = ['emoji_type']
        widgets = {
            'emoji_type': forms.HiddenInput()  # برای استفاده با AJAX
        }


class PostSearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'جستجو در پست‌ها...',
            'aria-label': 'Search'
        })
    )


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام شما'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ایمیل شما'
        })
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'موضوع پیام'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'متن پیام شما...'
        })
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name.strip()) < 2:
            raise forms.ValidationError("نام باید حداقل ۲ کاراکتر باشد")
        return name

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message.strip()) < 10:
            raise forms.ValidationError("پیام باید حداقل ۱۰ کاراکتر باشد")
        return message
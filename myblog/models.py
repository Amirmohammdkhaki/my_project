from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post_blog(models.Model):
    STATUS_CHOICES = (
        ('pub', 'published'),
        ('drf', 'draft'),
    )

    title = models.CharField(max_length=250)
    text = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True, verbose_name='تصویر پست')
    datetime_create = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=4)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    
    # فیلدهای جدید برای لایک عمومی
    likes_count = models.PositiveIntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'pk': self.pk})

    def toggle_like(self, user):
        """تغییر وضعیت لایک توسط کاربر"""
        if user in self.liked_by.all():
            self.liked_by.remove(user)
            self.likes_count -= 1
            is_liked = False
        else:
            self.liked_by.add(user)
            self.likes_count += 1
            is_liked = True
        self.save()
        return is_liked, self.likes_count

    def is_liked_by_user(self, user):
        """بررسی آیا کاربر این پست را لایک کرده است"""
        if user.is_authenticated:
            return self.liked_by.filter(id=user.id).exists()
        return False

    def get_active_comments(self):
        """دریافت نظرات فعال مرتبط با پست"""
        return self.comments.filter(is_active=True).order_by('-datetime_create')

    def get_emojis_summary(self):
        """دریافت خلاصه ایموجی‌های پست"""
        emojis = {}
        for reaction in self.emoji_reactions.all():
            if reaction.emoji_type in emojis:
                emojis[reaction.emoji_type] += 1
            else:
                emojis[reaction.emoji_type] = 1
        return emojis

    def get_user_emoji(self, user):
        """دریافت ایموجی انتخاب شده توسط کاربر"""
        if user.is_authenticated:
            reaction = self.emoji_reactions.filter(user=user).first()
            return reaction.emoji_type if reaction else None
        return None


class Comment(models.Model):
    """مدل برای نظرات پست‌ها"""
    post = models.ForeignKey(Post_blog, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده نظر')
    text = models.TextField(verbose_name='متن نظر')
    datetime_create = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    datetime_modified = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')
    
    class Meta:
        ordering = ['datetime_create']
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'

    def __str__(self):
        return f'نظر {self.author} روی {self.post.title}'


class EmojiReaction(models.Model):
    """مدل برای واکنش‌های ایموجی کاربران"""
    EMOJI_CHOICES = [
        ('like', '👍'),
        ('love', '❤️'),
        ('laugh', '😂'),
        ('wow', '😮'),
        ('sad', '😢'),
        ('angry', '😠'),
    ]
    
    post = models.ForeignKey(Post_blog, on_delete=models.CASCADE, related_name='emoji_reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    emoji_type = models.CharField(max_length=10, choices=EMOJI_CHOICES, verbose_name='نوع ایموجی')
    datetime_create = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    
    class Meta:
        unique_together = ['post', 'user']  # هر کاربر فقط یک واکنش در هر پست
        verbose_name = 'واکنش ایموجی'
        verbose_name_plural = 'واکنش‌های ایموجی'
    
    def __str__(self):
        return f'{self.user.username} - {self.get_emoji_type_display()} روی {self.post.title}'
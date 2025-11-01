from django.contrib import admin
from .models import Post_blog, Comment, EmojiReaction

class Post_admin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'datetime_modified', 'likes_count', 'get_comments_count')
    list_filter = ('status', 'datetime_create', 'author')
    search_fields = ('title', 'text', 'author__username')
    date_hierarchy = 'datetime_create'
    readonly_fields = ('datetime_create', 'datetime_modified', 'likes_count')
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'text', 'author', 'status')
        }),
        ('تصویر', {
            'fields': ('image',),
            'classes': ('collapse',)
        }),
        ('تاریخ‌ها', {
            'fields': ('datetime_create', 'datetime_modified'),
            'classes': ('collapse',)
        }),
        ('لایک‌ها', {
            'fields': ('likes_count', 'liked_by'),
            'classes': ('collapse',)
        }),
    )
    filter_horizontal = ('liked_by',)
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    get_comments_count.short_description = 'تعداد نظرات'

class Comment_admin(admin.ModelAdmin):
    list_display = ('author', 'post', 'short_text', 'datetime_create', 'is_active')
    list_filter = ('is_active', 'datetime_create', 'post')
    search_fields = ('text', 'author__username', 'post__title')
    list_editable = ('is_active',)
    actions = ['activate_comments', 'deactivate_comments']
    
    def short_text(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    short_text.short_description = 'متن نظر'
    
    def activate_comments(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, 'نظرات انتخاب شده فعال شدند.')
    activate_comments.short_description = 'فعال کردن نظرات انتخاب شده'
    
    def deactivate_comments(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, 'نظرات انتخاب شده غیرفعال شدند.')
    deactivate_comments.short_description = 'غیرفعال کردن نظرات انتخاب شده'

class EmojiReaction_admin(admin.ModelAdmin):
    list_display = ('user', 'post', 'get_emoji_display', 'datetime_create')
    list_filter = ('emoji_type', 'datetime_create')
    search_fields = ('user__username', 'post__title')
    readonly_fields = ('datetime_create',)
    
    def get_emoji_display(self, obj):
        return obj.get_emoji_type_display()
    get_emoji_display.short_description = 'ایموجی'

# ثبت مدل‌ها در ادمین
admin.site.register(Post_blog, Post_admin)
admin.site.register(Comment, Comment_admin)
admin.site.register(EmojiReaction, EmojiReaction_admin)
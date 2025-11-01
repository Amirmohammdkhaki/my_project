from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Post_blog, Comment, EmojiReaction
from .forms import NewPostForm, CommentForm, EmojiReactionForm, PostSearchForm, ContactForm

# دکوراتور اصلاح شده برای چک کردن اینکه کاربر ادمین است
def admin_required(function):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'برای دسترسی به این صفحه باید وارد شوید!')
            return redirect('login') + '?next=' + request.path
        elif not request.user.is_staff:
            messages.error(request, 'شما دسترسی لازم برای ایجاد پست جدید را ندارید!')
            return redirect('access_denied')
        return function(request, *args, **kwargs)
    return wrapper

class PostListView(ListView):
    model = Post_blog
    template_name = 'myblog/posts_list.html'
    context_object_name = 'post_list'
    paginate_by = 6
    ordering = ['-datetime_modified']

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(text__icontains=search_query) |
                Q(author__username__icontains=search_query)
            )
        
        return queryset.filter(status='pub')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # بررسی لایک شدن هر پست توسط کاربر جاری
        if self.request.user.is_authenticated:
            for post in context['post_list']:
                post.user_has_liked = post.is_liked_by_user(self.request.user)
                post.user_emoji = post.get_user_emoji(self.request.user)
        
        context['search_form'] = PostSearchForm(self.request.GET or None)
        context['search_query'] = self.request.GET.get('q', '')
        return context

def post_detail_view(request, pk):
    post = get_object_or_404(Post_blog, pk=pk)
    
    # دریافت نظرات فعال این پست
    comments = post.get_active_comments()
    
    # بررسی لایک شدن توسط کاربر جاری
    if request.user.is_authenticated:
        post.user_has_liked = post.is_liked_by_user(request.user)
        # دریافت ایموجی کاربر برای این پست
        post.user_emoji = post.get_user_emoji(request.user)
    
    # دریافت خلاصه ایموجی‌های پست
    emojis_summary = post.get_emojis_summary()
    
    # پردازش فرم نظر
    comment_form = CommentForm()
    if request.method == 'POST':
        if 'comment_submit' in request.POST:
            if not request.user.is_authenticated:
                messages.warning(request, 'برای ثبت نظر باید وارد حساب کاربری خود شوید.')
                return redirect('login') + '?next=' + request.path
            
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.author = request.user
                new_comment.save()
                messages.success(request, 'نظر شما با موفقیت ثبت شد!')
                return redirect('blog_detail', pk=post.pk)
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'emojis_summary': emojis_summary,
        'emoji_choices': EmojiReaction.EMOJI_CHOICES,
    }
    
    return render(request, 'myblog/post_detail.html', context)

# ==========================================
# ویوی اصلاح شده برای مدیریت خطا
# ==========================================
@require_POST
@login_required
def toggle_like(request, pk):
    """ویو برای تغییر وضعیت لایک با مدیریت خطا"""
    try:
        post = get_object_or_404(Post_blog, pk=pk)
        
        # این خط ممکن است باعث خطا شود
        is_liked, likes_count = post.toggle_like(request.user)
        
        return JsonResponse({
            'success': True,
            'likes_count': likes_count,
            'is_liked': is_liked,
            'post_id': pk
        })
    except Exception as e:
        # اگر هر خطایی رخ داد، آن را در ترمینال چاپ کن
        # این مهم‌ترین قسمت برای دیباگ کردن است!
        print(f"Error in toggle_like view: {e}") 
        
        # یک پاسخ خطا به جاوا اسکریپت بفرست
        return JsonResponse({
            'success': False,
            'error': 'An internal server error occurred.'
        }, status=500)

@require_POST
@login_required
def add_emoji_reaction(request, pk):
    """ویو برای اضافه کردن واکنش ایموجی"""
    post = get_object_or_404(Post_blog, pk=pk)
    emoji_type = request.POST.get('emoji_type')
    
    if emoji_type not in dict(EmojiReaction.EMOJI_CHOICES):
        return JsonResponse({'success': False, 'error': 'ایموجی نامعتبر'})
    
    # حذف واکنش قبلی کاربر اگر وجود داشته باشد
    EmojiReaction.objects.filter(post=post, user=request.user).delete()
    
    # اضافه کردن واکنش جدید
    reaction = EmojiReaction.objects.create(
        post=post,
        user=request.user,
        emoji_type=emoji_type
    )
    
    # دریافت خلاصه جدید ایموجی‌ها
    emojis_summary = post.get_emojis_summary()
    
    return JsonResponse({
        'success': True,
        'emojis_summary': emojis_summary,
        'user_emoji': emoji_type
    })

@require_POST
@login_required
def remove_emoji_reaction(request, pk):
    """ویو برای حذف واکنش ایموجی"""
    post = get_object_or_404(Post_blog, pk=pk)
    
    # حذف واکنش کاربر
    deleted_count = EmojiReaction.objects.filter(post=post, user=request.user).delete()[0]
    
    if deleted_count > 0:
        emojis_summary = post.get_emojis_summary()
        return JsonResponse({
            'success': True,
            'emojis_summary': emojis_summary,
            'user_emoji': None
        })
    else:
        return JsonResponse({'success': False, 'error': 'واکنشی برای حذف یافت نشد'})

@login_required
@admin_required
def post_create_view(request):
    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            messages.success(request, 'پست جدید با موفقیت ایجاد شد!')
            return redirect('post_list')
    else:
        form = NewPostForm()
    
    return render(request, 'myblog/add_post.html', {'form': form})

@login_required
def post_update_view(request, pk):
    post = get_object_or_404(Post_blog, pk=pk)
    
    # بررسی اینکه کاربر ادمین است یا نویسنده پست
    if not request.user.is_staff and post.author != request.user:
        messages.error(request, 'شما فقط می‌توانید پست‌های خودتان را ویرایش کنید!')
        return redirect('post_list')
    
    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            updated_post = form.save(commit=False)
            # اگر کاربر ادمین نیست، نویسنده را تغییر نده
            if not request.user.is_staff:
                updated_post.author = request.user
            updated_post.save()
            messages.success(request, 'پست با موفقیت ویرایش شد!')
            return redirect('post_list')
    else:
        form = NewPostForm(instance=post)
    
    return render(request, 'myblog/add_post.html', {'form': form, 'post': post})

@login_required
def post_delete_view(request, pk):
    post = get_object_or_404(Post_blog, pk=pk)
    
    # بررسی اینکه کاربر ادمین است یا نویسنده پست
    if not request.user.is_staff and post.author != request.user:
        messages.error(request, 'شما فقط می‌توانید پست‌های خودتان را حذف کنید!')
        return redirect('post_list')
    
    if request.method == "POST":
        post_title = post.title
        post.delete()
        messages.success(request, f'پست "{post_title}" با موفقیت حذف شد!')
        return redirect('post_list')
    
    return render(request, 'myblog/post_confirm_delete.html', {'post': post})

def access_denied(request):
    return render(request, 'myblog/access_denied.html', status=403)

def about_me_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # در اینجا می‌توانید ایمیل ارسال کنید یا داده‌ها را ذخیره کنید
            messages.success(request, 'پیام شما با موفقیت ارسال شد!')
            return redirect('about_me')
    else:
        form = ContactForm()
    
    context = {
        'title': 'درباره من',
        'description': 'این صفحه اطلاعاتی درباره من نمایش می‌دهد.',
        'form': form
    }
    return render(request, 'myblog/about_me.html', context)

def projects_view(request):
    context = {
        'title': 'پروژه‌ها',
        'description': 'این صفحه پروژه‌های من را نمایش می‌دهد.'
    }
    return render(request, 'myblog/projects.html', context)

def computer_vision_code_view(request):
    """صفحه نمایش نمونه کدهای بینایی کامپیوتر"""
    context = {
        'title': 'نمونه کدهای بینایی کامپیوتر',
        'description': 'مجموعه‌ای از کدهای OpenCV و پرداش تصویر'
    }
    return render(request, 'myblog/computer_vision_codes.html', context)

@login_required
def delete_comment(request, pk):
    """حذف نظر توسط نویسنده نظر یا ادمین"""
    comment = get_object_or_404(Comment, pk=pk)
    
    # بررسی دسترسی
    if not request.user.is_staff and comment.author != request.user:
        messages.error(request, 'شما فقط می‌توانید نظرات خودتان را حذف کنید!')
        return redirect('blog_detail', pk=comment.post.pk)
    
    post_pk = comment.post.pk
    comment.delete()
    messages.success(request, 'نظر با موفقیت حذف شد!')
    return redirect('blog_detail', pk=post_pk)

def computer_python_view(request):
    """ python  """
    
    return render(request, 'myblog/computer_python_view.html')


def coputer_djngo(request):
    return render (request,'myblog/coputer_djngo_view.html')
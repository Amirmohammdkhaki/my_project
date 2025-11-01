from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post_blog

class PostBlogTests(TestCase):

    def setUp(self):
        # ایجاد کاربر تستی
        self.user = User.objects.create_user(username='testuser', password='12345')

        # ایجاد یک پست تستی
        self.post = Post_blog.objects.create(
            title='پست تستی',
            text='این یک پست تستی است.',
            status='pub',
            author=self.user
        )

    def test_post_list_view_status_code(self):
        """بررسی اینکه صفحه‌ی لیست پست‌ها باز می‌شود"""
        url = reverse('post_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_list_view_template_used(self):
        """بررسی اینکه از قالب درست استفاده می‌شود"""
        url = reverse('post_list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'myblog/posts_list.html')
        self.assertContains(response, self.post.title)

    def test_post_detail_view_status_code(self):
        """بررسی باز شدن صفحه‌ی جزئیات پست"""
        url = reverse('blog_detail', args=[self.post.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_detail_view_not_found(self):
        """بررسی واکنش در صورت درخواست پستی که وجود ندارد"""
        url = reverse('blog_detail', args=[999])  # شناسه‌ای که وجود ندارد
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_post_detail_template_and_content(self):
        """بررسی قالب و محتوای نمایش داده شده در صفحه جزئیات"""
        url = reverse('blog_detail', args=[self.post.pk])
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'myblog/post_detail.html')
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.text)

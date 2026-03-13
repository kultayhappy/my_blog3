from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Comment


class PostModelTest(TestCase):
    """Unit-тесты для модели Post."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Тестовый пост',
            content='Содержимое теста',
            author=self.user,
            published=True
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Тестовый пост')
        self.assertTrue(self.post.published)

    def test_post_str_method(self):
        self.assertEqual(str(self.post), 'Тестовый пост')

    def test_get_absolute_url(self):
        expected_url = reverse('blog:post_detail', kwargs={'pk': self.post.pk})
        self.assertEqual(self.post.get_absolute_url(), expected_url)


class CommentModelTest(TestCase):
    """Unit-тесты для Comment."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='commentuser',
            password='pass123'
        )
        self.post = Post.objects.create(
            title='Пост для тестов',
            content='Содержимое',
            author=self.user,
            published=True
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            text='Тестовый комментарий'
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.text, 'Тестовый комментарий')

    def test_related_comments(self):
        Comment.objects.create(
            post=self.post,
            author=self.user,
            text='Второй комментарий'
        )
        self.assertEqual(self.post.comments.count(), 2)

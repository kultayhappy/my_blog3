from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm


def post_list(request):
    """Список всех опубликованных постов."""
    posts = Post.objects.filter(
        published=True
    ).select_related('author')

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'paginator': paginator,
    }

    return render(request, 'blog/post_list.html', context)


def post_detail(request, pk):
    """Детальный просмотр поста."""
    post = get_object_or_404(Post, pk=pk, published=True)
    comments = post.comments.select_related('author').all()

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
            return redirect('post_detail', pk=post.id)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': form,
    }

    return render(request, 'blog/post_detail.html', context)


@login_required
def post_create(request):
    """Создание нового поста."""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Пост создан!')
            return redirect('post_detail', pk=post.id)
    else:
        form = PostForm()

    context = {'form': form, 'title': 'Создать пост'}
    return render(request, 'blog/post_form.html', context)


@login_required
def post_edit(request, pk):
    """Редактирование поста."""
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        messages.error(request, 'Можно редактировать только свои посты.')
        return redirect('post_detail', pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.updated_at = timezone.now()
            post.save()
            messages.success(request, 'Пост обновлён!')
            return redirect('post_detail', pk=post.id)
    else:
        form = PostForm(instance=post)

    context = {'form': form, 'post': post, 'title': 'Редактировать пост'}
    return render(request, 'blog/post_form.html', context)


@login_required
def post_delete(request, pk):
    """Удаление поста."""
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        messages.error(request, 'Можно удалять только свои посты.')
        return redirect('post_detail', pk=pk)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Пост удалён.')
        return redirect('post_list')

    context = {'post': post}
    return render(request, 'blog/post_confirm_delete.html', context)

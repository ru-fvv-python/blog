from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from taggit.models import Tag

from .forms import EmailPostForm, CommentForm
from .models import Post


class PostListView(ListView):
    """
    Альтернативнре представление списка постов
    """

    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_list(request, tag_slug=None):
    """
    в данном представлении извлекаются все посты со статусом PUBLISHED
    """
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    # Постраничная разбивка с 3 постами на страницу
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page_number не целое число, то
        # выдать первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если page_number находится вне диапазона, то
        # выдать последнюю страницу
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts,
                   'tag': tag})


def post_detail(request, year, month, day, post):
    """
    представление одиночного поста на странице
    """
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # список активных комментариев к этому посту
    comments = post.comments.filter(active=True)
    # форма для комментирования пользователями
    form = CommentForm
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form})


def post_share(request, post_id):
    """
    представление, чтобы создавать экземпляр формы и работать
    с передачей формы на обработку
    """
    # Извлечь пост по идентификатору id
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        # Форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Поля формы успешно прошли валидацию
            cd = form.cleaned_data
            # ... отправить электронное письмо
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = '{} recommends you read {}'.format(cd['name'],
                                                         post.title)

            message = 'Read {} at {}\n\n' \
                      '{}\'s comments: {}'.format(post.title,
                                                  post_url,
                                                  cd['name'],
                                                  cd['comments'])

            send_mail(subject, message, 'vladfomin2008@yandex.ru', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


@require_POST
def post_comment(request, post_id):
    """
    передача формы на обработку
    """
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    comment = None

    # Комментарий был отправлен
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # создать объект класса Comment, не сохраняя его в базе данных
        comment = form.save(commit=False)
        # назначить пост комментарию
        comment.post = post
        # сохранить комментарий в базе данных
        comment.save()
    return render(request, 'blog/post/comment.html',
                  {'post': post,
                   'form': form,
                   'comment': comment})

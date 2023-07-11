from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from blog.models import Post


# Create your views here.
# данном представлении извлекаются все посты со статусом PUBLISHED
def post_list(request):
    post_list = Post.published.all()

    # Постраничная разбивка с 3 постами на страницу
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)

    posts = paginator.page(page_number)
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})


# представление одиночного поста на странице
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    return render(request,
                  'blog/post/detail.html',
                  {'post': post})

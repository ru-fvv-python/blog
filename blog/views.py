from django.shortcuts import render, get_object_or_404

from blog.models import Post


# Create your views here.
# данном представлении извлекаются все посты со статусом PUBLISHED
def post_list(request):
    posts = Post.published.all()
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

from django.shortcuts import render, get_object_or_404

from blog.models import Post


# Create your views here.
# данном представлении извлекаются все посты со статусом PUBLISHED
def post_list(request):
    posts = Post.published.all()
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})


# редставление одиночного поста на странице
def post_detail(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)

    return render(request,
                  'blog/post/detail.html',
                  {'post': post})

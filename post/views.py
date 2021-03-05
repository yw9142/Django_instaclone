from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .admin import PostForm
from .models import Post


def post_list(request):
    posts = Post.objects.all()

    if request.user.is_authenticated:
        username = request.user
        user = get_object_or_404(get_user_model(), username=username)
        user_profile = user.profile
        return render(request, 'post/post_list.html', {
            'user_profile': user_profile,
            'posts': posts,
        })
    else:
        return render(request, 'post/post_list.html', {
            'posts': posts,
        })


@login_required  # 데코레이터 : 로그인 상태인 경우에만 작동하는 함수
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # 유저 정보를 넣은 뒤 저장하기 위해 commit = False 옵션을 줌.
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # post.tag_save()
            messages.info(request, '새 글이 등록되었습니다.')
            return redirect('post:post_list')
    else:
        form = PostForm()
    return render(request, 'post/post_new.html', {
        'form': form,
    })


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:  # post data와 request data가 다르다면 경고
        messages.warning(request, '잘못된 접근입니다')
        return redirect('post:post_list')

    if request.method == 'POST':  # POST요청이라면 PostForm에 요청정보 넣기
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            # post.tag_set.clear()
            # post.tag_save()
            messages.success(request, '수정완료')
            return redirect('post:post_list')
    else:
        form = PostForm(instance=post)

    return render(request, 'post/post_edit.html', {
        'post': post,
        'form': form,
    })


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # URL을 통한 DB 접근 방지
    if post.author != request.user or request.method != 'POST':
        messages.warning(request, '잘못된 접근입니다.')
    else:
        post.delete()
        # messages.success(request, '삭제완료')
    return redirect('post:post_list')

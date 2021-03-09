from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import json

from .forms import CommentForm
from .admin import PostForm
from .models import Post, Comment


def post_list(request, tag=None):
    posts = Post.objects.all()
    comment_form = CommentForm()
    post_list = Post.objects.all()
    if request.user.is_authenticated:
        username = request.user
        user = get_object_or_404(get_user_model(), username=username)
        user_profile = user.profile

        follow_set = request.user.profile.get_following
        following_post_list = Post.objects.filter(author__profile__in=follow_set)

        return render(request, 'post/post_list.html', {
            'user_profile': user_profile,
            'posts': post_list,
            'following_post_list': following_post_list,
        })
    else:
        return render(request, 'post/post_list.html', {
            'posts': post_list,
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


@login_required
@require_POST
def post_like(request):
    pk = request.POST.get('pk', None)
    post = get_object_or_404(Post, pk=pk)
    post_like, post_like_created = post.like_set.get_or_create(
        user=request.user)

    if not post_like_created:
        post_like.delete()
        message = "좋아요 취소"
    else:
        message = "좋아요"

    context = {'like_count': post.like_count,
               'message': message}

    return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
@require_POST
def post_bookmark(request):
    pk = request.POST.get('pk', None)
    post = get_object_or_404(Post, pk=pk)
    post_bookmark, post_bookmark_created = post.bookmark_set.get_or_create(
        user=request.user)

    if not post_bookmark_created:
        post_bookmark.delete()
        message = "북마크 취소"
    else:
        message = "북마크"

    context = {'bookmark_count': post.bookmark_count,
               'message': message}

    return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
def comment_new(request):
    pk = request.POST.get('pk')  # Ajax 통신 부분
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return render(request, 'post/comment_new_ajax.html', {
                'comment': comment,
            })
        return redirect("post:post_list")


@login_required
def comment_new_detail(request):
    pk = request.POST.get('pk')  # Ajax 통신 부분
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return render(request, 'post/comment_new_ajax.html', {
                'comment': comment,
            })
        return redirect("post:post_list")


@login_required
def comment_delete(request):
    pk = request.POST.get('pk')
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST' and request.user == comment.author:
        comment.delete()
        message = '삭제완료'
        status = 1

    else:
        message = '잘못된 접근입니다'
        status = 0

    return HttpResponse(json.dumps({'message': message, 'status': status, }), content_type="application/json")

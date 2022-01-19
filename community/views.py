from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PostForm,CommentForm
from django.contrib import messages
from .models import Post

# Create your views here.


def community_index(request):
    post_list_bit = Post.objects.filter(category ='bitcoin')
    post_list_alt = Post.objects.filter(category='altcoin')
    post_list_etc = Post.objects.filter(category='etc')

    return render(request,'community/community_index.html', {
        'post_list_bit' : post_list_bit,
        'post_list_alt': post_list_alt,
        'post_list_etc': post_list_etc,
    })


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.author= request.user
            post.save()
            messages.success(request,"포스팅을 저장했습니다.")
            return redirect(post)
    else:
        form = PostForm()
    return render(request,"community/post_form.html",{
        'form':form
    })

def post_detail(reqeust, pk):
    post = get_object_or_404(Post,pk=pk)
    comment_form=CommentForm()

    return render(reqeust, 'community/post_detail.html',{
        'post':post,
        'comment_form' :comment_form,
    })

@login_required
def comment_create(request,pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = Post.objects.get(pk=pk)
            comment.save()
            return redirect(comment.post)
    else :
        messages.success(request,"잘못된 접근입니다.")
        return redirect('community:community_index')
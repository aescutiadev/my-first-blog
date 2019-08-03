from django.utils import timezone
from .models import Post
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm


def post_list(request): # SELECT * FROM TODO alv!!!
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'inicio/post_list.html', {'posts': posts})

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'inicio/post_detail.html', {'post': post})

def post_new(request):
    if (request.method == "POST"): # Si el metodo es POST entonces:
        form = PostForm(request.POST) # Hace el request
        if (form.is_valid()): # Valida si no hay errores
            post = form.save(commit=False) # No quiero que se guarde aún
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('/', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'inicio/post_edit.html', {'form': form})

def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if (request.method == "POST"):
		form = PostForm(request.POST, instance=post)
		if (form.is_valid()):
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'inicio/post_edit.html', {'form': form})

def contact(request):
	return render(request,'inicio/contact.html')

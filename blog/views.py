from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Blog
from .forms import BlogPost

# Create your views here.
def home(request):  #crud 중 r
    myBlog = Blog.objects.all()
    return render(request, 'home.html', {'blogs': myBlog})

def detail(request, blog_id):
    blog_detail = get_object_or_404(Blog, pk = blog_id)
    return render(request, 'detail.html', {'blog':blog_detail})

def new(request):
    return render(request, 'new.html')

def create(request): #입력받은 내용을 데이터베이스에 넣어주는 함수
    blog = Blog()
    blog.title = request.GET['title']
    blog.body = request.GET['body']
    blog.pub_date = timezone.datetime.now()
    blog.save()
    return redirect('/blog/' + str(blog.id))

def blogpost(request):  #crud 중 c
    #1. 입력된 내용을 처리하는 기능 -> POST
    #2. 빈 페이지를 띄워주는 기능 -> GET
    if request.method =='POST':
        form = BlogPost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  #아직 저장하지 말고
            post.pub_date=timezone.now()    #시간 저장하고 나서
            post.save()     #저장
            return redirect('home')
    else:
        #입력받을 수 있는 form을 띄움
        form = BlogPost()
        return render(request,'new.html',{'form':form})

def update(request, pk):
    #어떤 블로그를 수정할지 해당 블로그 객체 가져오기
    blog = get_object_or_404(Blog, pk = pk)

    #해당 블로그 객체 pk에 맞는 입력공간 가져오기
    form = BlogPost(request.POST, instance=blog)

    if form.is_valid():
        form.save()
        return redirect('home')

    return render(request, 'update.html', {'form':form})

def delete(request, pk):
    myBlog = Blog.objects.get(pk = pk)
    return render(request, 'sure.html', {'blog':myBlog})

def sure(request, pk):
    blog = get_object_or_404(Blog, pk = pk)
    blog.delete()
    return redirect('home')
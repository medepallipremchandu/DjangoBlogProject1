from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render
from .forms import ContactForm
from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            subject = f"Message from {name}"
            body = f"Sender's email: {email}\n\nMessage:\n{message}"
            
            # Create and send the email
            email_message = EmailMessage(
                subject=subject,
                body=body,
                from_email=email,  # Sender's email address from the form
                to=['2000031715cse@gmail.com'],  # Replace with your recipient's email address
                reply_to=[email],  # Set the reply-to address to sender's email
            )
            email_message.send()
            
            return render(request, 'blog/success.html')  # Display a success page
    else:
        form = ContactForm()
    return render(request, 'blog/contact.html', {'form': form})

from .models import Post, Comment, Category
from .forms import CommentForm

def blog_index(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(title__icontains=query).order_by("-created_on")
    else:
        posts = Post.objects.all().order_by("-created_on")

    paginator = Paginator(posts, 5)  # 5 posts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    categories = Category.objects.all()
    
    return render(request, 'blog/index.html', {'posts': posts, 'query': query, 'categories': categories})

def blog_category(request, category):
    posts = Post.objects.filter(categories__name__contains=category).order_by("-created_on")
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "blog/category.html", context)

def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)

    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        "form": form,
    }

    return render(request, "blog/detail.html", context)

def about(request):
    return render(request, "blog/about.html")





def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            ######################### mail system #################################### 
            htmly = get_template('blog/Email.html')
            d = { 'username': username }
            subject, from_email, to = 'welcome', 'your_email@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            ################################################################## 
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form, 'title':'register here'})
  
################ login forms################################################### 
def Login(request):
    if request.method == 'POST':
  
        # AuthenticationForm_can_also_be_used__
  
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' welcome {username} !!')
            return redirect('blog_index')
        else:
            messages.info(request, f'account done not exit plz sign in')
    form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form':form, 'title':'log in'})

def logout_view(request):
    logout(request)
    # Custom logic, if any
    return redirect('blog_index')

from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'blog/password_reset.html'
    email_template_name = 'blog/password_reset_email.html'
    subject_template_name = 'blog/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('blog_index')
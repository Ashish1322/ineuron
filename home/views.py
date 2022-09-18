# importing some functions and libraries
from email.message import EmailMessage
from tkinter.tix import Tree
from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from .models import Contact
from django.contrib import messages
from blog.models import Post, Likes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from .utils import token_generator
from django.urls import reverse
from django.core.mail import send_mail, BadHeaderError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding  import DjangoUnicodeDecodeError,force_bytes,force_str
from newblog.settings import EMAIL_HOST_PASSWORD, EMAIL_HOST_USER
import smtplib
from django.core.paginator import Paginator


# Function to give popular posts 

def populars(request):
    a = Post.objects.all().order_by('-likes')
    p = Paginator(a,6)
    page_number = request.GET.get('page')
    pgs_page = p.get_page(page_number)
    likes_list = []
    for i in pgs_page:
        try:
            Likes.objects.get(user=request.user.username,post_sno = i.sno)
            likes_list.append(True)
        except Exception as e:
            likes_list.append(False)

    return render(request,'blog/bloghome.html',{'posts':zip(likes_list,pgs_page),'page_range':p.page_range,'lklist':likes_list})


# Home page for the Blog (Home Link on the website)
def bloghome(request):
    a = Post.objects.all().order_by('-likes')
    p = Paginator(a,6)
    page_number = request.GET.get('page')
    pgs_page = p.get_page(page_number)
    likes_list = []
    carouselPages = Post.objects.all()[0:3]

    for i in pgs_page:
        try:
            Likes.objects.get(user=request.user.username,post_sno = i.sno)
            likes_list.append(True)
        except Exception as e:
            likes_list.append(False)
    
    

    return render(request,'blog/bloghome.html',{'posts':zip(likes_list,pgs_page),'page_range':p.page_range,'lklist':likes_list,'carousal':carouselPages})




# contact Page on the website
def contact(request):
    if(request.method=="POST"):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Handling the worng inputs in the form
        if(len(name)<4 or len(email)<10):
            messages.error(request,'Please fill the form correctly')
        else:
            a = Contact(name=name,email=email,message=message)
            Contact.save(a)
            messages.success(request,'Your query has been submitted successfully we will contact you shortly')
        return render(request,'home/contact.html')

    return render(request,'home/contact.html')

# Search button functionality and Handling Search Queries
def search_result(request):

    if(request.method=='GET'):
        query = request.GET.get('query')
        if(query==None):
            return redirect('home')
        data = {'query':query}
        # Limitng the Characters in the Search
        if(len(query)>78):
            data['posts'] = "" # No results(Empty posts)
        else:
            a1 = Post.objects.filter(title__icontains=query) # If query in title
            a2 = Post.objects.filter(content__icontains = query) # if query in content
            a = a1.union(a2) # Taking union of above two query sets
            p = Paginator(a,6)
            likes_list = []
            page_number = request.GET.get('page')
            pgs_page = p.get_page(page_number)
            for i in pgs_page:
                try:
                    Likes.objects.get(user=request.user.username,post_sno = i.sno)
                    likes_list.append(True)
                except Exception as e:
                    likes_list.append(False)
                
            
            

        return render(request,'home/search.html',{'posts':zip(likes_list,pgs_page),'page_range':p.page_range, 'number':len(pgs_page)})

       
    return redirect("home")

# Search button functionality and Handling Search Queries
def category(request,slug):

    if(request.method=='GET'):
        
        # Limitng the Characters in the Search
    
        a1 = Post.objects.filter(category=slug) 
        p = Paginator(a1,6)
        likes_list = []
        page_number = request.GET.get('page')
        pgs_page = p.get_page(page_number)
        for i in pgs_page:
            try:
                Likes.objects.get(user=request.user.username,post_sno = i.sno)
                likes_list.append(True)
            except Exception as e:
                likes_list.append(False)
                
            


        return render(request,'home/search.html',{'posts':zip(likes_list,pgs_page),'page_range':p.page_range, 'number':len(pgs_page)})

       
    return redirect("home")


# Function for Handle all the working related with signup
def handleSignUp(request):

    # If the request come from a SignUp form then only do all the things
    if request.method == "POST":
        # Get the data of the signup
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        conpassword = request.POST['conpassword']
        # Validating for the input data
        if(User.objects.filter(username=username).exists()): # If user already exits
            messages.error(request,'This username already exists, Kindly Choose a different one.')
            return redirect('home')

        elif(User.objects.filter(email=email).exists()): # If user already exits
            messages.error(request,'An account with this email already exists')
            return redirect('home')

        elif(len(username)>15): # If username is greater then given limit
            messages.error(request,'Username exceeds 15 characters limit')
            return redirect('home')

        elif(password!=conpassword): # If Password and Confirm Password Does not Match
            messages.error(request,'Password does not matches')
            return redirect('home')

        # If no error occur then Creating the user
        else:
            # save temprarory
            myuser = User.objects.create_user(username, email, password)
            myuser.first_name = name
            myuser.is_active = False
            myuser.save()
            # Setting up activation email
            domain = get_current_site(request).domain
            uidb64 = urlsafe_base64_encode(force_bytes(myuser.pk))
            link =  reverse('activate',kwargs={'uidb64':uidb64,'token':token_generator.make_token(myuser)})
            activate_url = "http://"+domain+link
            subjet = "Activate your account"
            body = "Hi "+myuser.first_name + "Please use this link to verify your account\n"+activate_url
            msg = EmailMessage()
            msg['Subject'] = 'Activate your account'
            msg['From'] = EMAIL_HOST_USER
            msg['To'] = myuser.email
            content = body
            msg.set_content(content,subtype='html')
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
                smtp.send_message(msg)

        

            messages.warning(request,"The activation link has been sent on the email provided. Kindly check your email  to activate your account.")
            return redirect('home')

    # Else return the 404 Error(on Manually opening this url when request is not Post )
    else:
        return render(request,'home/signup.html')

# Function for Handling all the working related with the Login
def handleLogin(request):
    print("hello")
    # If the request come from a Login form then only do all the things
    if(request.method=="POST"):
        
        username = request.POST['loginusername']
        password = request.POST['loginpassword']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"Successfully Loged in")
            return redirect('home')
        else:
            messages.error(request,'Invalid credentials, Please try agian')
            return redirect('home')
    # Else return the 404 Error(on Manually opening this url when request is not Post )
    return render(request,'home/login.html')

# Logout Function(If the user is login then it will Logout else do nothing)
def handleLogout(request):
    logout(request)
    messages.success(request,"Successfully loged out")
    return redirect('home')


def get(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None
    if user is not None and token_generator.check_token(user,token):
        user.is_active = True
        user.save()        
        messages.success(request,"Your account has been verified and activated succesfully. Hoping for your better experience.")
        return redirect("home")

    messages.error(request,"There is some problem in link so please Try again.")
    return redirect("home")


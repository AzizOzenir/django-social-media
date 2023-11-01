from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from base.models import FollowersCount, Like, Post, Profile
from itertools import chain
# Create your views here.

@login_required(login_url="login")
def index(req):
    user_object = User.objects.get(username=req.user.username)
    user_profile = Profile.objects.get(user=user_object)

#    user_following = FollowersCount.objects.filter(follower=req.user.username)
    posts = Post.objects.all()
    my_likes = Like.objects.filter( username=req.user.username)
   

    
    context = {"user_profile":user_profile,"posts":posts,"my_likes":my_likes,"user_object":user_object,}
    
    
    
    return render(req,"index.html",context)

def signup(req):
    if req.method == "POST":
        username = req.POST["username"]
        email = req.POST["email"]
        password = req.POST["password"]
        password2 = req.POST["password2"]

        if password != password2:
            messages.info(req,"password doesnt math")
            return redirect("signup")
        else:
            if User.objects.filter(email=email).exists():
                messages.info(req,"Email already exists")
                return  redirect("signup")
            elif User.objects.filter(username = username).exists():
                messages.info(req,"This username taken")
                return redirect("signup")
            else:
                user  =User.objects.create_user(username=username,email = email,password=password)
                user.save()

                user_login = auth.authenticate(username = username, password = password)
                auth.login(req,user_login)

                user_model = User.objects.get(email = email)
                new_profile = Profile.objects.create(user=user_model,id_user =user_model.id)
                new_profile.save()
                return redirect("settings")

    else:
        return render(req,"signup.html")
    
def login(req):
    if req.method != "POST":
        return render(req,"login.html")
    else:
        username = req.POST["username"]
        password = req.POST["password"]
        user = auth.authenticate(username= username, password = password)

        if user != None:
            auth.login(request=req , user=user ) 
            return redirect("/")
        else:
            messages.info(req,"Credentials Invalid")
            return redirect("login")
        
def logout(req):
    auth.logout(req)
    return redirect("login")

@login_required(login_url="login")
def settings(req):
    user_profile = Profile.objects.get(user = req.user)
    if req.method == "POST":
        """ EDITING """
        if req.FILES.get("image") == None:
            image = user_profile.pp
            bio = req.POST["bio"]
            location = req.POST["location"]
            bg = user_profile.bg

            user_profile.bg = bg
            user_profile.pp = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        """ FIRST TIME CREATING PROFILE """      
        if req.FILES.get("image") != None:
            image = req.FILES.get("image")
            bio = req.POST["bio"]
            location = req.POST["location"]
            bg = req.FILES.get("bgImage")

            user_profile.bg = bg
            user_profile.pp = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        username = user_profile.user.username
        
        # Redirect to the user's profile page using the username
        return redirect(f"/profile/{username}")
        
    

    """ for first time when directing to this page """
    context = {"user_profile":user_profile}
    return render(req,"settings.html",context)

@login_required(login_url='login')
def upload(req):
    
    if req.method == 'POST':
        user = req.user 
        image = req.FILES.get('image')
        caption = req.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
   
    return render(req, "upload.html")

@login_required(login_url='login')
def like(req):
    username = req.user.username
    post_id = req.GET.get('post_id')
    scroll = req.GET.get('scroll')
    print("Scroll id is ",scroll )
    print("pOST id is ",post_id )

    post = Post.objects.get(id=post_id)

    like_filter = Like.objects.filter(post_id=post_id, username=username).first()

   
    if like_filter == None:
        new_like = Like.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.likes +=1
        post.save()
    else:
        like_filter.delete()
        post.likes -=1
        post.save()
    username = req.user.username
        
        # Redirect to the user's profile page using the username
    return redirect('/')


@login_required(login_url='login')
def profile(req,pk):
    current_user =req.user.username  #user_object = User.objects.get(username=req.user.username)
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=user_object)
    user_post_length = len(user_posts)


    followers = FollowersCount.objects.filter(user=pk)
    followings = FollowersCount.objects.filter(follower=pk)
    follower = req.user.username
    user = pk

    # cheking for is it already following or not 
    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(followers) # maybe user_object
    user_following = len(followings)
    posts = Post.objects.all()
    context = {"current_user":current_user  ,"isSelfProfile":current_user == user ,"followers":followers,"followings":followings, "user_profile":user_profile,"user_posts":user_posts,"posts":posts,"user_object":user_object,"user_post_length":user_post_length,"button_text":button_text,"user_followers":user_followers,"user_following":user_following}
    return render(req,"profile.html",context)

@login_required(login_url='login')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('profile/'+user)
    else:
        return redirect('/')
    

@login_required(login_url='login')
def search(req):
    user_object = User.objects.get(username=req.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if req.method == 'POST':
        username = req.POST['username']
        
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
        context = {'user_profile': user_profile, 'username_profile_list': username_profile_list}
    return render(req, 'search.html',context )

@login_required(login_url='login')
def delete_post(req):
    user_object = User.objects.get(username=req.user.username)
    post_id = req.GET.get('post_id')
    user_post = Post.objects.filter(user=user_object,id=post_id).first()
    user_post.delete()
    username = req.user.username
        
        # Redirect to the user's profile page using the username
    return redirect(f'/profile/{username}')
    

@login_required(login_url='login')
def search(request):
    query = request.GET.get('q')
    # __icontains helps to find users which contains username that given.
    results = Profile.objects.filter(user__username__icontains=query) if query else []
    return render(request, 'search.html', {'results': results, 'query': query})
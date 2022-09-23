from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login

from .forms import *
from django.template.defaulttags import register


@register.filter()
def get_item(dictionary, key):
    return dictionary.get(key)






@login_required(login_url='loginDashboard')
def indexDashboard(request):

    list_project = Project.objects.filter(owner=request.user)
 
    count_users  = User.objects.filter().exclude(is_staff=True).count()
    data = {
        "list_project":list_project,
        "count_users":count_users,
    }
    return render(request,'indexDashboard.html',data)


def loginDashboard(request):
    if request.user.is_authenticated:
        return redirect('indexDashboard')
    else:
        if 'login_form' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                user = authenticate(email=login_form.cleaned_data['email'], password=login_form.cleaned_data['password'])
                if user is not None:
                    try:
                        if user.is_active:
                            login(request, user)
                            return redirect('indexDashboard')
                    except:
                        login_form = LoginForm()
                        dataErrorLogin = "Lo sentimos, su usuario no esta habilitado para ingresar al sistema"
                        return render(request, 'loginUser.html', {'login_form': login_form, 'dataErrorLogin': dataErrorLogin})
                else:
                    login_form = LoginForm()
                    dataErrorLogin = "Usuario y/o contraseña no son válidos"
                    return render(request, 'loginUser.html', {'login_form': login_form, 'dataErrorLogin': dataErrorLogin})
            else:
                raise ('Error Login : Form Invalid')
        else:
            login_form = LoginForm()
            return render(request, 'loginUser.html', {'login_form': login_form})

def registerDashboard(request):
    if request.user.is_authenticated:
        return redirect('indexWebsite')
    else:
        if request.method == "POST":
            if 'register_form' in request.POST:
                user_register = RegisterForm(request.POST)
                if user_register.is_valid():
                    p2 = request.POST["password2"]
                    p1 = user_register.cleaned_data['password']

                    if not p1 == p2:
                        register_form = RegisterForm()
                        dataErrorRegister = "Las contraseñas no coinciden"
                        return render(request, 'registerUser.html', {'register_form': register_form, 'dataErrorRegister': dataErrorRegister})

                    User.objects.create_user(
                        email=user_register.cleaned_data['email'],
                        password=user_register.cleaned_data['password'],
                    )
                    user = authenticate(email=user_register.cleaned_data['email'], password=user_register.cleaned_data['password'])
                    if user is not None:
                        try:
                            if user.is_active:
                                login(request, user)
                                return redirect('indexDashboard')
                        except:
                            register_form = RegisterForm()
                            dataErrorRegister = "Lo sentimos, su usuario no esta habilitado para ingresar al sistema"
                            return render(request, 'registerUser.html', {'register_form': register_form, 'dataErrorRegister': dataErrorRegister})
                else:
                    register_form = RegisterForm()
                    dataErrorRegister = "Lo sentimos ya existe una cuenta registrada con estos datos"
                    return render(request, 'registerUser.html', {'register_form': register_form, 'dataErrorRegister': dataErrorRegister})
        else:
            register_form = RegisterForm()
            return render(request, 'registerUser.html', {'register_form': register_form})

def logoutDashboard(request):
    logout(request)
    return redirect('/')


 

#####################################
##  VIEWS MODULE USUARIO         ## 
#####################################


@login_required(login_url='loginView')
def listUserDashboard(request):
   
    list_users = User.objects.filter().exclude(is_staff=True)
    data = {
              
             "list_users":list_users,
        }
    return render(request,'listUserDashboard.html',data)


@login_required(login_url='loginView')
def createUserDashboard(request):
   
    if request.POST:
        form = createUserForm(request.POST,request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            user_new = User.objects.last()
            user_new.set_password(user_new.password)
            user_new.save()
            return redirect('listUserDashboard')
        else:
            form = createUserForm()
            data = {         
               
                "form":form,
            }
            return render(request,"createUserDashboard.html",data)
    else:
        form = createUserForm()
        data = {
            
            "form":form,
        }
        return render(request,"createUserDashboard.html",data)


@login_required(login_url='loginView')
def updateUserDashboard(request,pk):
    user_to_update = User.objects.get(pk=pk)
   
    if request.POST:
        form = updateUserForm(request.POST,request.FILES,instance=user_to_update)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            user_to_update.set_password(user_to_update.password)
            user_to_update.save()
            return redirect('listUserDashboard')
        else:
            form = updateUserForm(instance=user_to_update)
            data = {     
               
                "form":form,
            }
            return render(request,"updateUserDashboard.html",data)
    else:
        form = updateUserForm(instance=user_to_update)
        data = { 
            
            "form":form,
        }
        return render(request,"updateUserDashboard.html",data)


@login_required(login_url='loginView')
def deleteUserDashboard(request,pk):
   
    User.objects.get(pk=pk).delete()
    return redirect('listUserDashboard')
 

@login_required(login_url='loginView')
def viewUserDashboard(request,pk):
   
    user = User.objects.get(pk=pk)
    data = { 
       
        "user":user,
    }
    return render(request,'viewUserDashboard.html',data)   


@login_required(login_url='loginView')
def createProjectDashboard(request):
   
    if request.POST:
        form = createProjectForm(request.POST,request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.owner = request.user
            f.save()
            return redirect('indexDashboard')
        else:
            form = createProjectForm()
            data = {         
               
                "form":form,
            }
            return render(request,"createProjectDashboard.html",data)
    else:
        form = createProjectForm()
        data = {
            
            "form":form,
        }
        return render(request,"createProjectDashboard.html",data)

@login_required(login_url='loginView')
def updateProjectDashboard(request,pk):
    instance = Project.objects.get(pk=pk)
    if request.POST:
        form = updateProjectForm(request.POST,request.FILES,instance=instance)
        if form.is_valid():
            f = form.save(commit=False)
            f.owner = request.user
            f.save()
            return redirect('indexDashboard')
        else:
            form = updateProjectForm(instance=instance)
            data = {         
               
                "form":form,
            }
            return render(request,"updateProjectDashboard.html",data)
    else:
        form = updateProjectForm(instance=instance)
        data = {
            
            "form":form,
        }
        return render(request,"updateProjectDashboard.html",data)

@login_required(login_url='loginView')
def viewProjectDashboard(request,pk):
    project = Project.objects.get(pk=pk)
    list_chapters = Chapter.objects.filter(project=pk)
    data = { 
        "project":project,
        "list_chapters":list_chapters,
    }
    return render(request,'viewProjectDashboard.html',data)   


@login_required(login_url='loginView')
def createChapterDashboard(request,pk):
   
    if request.POST:
        form = createChapterForm(request.POST,request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.project = Project.objects.get(pk=pk)
            f.save()
            return redirect('viewProjectDashboard',pk)
        else:
            form = createChapterForm()
            data = {         
               
                "form":form,
            }
            return render(request,"createChapterDashboard.html",data)
    else:
        form = createChapterForm()
        data = {
            
            "form":form,
        }
        return render(request,"createChapterDashboard.html",data)


@login_required(login_url='loginView')
def updateChapterDashboard(request,pk,chapter):
    instance = Chapter.objects.get(pk=chapter)
    if request.POST:
        form = updateChapterForm(request.POST,request.FILES,instance=instance)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            return redirect('viewProjectDashboard',pk)
        else:
            form = updateChapterForm(instance=instance)
            data = {         
               
                "form":form,
            }
            return render(request,"updateChapterDashboard.html",data)
    else:
        form = updateChapterForm(instance=instance)
        data = {
            
            "form":form,
        }
        return render(request,"updateChapterDashboard.html",data)

@login_required(login_url='loginView')
def writeChapterDashboard(request,pk,chapter):
    instance = Chapter.objects.get(pk=chapter)
    notes = NotesChapter.objects.filter(chapter=chapter)
    if request.POST:
        form = writeChapterForm(request.POST,request.FILES,instance=instance)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            import time
            time.sleep(2.5)
            return redirect('writeChapterDashboard',pk,instance.pk)
        else:
            form = writeChapterForm(instance=instance)
            form_note = createNotesForm()
            data = {         
            
                "form":form,
                "form_note":form_note,
                "chapter":instance,
                "notes":notes,
            }
            return render(request,"writeChapterDashboard.html",data)
    else:
        form = writeChapterForm(instance=instance)
        form_note = createNotesForm()
        data = {
            
            "form":form,
            "form_note":form_note,
            "chapter":instance,
            "notes":notes,
        }
        return render(request,"writeChapterDashboard.html",data)

@login_required(login_url='loginView')
def writeNoteChapterDashboard(request,pk,chapter):
    instance = Chapter.objects.get(pk=chapter)
    notes = NotesChapter.objects.filter(chapter=chapter)
    if request.POST:
        form_note = createNotesForm(request.POST,request.FILES)
        if form_note.is_valid():
            f = form_note.save(commit=False)
            f.chapter = instance
            f.save()
            return redirect('writeChapterDashboard',pk,instance.pk)
        else:
            
            form_note = createNotesForm()
            data = {         
                
                "form_note":form_note,
                "chapter":instance,
                "notes":notes,
            }
            return render(request,"writeNoteChapterDashboard.html",data)
    else:
        
        form_note = createNotesForm()
        data = {
            
            "form_note":form_note,
            "chapter":instance,
            "notes":notes,
        }
        return render(request,"writeNoteChapterDashboard.html",data)


login_required(login_url='loginView')
def deleteNoteChapterDashboard(request,note):
    project = NotesChapter.objects.get(pk=note).chapter.project.pk
    chapter = NotesChapter.objects.get(pk=note).chapter.pk
    note_to_delete = NotesChapter.objects.get(pk=note).pk
    NotesChapter.objects.filter(pk=note_to_delete).delete()
    return redirect('writeChapterDashboard',project,chapter)

@login_required(login_url='loginView')
def listCharacterDashboard(request,pk):
    project = Project.objects.get(pk=pk)
    list_characters = Character.objects.filter(project=pk)
    data = { 
        "project":project,
        "list_characters":list_characters,
    }
    return render(request,'listCharacterDashboard.html',data)   


@login_required(login_url='loginView')
def createCharacterDashboard(request,pk):
    if request.POST:
        form = createCharacterForm(request.POST,request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.project = Project.objects.get(pk=pk)
            f.save()
            return redirect('listCharacterDashboard',pk)
        else:
            form = createCharacterForm()
            data = {         
               
                "form":form,
            }
            return render(request,"createCharacterDashboard.html",data)
    else:
        form = createCharacterForm()
        data = {
            
            "form":form,
        }
        return render(request,"createCharacterDashboard.html",data)


@login_required(login_url='loginView')
def updateCharacterDashboard(request,pk,character):
    instance = Character.objects.get(pk=character)
    if request.POST:
        form = updateCharacterForm(request.POST,request.FILES,instance=instance)
        if form.is_valid():
            f = form.save(commit=False)
            f.project = Project.objects.get(pk=pk)
            f.save()
            return redirect('listCharacterDashboard',pk)
        else:
            form = updateCharacterForm(instance=instance)
            data = {         
               
                "form":form,
            }
            return render(request,"updateCharacterDashboard.html",data)
    else:
        form = updateCharacterForm(instance=instance)
        data = {
            
            "form":form,
        }
        return render(request,"updateCharacterDashboard.html",data)
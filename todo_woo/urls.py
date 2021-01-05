from django.contrib import admin
from django.urls import path
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('signup/', views.signupUser, name='signupUser'),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('login/', views.loginUser, name='loginUser'),
    # Todos
    path('', views.home, name='home'),
    path('create/', views.createTodo, name='createTodo'),
    path('current/', views.currentTodos, name='currentTodos'),
    path('todo/<int:todo_pk>', views.viewTodo, name='viewTodo'),
]

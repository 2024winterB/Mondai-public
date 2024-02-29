from django.urls import path
from . import views

app_name = 'Mondai_app'
urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('regist/', views.RegistUserView.as_view(), name='regist'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('mine/', views.MineView.as_view(), name='mine'),
    path('<int:pk>/questions/', views.QuestionsView.as_view(), name='questions'),
    path('<int:pk>/question/<int:question_pk>', views.QuestionsView.as_view(), name='question'),
    path('create-keyword/', views.CreateKeywordView.as_view(), name='create-keyword'),
    path('update-keyword/<int:pk>/', views.UpdateKeywordView.as_view(), name='update-keyword'),
    path('<int:pk>/create-question/', views.CreateQuestionView.as_view(), name='create-question'),
    # questionを更新するため、category.idとquestion.idを指定し、updateview
    path('<int:pk>/update-question/<int:question_pk>/', views.UpdateQuestionView.as_view(), name='update-question'),
    path('<int:pk>/delete-question/<int:question_pk>/', views.DeleteQuestionView.as_view(), name='delete-question'),
    path('edituser/', views.EditUserView.as_view(), name='edituser'), 
    path('test', views.TestView.as_view(), name='test'),
    path('test/keyword/<str:check_favorite>/<int:keywords_pk>', views.TestView.as_view(), name='test-keyword'),
    path('test/keyword/<str:check_favorite>/<int:keywords_pk>/<int:questions_pk>', views.TestView.as_view(), name='test-keyword'),
    path('test/one/<str:check_favorite>/<int:questions_pk>', views.TestView.as_view(), name='test-one'),
    path('test/post/<str:check_favorite>/<str:question_method>/<int:pk>', views.TestView.as_view(), name='test-post'),
    path('answer/<str:check_favorite>/<str:question_method>/<int:grades_pk>', views.AnswerView.as_view(), name='answer'),
    path('detail/<str:check_favorite>/<int:question_pk>', views.DetailQuestionView.as_view(), name='detail-question'),
    path('profile/', views.UserProfileView.as_view(), name='profile'), 
    path('change-password/', views.PasswordView.as_view(), name='change-password'), 
    path('changedone-password/', views.PasswordCompleteView.as_view(), name='changedone-password'),
    # お気に入り登録・解除の処理
    path('favorite/<int:pk>/', views.favorite, name='favorite'),
    # キーワードのうち、お気に入りしたquestionsだけを見れるページ
    path('<int:pk>/favorite-questions/', views.FavoriteQuestionsView.as_view(), name='favorite-questions'),
    

    # 以下ボツ
    # path('others/', views.OthersView.as_view(), name='others'),

    # keywordに紐づくchoicesを追加するためのupdateview
    # path('<int:pk>/choices/', views.ChoiceView.as_view(), name='choice-list'),
   # <int:pk>/choice/addでChoiceViewの追加機能を呼び出す
    # path('<int:pk>/choice/add/', views.ChoiceView.add, name='choice-add'),
    # <int:pk>/choice/<int:choice_pk>/deleteでChoiceViewの削除機能を呼び出す
    # path('<int:pk>/choice/<int:choice_pk>/delete/', views.ChoiceView.delete, name='choice-delete'),
    
]

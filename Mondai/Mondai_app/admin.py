from django.contrib import admin

# Register your models here.

# adminサイトに登録したいモデルをインポートする
from .models import Keywords, Questions, Grades, Favorites

# adminサイトに登録したいモデルの管理クラスを定義する
# ここでは、デフォルトの管理クラスを使用しますが、カスタマイズすることもできます[^1^][1] [^2^][2] [^3^][3] [^4^][4]
class KeywordsAdmin(admin.ModelAdmin):
    list_display = ['id', 'keyword_name', 'search_tag', 'user'] 
    list_editable = ['keyword_name', 'search_tag', 'user']

class QuestionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'correct_answer', 'equal', 'note', 'keyword', 'user'] 
    list_editable = ['question', 'correct_answer', 'equal', 'note', 'keyword', 'user']

class GradesAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'score', 'challenge_number', 'correct_number', 'last_challenge_date','last_answer', 'user'] 
    list_editable = ['question', 'score', 'challenge_number', 'correct_number', 'last_challenge_date', 'last_answer', 'user']

class FavoritesAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'question'] 
    list_editable = ['user', 'question']

# admin.site.register関数でモデルと管理クラスを登録する
admin.site.register(Keywords, KeywordsAdmin)
admin.site.register(Questions, QuestionsAdmin)
admin.site.register(Grades, GradesAdmin)
admin.site.register(Favorites, FavoritesAdmin)

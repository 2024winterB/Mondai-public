from typing import Any

from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.db.models import Q # OR検索のために追加
from django.shortcuts import render,redirect,reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.base import TemplateView

from .forms import RegistForm, LoginForm, KeywordForm, CreateQuestionForm, EditUserForm, TestForm  # 自分で作ったフォームを使う
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from .models import Users,Favorites,Keywords,Questions, Grades
from django.urls import reverse_lazy
from django.contrib import messages # messagesをインポート
from django.db import IntegrityError # IntegrityErrorをインポートする
from django.core.exceptions import ObjectDoesNotExist # ObjectDoesNotExistをインポートする
from django.shortcuts import get_object_or_404
# Ajaxのリクエストに対応する処理を追加
from django.http import JsonResponse, HttpResponse
# querysetをjsonにするモジュール
from django.core import serializers
import json

import datetime
from sklearn import preprocessing
import random

# mecabを使う
import MeCab
from django.utils.safestring import mark_safe
import re


# ユーザー登録用
class RegistUserView(CreateView):
  template_name = 'regist.html' # 表示するHTMLファイルの名前を指定
  form_class = RegistForm # ユーザー登録に使うフォームを指定


# ログイン用
class LoginView(LoginView):
  template_name = 'login.html'
  authentication_form = LoginForm


# ログアウト用
class LogoutView(LogoutView):
  pass


# ホーム用
#↓適切なクラスviewに変更してください
class HomeView(LoginRequiredMixin, ListView):
  template_name = 'home.html' # 表示するHTMLファイルの名前を指定
  model = Keywords
  context_object_name = "keywords" # HTMLのレンダリング時に、HTMLファイル内で使用する名前を指定
  paginate_by = 10  # 1ページに表示する最大カテゴリ数を指定

  def get_context_data(self, **kwargs):
    # 既存のコンテキストをスーパークラスから取得
    ctx = super().get_context_data()
    # title を追加する
    ctx['title'] = 'home'
    # search_query(検索ワード)をコンテキストに追加
    ctx['search_query'] = self.request.GET.get('search', '')
    return ctx
  
  # HomeViewにアクセスしたら、どのデータを、どのように加工したものを表示するかの関数
  def get_queryset(self):
    # キーワード全件取得
    keywords = Keywords.objects.order_by("-id")
    # 検索フォームに入力した値を取得、searchキーが存在しない場合はNoneを返す
    search_query = self.request.GET.get('search', '')

    if search_query: # search_queryが存在する場合は次に進む(変数が空＝False扱い) -> QオブジェクトでOR条件
        keywords = keywords.filter(
          Q(keyword_name__icontains=search_query) |
          Q(search_tag__icontains=search_query)
        )
    return keywords

# 自分の画面用
#↓適切なクラスviewに変更してください
class MineView(LoginRequiredMixin, ListView):
  model = Keywords # DBのテーブル名
  template_name = 'mine.html' # 表示したいHTML
  context_object_name = "mine_keywords" # HTMLのレンダリング時に、HTMLファイル内で使用するオブジェクト名を指定
  paginate_by = 10  # 1ページに表示する最大カテゴリ数を指定

  def get_context_data(self):
    ctx = super().get_context_data()
    # title を追加する -> sidebar.htmlの{% if title != 'mine'%}で参照
    ctx['title'] = 'mine'
    # search_query(検索ワード)をコンテキストに追加
    ctx['search_query'] = self.request.GET.get('search', '')
    return ctx
  
  
  # Viewにアクセスしたら、どのデータを、どのように加工したものを表示するかの関数
  def get_queryset(self):
    # ログインユーザーがお気に入りに登録したquestionIDを取得し、単一のリスト[a,b,c,..]にする。
    favorite_question_ids = Favorites.objects.filter(user=self.request.user.id).values_list("question",flat=True)
    # questionIDをもとに、Keywordsテーブルをfilterして抽出する。.distinct()で重複を除く。
    queryset = Keywords.objects.filter(questions__in=favorite_question_ids).distinct()
    # 抽出したquerysetを、keywordsテーブルのid降順に並び変える。（よりあとにお気に入りに追加したものが上にくる）
    print(queryset)
    queryset = queryset.order_by("-id")

    # 検索フォームに入力した値を取得、searchキーが存在しない場合はNoneを返す
    search_query = self.request.GET.get('search', '')

    if search_query: # search_queryが存在する場合は次に進む(変数が空＝False扱い) -> QオブジェクトでOR条件
        queryset = queryset.filter(
          Q(keyword_name__icontains=search_query) |
          Q(search_tag__icontains=search_query)
        )
    return queryset


# 問題一覧画面用
#↓適切なクラスviewに変更してください
class QuestionsView(LoginRequiredMixin, ListView):
  model = Questions # DBのテーブル名
  template_name = 'questions.html' # 表示したいHTML
  paginate_by = 10  # 1ページに表示する最大カテゴリ数を指定

  # QuestionsViewにアクセス時、表示する問題を抽出する関数
  def get_queryset(self):
        # urlからkeywordのpkを取得
        keyword_id = self.kwargs['pk']
        # keywordに紐づくquestionをフィルター => ページネーションされたobject_listをHTMLに渡す
        queryset = Questions.objects.filter(keyword=keyword_id)
        return queryset

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      # keywordのオブジェクトをコンテキストに追加
      context['keyword'] = Keywords.objects.get(pk=self.kwargs['pk'])
      # ログインユーザーがお気に入りに登録したquestionIDを取得し、単一のリスト[a,b,c,..]にする。
      context['favorite_questions'] = Favorites.objects.filter(user=self.request.user.id).values_list("question",flat=True)
      obj_questions = Questions.objects.filter(keyword_id=self.kwargs['pk'])
      if obj_questions.count() == 1:
        context['question'] = obj_questions.first()

      return context

# お気に入り問題一覧画面用
#↓適切なクラスviewに変更してください
class FavoriteQuestionsView(LoginRequiredMixin, ListView):
  model = Questions # DBのテーブル名
  template_name = 'favorite-questions.html' # 表示したいHTML
  paginate_by = 10  # 1ページに表示する最大カテゴリ数を指定

  # FavoriteQuestionsViewにアクセス時、表示する問題を抽出する関数
  def get_queryset(self):
        # ログインユーザーのお気に入りquestionを取得
        user_favorites = Favorites.objects.filter(user=self.request.user.id).values_list("question",flat=True)
        # urlからkeywordのpkを取得
        keyword_id = self.kwargs['pk']
        # keywordに紐づくお気に入りquestionをフィルター => ページネーションされたobject_listをHTMLに渡す
        queryset = Questions.objects.filter(id__in=user_favorites, keyword=keyword_id)
        return queryset
    
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      # keywordのオブジェクトをコンテキストに追加
      context['keyword'] = Keywords.objects.get(pk=self.kwargs['pk'])
      # ログインユーザーがお気に入りに登録したquestionIDを取得し、単一のリスト[a,b,c,..]にする。
      context['favorite_questions'] = Favorites.objects.filter(user=self.request.user.id).values_list("question",flat=True)
      # 問題が一つしかない場合は、その問題をコンテキストに追加
      obj_favorite = Favorites.objects.filter(user = self.request.user.id).values_list("question",flat=True)
      obj_questions = Questions.objects.filter(keyword_id=self.kwargs['pk'], id__in=obj_favorite)
      if obj_questions.count() == 1:
        context['question'] = obj_questions.first()
      return context

# カテゴリの作成画面
#↓適切なクラスviewに変更してください
class CreateKeywordView(LoginRequiredMixin, CreateView):
    model = Keywords
    form_class = KeywordForm
    template_name = 'create-keyword.html'

    # get_success_urlメソッドをオーバーライドします。
    def get_success_url(self):
        # 作成したキーワードのidを取得します。
        keyword_id = self.object.id
        # 問題作成ページのURLを生成します。
        question_url = reverse_lazy('Mondai_app:create-question', kwargs={'pk': keyword_id})
        # 生成したURLを返します。
        return f"{question_url}?modal=show"

    def form_valid(self, form):
        if form.is_valid():
            # keywordのフォームを保存する前に、ログインユーザーのidをuserに設定
            form.instance.user = self.request.user
            response = super().form_valid(form)
            return response
        else:
            # バリデーションエラーがあればフォームを再表示
            return super().form_invalid(form)
        
# カテゴリの更新画面
#↓適切なクラスviewに変更してください
class UpdateKeywordView(LoginRequiredMixin, UpdateView):
    model = Keywords
    form_class = KeywordForm
    template_name = 'update-keyword.html'

    def get_success_url(self):
        keyword_id = self.object.id
        #変更後にモーダルを表示するためのクエリパラメータをURLに追加
        return f"{reverse('Mondai_app:questions', kwargs={'pk': self.kwargs['pk']})}?modal=show"
    
    def dispatch(self, request, *args, **kwargs):
        # dispatchメソッドをオーバーライド
        try:
            # get_objectメソッドを呼び出してオブジェクトを取得
            obj = self.get_object()
            # ログインユーザーが作成者と一致するかチェック
            if obj.user != self.request.user:
                # messagesにエラーメッセージを追加
                messages.error(self.request, "あなたにはこのキーワードを編集する権限がありません。")
                # home.htmlにリダイレクト
                return redirect(reverse("Mondai_app:questions", kwargs={"pk": self.kwargs['pk']}))
            
        except ObjectDoesNotExist:
            # オブジェクトが存在しない場合はリダイレクト
            return redirect('Mondai_app:home')
        # 一致する場合は親クラスのメソッドを呼び出す
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        if form.is_valid():
            # keywordのフォームを保存する前に、ログインユーザーのidをuserに設定
            form.instance.user = self.request.user
            self.request.session['keyword_name'] = form.instance.keyword_name
            response = super().form_valid(form)
            return response
        else:
            # バリデーションエラーがあればフォームを再表示
            return super().form_invalid(form)
      

# 問題作成画面
#↓適切なクラスviewに変更してください
class CreateQuestionView(LoginRequiredMixin, CreateView):
  template_name = 'create-question.html'
  form_class = CreateQuestionForm
  
  def get_success_url(self):
      return reverse("Mondai_app:questions", kwargs={"pk": self.kwargs['pk']})
  
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      # keywordのオブジェクトをコンテキストに追加
      context['keyword'] = Keywords.objects.get(pk=self.kwargs['pk'])
      return context
  
  def form_invalid(self, form):
      # Ajaxのリクエストの場合、エラーメッセージを含むHTMLを返します。
      if self.request.is_ajax():
        return HttpResponse(form.errors, status=400)
      # 通常のリクエストの場合、デフォルトの処理を行います。
      return super().form_invalid(form)

  def form_valid(self, form):
        # questionのフォームを保存する前に、ログインユーザーのidをuserに設定
        form.instance.user = self.request.user
        correct_answer = form.cleaned_data.get('correct_answer')
        # # 正答フォームに入力されたchoiceデータをオブジェクトとして入手
        equal = form.cleaned_data.get('equal')
        # URLからpkを取得する
        keyword_id = self.kwargs.get("pk")
        # pkからkeywordを入手
        keyword = get_object_or_404(Keywords, pk=keyword_id)

        # 保存するデータを持つインスタンスを作成
        self.object = form.save(commit=False)
        # AI生成ボタンが押された場合、GPTにプロンプトを投げて回答を生成する
        print(self.request.POST)
        if 'ai_generate' in self.request.POST:
          note = write_note(form.cleaned_data.get('question'),correct_answer)
          print(note)
          self.object.note += '\n GPT解説:　\n' + note

        # インスタンス変数にcorrect_answerとkeywordを保存する
        self.object.correct_answer= correct_answer
        self.object.equal= equal
        self.object.keyword = keyword
        # テーブル反映する
        self.object.save()
        
        print(self.get_success_url())
        # Ajaxのリクエストの場合、成功したURLをJSONで返します。
        if self.request.is_ajax():
          return JsonResponse({"success_url": self.get_success_url()})
        
        # スーパークラスのform_validを呼び出してリダイレクト処理を完了
        return super().form_valid(form)


class UpdateQuestionView(LoginRequiredMixin, UpdateView):
  template_name = 'update-question.html'
  model = Questions  # 更新するモデルを指定
  form_class = CreateQuestionForm  # 更新に使うフォームを指定
  
  def get_success_url(self):
      return reverse("Mondai_app:questions", kwargs={"pk": self.kwargs['pk']})
  
  def dispatch(self, request, *args, **kwargs):
      # dispatchメソッドをオーバーライド
      try:
          # get_keywordメソッドを呼び出してオブジェクトを取得
          obj = self.get_object()
          # ログインユーザーが作成者と一致するかチェック
          if obj.user != self.request.user:
              # messagesにエラーメッセージを追加
              messages.error(self.request, "あなたにはこの問題を編集する権限がありません。")
              # questionsにリダイレクト
              return redirect(reverse("Mondai_app:questions", kwargs={"pk": self.kwargs['pk']}))
          
      except ObjectDoesNotExist:
          # オブジェクトが存在しない場合はリダイレクト
          return redirect(reverse("Mondai_app:questions", kwargs={"pk": self.kwargs['pk']}))
      # 一致する場合は親クラスのメソッドを呼び出す
      return super().dispatch(request, *args, **kwargs)

  def get_object(self):
        # URLからquestion_pkを取得する
        question_pk = self.kwargs['question_pk']
        # question_pkを使ってquestionのオブジェクトを取得する
        obj = get_object_or_404(Questions, pk=question_pk)
        # questionのオブジェクトを返す
        return obj
  
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      # keywordのオブジェクトをコンテキストに追加
      context['keyword'] = Keywords.objects.get(pk=self.kwargs['pk'])
      # questionのオブジェクトをコンテキストに追加
      context['question'] = Questions.objects.get(pk=self.kwargs['question_pk'])
      return context
  
  def form_valid(self, form):
        correct_answer = form.cleaned_data.get('correct_answer')
        # # 正答フォームに入力されたchoiceデータをオブジェクトとして入手
        equal = form.cleaned_data.get('equal')
        # URLからpkを取得する
        keyword_id = self.kwargs.get("pk")
        # pkからkeywordを入手
        keyword = get_object_or_404(Keywords, pk=keyword_id)

        # 保存するデータを持つインスタンスを作成
        self.object = form.save(commit=False)
        # インスタンス変数にcorrect_answerとkeywordを保存する
        self.object.correct_answer= correct_answer
        self.object.equal= equal
        self.object.keyword = keyword
        # テーブル反映する
        self.object.save()
        # スーパークラスのform_validを呼び出してリダイレクト処理を完了
        return super().form_valid(form)
  

class DeleteQuestionView(DeleteView):
    model = Questions
    
    def get_success_url(self):
      return reverse("Mondai_app:questions", kwargs={"pk": self.kwargs['pk']})
    
    def get_object(self):
        # URLからquestion_pkを取得する
        question_pk = self.kwargs['question_pk']
        # question_pkを使ってquestionのオブジェクトを取得する
        obj = get_object_or_404(Questions, pk=question_pk)
        # questionのオブジェクトを返す
        return obj
    
    def dispatch(self, request, *args, **kwargs):
      # dispatchメソッドをオーバーライド
      try:
          # get_keywordメソッドを呼び出してオブジェクトを取得
          obj = self.get_object()
          # ログインユーザーが作成者と一致するかチェック
          if obj.user != self.request.user:
              # messagesにエラーメッセージを追加
              messages.error(self.request, "あなたにはこの問題を編集する権限がありません。")
              # questionsにリダイレクト
              return redirect(reverse("Mondai_app:questions", kwargs={"pk": self.kwargs['pk']}))
          
      except ObjectDoesNotExist:
          # オブジェクトが存在しない場合はリダイレクト
          return redirect(reverse("Mondai_app:questions", kwargs={"pk": self.kwargs['pk']}))
      # 一致する場合は親クラスのメソッドを呼び出す
      return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


# 問題解く画面
class TestView(LoginRequiredMixin, FormView):
  template_name = 'test.html'
  form_class = TestForm #回答を記入するフォーム
  obj_question = None

  #Questionsテーブルより出題する問題文をランダムに抽出
  def get_context_data(self, **kwargs):
    # categoryのオブジェクトをコンテキストに追加
    context = super().get_context_data(**kwargs)
    #一度も解いたことの無い問題を入手
    unsolved_question = self.get_unsolved_question()
    #一度も解いたことがない問題がある場合
    print(unsolved_question.count())
    if unsolved_question.count() > 0:
      myobj_question = unsolved_question.order_by('?').first()

    #複数の問題がある場合
    elif "keywords_pk" in self.kwargs:  
      # 正答率と経過日数を用いた重みと問題の配列を入手
      list_evaluation, list_question_id = self.get_weight_correctrate_date()
      #重み配列を元に、ランダムに問題オブジェクトを入手する
      myobj_question= self.get_random_question(list_question_id, list_evaluation)

    #単一の問題がある場合
    elif "questions_pk" in self.kwargs:
      question_method="one"
      #urlより選択されたquiestion_idを入手する
      question_id =self.kwargs['questions_pk']
      #問題文に対応する問題オブジェクトをクエリにより入手し、コンテキストに追加
      myobj_question = Questions.objects.get(id=question_id)
 
    context['question'] = myobj_question

    #コンテキストに成績オブジェクトをセット。成績がない場合はNoneをセット
    try:
      context['grades'] = Grades.objects.get(question=myobj_question, user=self.request.user)
    except Grades.DoesNotExist:
      context['grades'] = None

    context['question_method'] = self.get_question_method()
    context['check_favorite'] = self.kwargs['check_favorite']
    # ログインユーザーがお気に入りに登録したquestionIDを取得し、単一のリスト[a,b,c,..]にする。
    context['favorite_questions'] = Favorites.objects.filter(user=self.request.user.id).values_list("question",flat=True)

    return context

  def form_valid(self, form): 
    #urlより選択された変数を入手する
    check_favorite=self.kwargs['check_favorite']
    question_method=self.kwargs['question_method']
    question_id =self.kwargs['pk']
    obj_question = Questions.objects.get(id=question_id)
    #問題文に対応する正答を入手
    f_correct = (form.cleaned_data.get('answer')==obj_question.correct_answer)
    #事前に前回の情報を入手。
    try:
      pre_obj = Grades.objects.get(question_id=question_id, user=self.request.user)
    except Grades.DoesNotExist:
      pre_obj = None
    #すでにGradeテーブルに問題を解いた結果がある場合は前回の情報を入手
    if pre_obj:
      pre_challenge_number = pre_obj.challenge_number
      pre_correct_number = pre_obj.correct_number
      pre_correct_rate = pre_obj.correct_rate
    #まだGradesテーブルに問題を解いた結果がない場合は初期値を入れる
    else:
      pre_challenge_number = 0
      pre_correct_number = 0
      pre_correct_rate = 0
    #Gradesテーブルにデータが登録されていなければcreate,登録していればupdate
    obj, created = Grades.objects.update_or_create(
        question=obj_question,
        user = self.request.user,
        defaults={"score":f_correct,"challenge_number": pre_challenge_number + 1, "correct_number": pre_correct_number + int(f_correct), 
        "correct_rate": (pre_correct_number + int(f_correct)) / (pre_challenge_number + 1), "last_answer":form.cleaned_data.get('answer'),
        "last_challenge_date":datetime.datetime.now()}
    )

    #問題解説画面に対して、登録した成績idを渡す
    self.success_url =reverse_lazy('Mondai_app:answer',kwargs={"check_favorite":check_favorite, "question_method":question_method,"grades_pk":obj.pk})
    return super().form_valid(form)

  #一度も解いたことがない問題は入手する
  def get_unsolved_question(self):

    list_favorite = Favorites.objects.filter(user=self.request.user.id).values_list("question",flat=True)
    #問題を解いたことがない問題を入手
    if self.kwargs['check_favorite'] == "normal":
      #指定キーワードの成績のない問題を入手
      if "keywords_pk" in self.kwargs:
         unsolved_question = Questions.objects.filter(keyword_id = self.kwargs["keywords_pk"]).exclude(grades__user=self.request.user)
      else:
          unsolved_question = Questions.objects.filter(id = self.kwargs["questions_pk"])
    elif self.kwargs['check_favorite'] == "favorite":
      #お気に入りの指定キーワードの成績のない問題を入手
      if "keywords_pk" in self.kwargs:
        unsolved_question = Questions.objects.filter(keyword_id = self.kwargs["keywords_pk"], id__in = list_favorite).exclude(grades__user=self.request.user)
      else:
        unsolved_question = Questions.objects.filter(id = self.kwargs["questions_pk"], id__in = list_favorite)
    
    return unsolved_question

  #正答率と経過日数を用いて重み配列を計算する
  def get_weight_correctrate_date(self):
    today = datetime.date.today() 
    corr_evaluation_a = 1
    corr_evaluation_b = 1
    
    if self.kwargs['check_favorite'] == "normal":
      #連続問題出題にて、直前の問題IDが指定されている場合はそれ以外の問題を評価指標に従って抽出する。 
      if "questions_pk" in self.kwargs:
        list_correct_rate = list(Grades.objects.filter(user=self.request.user, question__keyword_id=self.kwargs['keywords_pk']).exclude(question_id=self.kwargs['questions_pk']).values_list("correct_rate",flat=True))
        list_last_challenge_date = list(Grades.objects.filter(user=self.request.user, question__keyword_id=self.kwargs['keywords_pk']).exclude(question_id=self.kwargs['questions_pk']).values_list("last_challenge_date",flat=True))
        list_question_id = list(Grades.objects.filter(user=self.request.user, question__keyword_id=self.kwargs['keywords_pk']).exclude(question_id=self.kwargs['questions_pk']).values_list("question_id",flat=True))

      else:
        #初回問題出題にて、問題を評価指標に従って抽出する。 
        list_correct_rate = list(Grades.objects.filter(user=self.request.user, question__keyword_id=self.kwargs['keywords_pk']).values_list("correct_rate",flat=True))
        list_last_challenge_date = list(Grades.objects.filter(user=self.request.user, question__keyword_id=self.kwargs['keywords_pk']).values_list("last_challenge_date",flat=True))
        list_question_id = list(Grades.objects.filter(user=self.request.user, question__keyword_id=self.kwargs['keywords_pk']).values_list("question_id",flat=True))

    elif self.kwargs['check_favorite'] == "favorite":
      list_favorite = Favorites.objects.filter(user=self.request.user.id).values_list("question",flat=True)

      if "questions_pk" in self.kwargs:
        list_correct_rate = list(Grades.objects.filter(user=self.request.user, question__keyword_id=self.kwargs['keywords_pk'],question_id__in = list_favorite).exclude(question_id=self.kwargs['questions_pk']).values_list("correct_rate",flat=True))
        list_last_challenge_date = list(Grades.objects.filter(user=self.request.user, question__keyword_id=self.kwargs['keywords_pk'],question_id__in = list_favorite).exclude(question_id=self.kwargs['questions_pk']).values_list("last_challenge_date",flat=True))
        list_question_id = list(Grades.objects.filter(user=self.request.user, question__keyword_id=self.kwargs['keywords_pk'],question_id__in = list_favorite).exclude(question_id=self.kwargs['questions_pk']).values_list("question_id",flat=True))

      else:
        list_correct_rate = list(Grades.objects.filter(user=self.request.user, question__keyword_id=self.kwargs['keywords_pk'],question_id__in = list_favorite).values_list("correct_rate",flat=True))
        list_last_challenge_date = list(Grades.objects.filter(user=self.request.user, question__keyword_id=self.kwargs['keywords_pk'],question_id__in = list_favorite).values_list("last_challenge_date",flat=True))
        list_question_id = list(Grades.objects.filter(user=self.request.user, question__keyword_id=self.kwargs['keywords_pk'],question_id__in = list_favorite).values_list("question_id",flat=True))

    list_period_date = [(today - date).days for date in list_last_challenge_date]
    list_correct_rate_scaled = preprocessing.minmax_scale(list_correct_rate, feature_range=(0.01, 1))
    list_period_date_scaled = preprocessing.minmax_scale(list_period_date, feature_range=(0.01, 1))
    list_wrong_rate_scaled = 1 - list_correct_rate_scaled 
    list_evaluation_weight = corr_evaluation_a*list_wrong_rate_scaled+corr_evaluation_b*list_period_date_scaled
    return list_evaluation_weight, list_question_id

  #重み配列を元に、ランダムに問題オブジェクトを入手する
  def get_random_question(self, list_question_id, list_evaluation_weight):
    # 重み配列を元に、ランダムに問題オブジェクトを入手する
    question_id = random.choices(list_question_id, k = 1, weights = list_evaluation_weight)[0]
    obj_question = Questions.objects.get(id=question_id)
    
    return obj_question

  #問題の出題方式を文字列で返す
  def get_question_method(self):
    if "keywords_pk" in self.kwargs:  
      question_method="keyword"
    elif "questions_pk" in self.kwargs:
      question_method="one"
    return question_method

  
# 問題解説画面
#↓適切なクラスviewに変更してください
class AnswerView(LoginRequiredMixin, TemplateView):
  template_name = 'answer.html'

  def get_grades(self):
    # urlからgradesのpkを取得
    grades_id = self.kwargs['grades_pk']
    # gradesのオブジェクトを取得
    obj = get_object_or_404(Grades, pk=grades_id)
    return obj

  def dispatch(self, request, *args, **kwargs):
      # gradesオブジェクトを取得
      obj = self.get_grades()
      # ログインユーザーが作成者と一致するかチェック
      if obj.user != self.request.user:
          # messagesにエラーメッセージを追加
          messages.error(self.request, "他の人の成績は見れません")
          # testにリダイレクト
          return redirect(reverse("Mondai_app:home"))
            
      return super().dispatch(request, *args, **kwargs)

 
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    # check_favoriteをコンテキストに追加
    context['check_favorite'] = self.kwargs['check_favorite']

    # question_methodをコンテキストに追加
    context['question_method'] = self.kwargs['question_method'] 

    # gradesのオブジェクトをコンテキストに追加
    context['grades'] = self.get_grades()

    # gradesオブジェクトよりquestion_idを入手。該当するquestionオブジェクトをクエリにより入手し、コンテキストに追加
    question_id = context['grades'].question.id
    context['question'] = get_object_or_404(Questions, pk=question_id)

    # ログインユーザーがお気に入りに登録したquestionIDを取得し、単一のリスト[a,b,c,..]にする。
    context['favorite_questions'] = Favorites.objects.filter(user=self.request.user.id).values_list("question",flat=True)

    # keyword_nameの一覧を取得する
    # コンテキストにkeyword_listというキーで追加する
    keyword_list= serializers.serialize('json', Keywords.objects.all())
    # context["keyword_list"]をオブジェクトに変換
    keyword_list = json.loads(keyword_list)
    # リスト内包表記でpkとkeyword_nameを取り出して新しいリストを作る
    new_list = [{item["pk"]: item["fields"]["keyword_name"]} for item in keyword_list]
    # 辞書内包表記で新しい辞書を作成
    new_dict = {value: key for item in new_list for key, value in item.items()}
    # print(new_dict)
        # 文章と用語の辞書を定義する
    text = Questions.objects.filter(pk=question_id).values_list("note",flat=True).first()
    # print(text)
    terms = new_dict
    print(terms)

    # mecabのインスタンスを作る
    mecab = MeCab.Tagger('-r /etc/mecabrc')

    # 文章を単語に分割する
    words = mecab.parse(text).splitlines()
    # print(words)

    # 用語に一致する単語があれば、aタグとリンクを付ける
    new_words = []
    print(terms)
    # ここでtermの中身を、文字が長い順に並べ直す
    sorted_terms = sorted(terms.items(), key=lambda x: len(x[0]), reverse=True)
    print(sorted_terms)

    for term in sorted_terms:
        # textをaタグで分割して、リストにする
        # aタグのパターンを定義する
        a_pattern = re.compile(r"<a.*?/a>")
        a_text_list = a_pattern.findall(text) # aタグで挟まれている部分のリスト
        no_a_text_list = a_pattern.split(text) # aタグで挟まれていない部分のリスト
        # text_list = a_pattern.split(text)
        print(no_a_text_list)
        # リストの奇数番目の要素（aタグで挟まれていない部分）に対して、用語に一致する単語にaタグとリンクを付ける処理を行う
        for i in range(len(no_a_text_list)):
            print(no_a_text_list[i])
            
            # mecabの分かち書き器を作成
            wakati = MeCab.Tagger("-Owakati -r /etc/mecabrc")
            
            print(term[0])
            # 用語を分かち書きして単語リストに変換
            wakati_words = wakati.parse(term[0]).split()
            if len(wakati_words) >= 2:
                # 用語を正規表現パターンにする
                pattern = re.compile(term[0])
                # 用語に一致する部分があれば、aタグとリンクを付ける
                if pattern.search(no_a_text_list[i]):
                  # リンクのURLを作る
                    url = reverse_lazy('Mondai_app:questions', kwargs={'pk': term[1]})
                    # aタグを作る
                    a_tag = f"<a href='{url}' style='font-weight:bold;'>{term[0]}</a>"
                    # aタグで文章を置き換える
                    no_a_text_list[i] = pattern.sub(a_tag, no_a_text_list[i])
                    print(no_a_text_list[i])

            else:
                new_words = []
                # 文章を単語に分割する
                words = mecab.parse(no_a_text_list[i]).splitlines()
                # 用語に一致する単語があれば、aタグとリンクを付ける
                for word in words:
                    # 空行を無視する
                    if word.strip() == "":
                        new_words.append("\n")
                        continue

                    # タブで分割できるかチェックする
                    if "\t" in word:
                        # 単語と品詞情報に分ける
                        word, info = word.split("\t")
                        # ここでaタグとリンクを付ける処理を行う
                        if word in terms:
                          # リンクのURLを作る
                          url = reverse_lazy('Mondai_app:questions', kwargs={'pk': terms[word]})
                          # aタグを作る
                          a_tag = f"<a href='{url}' style='font-weight:bold;'>{word}</a>"
                          # aタグを単語に置き換える
                          word = a_tag
                        new_words.append(word)
                    else:
                        continue
            
                # 新しい文章を作る
                a_text = "".join(new_words)
                # リストの要素を置き換える
                no_a_text_list[i] = a_text

        print(no_a_text_list)

        # aタグで挟まれている部分と置き換えた部分を交互に結合して、新しい文章を作る
        new_text = ""
        for i in range(len(a_text_list)):
            new_text += no_a_text_list[i] + a_text_list[i]
        new_text += no_a_text_list[-1]

        text = new_text

    a_text = text

    # 新しい文章を出力する
    print(a_text)
    
    context['a_note']=mark_safe(a_text)

    return context
  
  def post(self, request, *args, **kwargs):
    obj = self.get_grades()
    # リクエストからscoreの値を取得
    score = request.POST.get("score")
    score = int(score)
    # gradesテーブルにscoreを保存
    obj.score = score
    if score ==1:
       obj.correct_number += 1
    obj.save()
    # もとのページに戻る
    
    return redirect(request.META.get('HTTP_REFERER'))
  

class DetailQuestionView(LoginRequiredMixin, TemplateView):
  template_name = 'detail-question.html'

  def get_grades(self):
    # urlからgradesのpkを取得
    question_id = self.kwargs['question_pk']
    # questionのオブジェクトを取得
    question = Questions.objects.filter(id=question_id).get()
    # gradesのオブジェクトを取得または作成
    try:
      obj = Grades.objects.get(question=question, user=self.request.user)
    except Grades.DoesNotExist:
      obj =  None
    return obj

  def dispatch(self, request, *args, **kwargs):
      # gradesオブジェクトを取得
      obj = self.get_grades()
      # objがNoneの場合、エラーメッセージを表示してリダイレクト
      if obj is None:
          messages.error(self.request, "成績が存在しません")
          # return redirect(reverse("Mondai_app:home"))
      else:
          # ログインユーザーが作成者と一致するかチェック
          if obj.user != self.request.user:
              # messagesにエラーメッセージを追加
              messages.error(self.request, "他の人の成績は見れません")
              # testにリダイレクト
              return redirect(reverse("Mondai_app:home"))
            
      return super().dispatch(request, *args, **kwargs)

 
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    # check_favoriteをコンテキストに追加
    context['check_favorite'] = self.kwargs['check_favorite']

    # gradesのオブジェクトをコンテキストに追加
    context['grades'] = self.get_grades()

    # gradesオブジェクトよりquestion_idを入手。該当するquestionオブジェクトをクエリにより入手し、コンテキストに追加
    question_id = self.kwargs['question_pk']
    context['question'] = get_object_or_404(Questions, pk=question_id)

    # ログインユーザーがお気に入りに登録したquestionIDを取得し、単一のリスト[a,b,c,..]にする。
    context['favorite_questions'] = Favorites.objects.filter(user=self.request.user.id).values_list("question",flat=True)

    # keyword_nameの一覧を取得する
    # コンテキストにkeyword_listというキーで追加する
    keyword_list= serializers.serialize('json', Keywords.objects.all())
    # context["keyword_list"]をオブジェクトに変換
    keyword_list = json.loads(keyword_list)
    # リスト内包表記でpkとkeyword_nameを取り出して新しいリストを作る
    new_list = [{item["pk"]: item["fields"]["keyword_name"]} for item in keyword_list]
    # 辞書内包表記で新しい辞書を作成
    new_dict = {value: key for item in new_list for key, value in item.items()}
    # print(new_dict)
    # 文章と用語の辞書を定義する
    text = Questions.objects.filter(pk=question_id).values_list("note",flat=True).first()
    # print(text)
    terms = new_dict
    print(terms)

    # mecabのインスタンスを作る
    mecab = MeCab.Tagger('-r /etc/mecabrc')

    # 文章を単語に分割する
    words = mecab.parse(text).splitlines()
    # print(words)

    # 用語に一致する単語があれば、aタグとリンクを付ける
    new_words = []
    print(terms)
    # ここでtermの中身を、文字が長い順に並べ直す
    sorted_terms = sorted(terms.items(), key=lambda x: len(x[0]), reverse=True)
    print(sorted_terms)

    for term in sorted_terms:
        # textをaタグで分割して、リストにする
        # aタグのパターンを定義する
        a_pattern = re.compile(r"<a.*?/a>")
        a_text_list = a_pattern.findall(text) # aタグで挟まれている部分のリスト
        no_a_text_list = a_pattern.split(text) # aタグで挟まれていない部分のリスト
        # text_list = a_pattern.split(text)
        print(no_a_text_list)
        # リストの奇数番目の要素（aタグで挟まれていない部分）に対して、用語に一致する単語にaタグとリンクを付ける処理を行う
        for i in range(len(no_a_text_list)):
            print(no_a_text_list[i])
            
            # mecabの分かち書き器を作成
            wakati = MeCab.Tagger("-Owakati -r /etc/mecabrc")
            
            print(term[0])
            # 用語を分かち書きして単語リストに変換
            wakati_words = wakati.parse(term[0]).split()
            if len(wakati_words) >= 2:
                # 用語を正規表現パターンにする
                pattern = re.compile(term[0])
                # 用語に一致する部分があれば、aタグとリンクを付ける
                if pattern.search(no_a_text_list[i]):
                  # リンクのURLを作る
                    url = reverse_lazy('Mondai_app:questions', kwargs={'pk': term[1]})
                    # aタグを作る
                    a_tag = f"<a href='{url}' style='font-weight:bold;'>{term[0]}</a>"
                    # aタグで文章を置き換える
                    no_a_text_list[i] = pattern.sub(a_tag, no_a_text_list[i])
                    print(no_a_text_list[i])

            else:
                new_words = []
                # 文章を単語に分割する
                words = mecab.parse(no_a_text_list[i]).splitlines()
                # 用語に一致する単語があれば、aタグとリンクを付ける
                for word in words:
                    # 空行を無視する
                    if word.strip() == "":
                        new_words.append("\n")
                        continue

                    # タブで分割できるかチェックする
                    if "\t" in word:
                        # 単語と品詞情報に分ける
                        word, info = word.split("\t")
                        # ここでaタグとリンクを付ける処理を行う
                        if word in terms:
                          # リンクのURLを作る
                          url = reverse_lazy('Mondai_app:questions', kwargs={'pk': terms[word]})
                          # aタグを作る
                          a_tag = f"<a href='{url}' style='font-weight:bold;'>{word}</a>"
                          # aタグを単語に置き換える
                          word = a_tag
                        new_words.append(word)
                    else:
                        continue
            
                # 新しい文章を作る
                a_text = "".join(new_words)
                # リストの要素を置き換える
                no_a_text_list[i] = a_text

        print(no_a_text_list)

        # aタグで挟まれている部分と置き換えた部分を交互に結合して、新しい文章を作る
        new_text = ""
        for i in range(len(a_text_list)):
            new_text += no_a_text_list[i] + a_text_list[i]
        new_text += no_a_text_list[-1]

        text = new_text

    a_text = text

    # 新しい文章を出力する
    print(a_text)
    
    context['a_note']=mark_safe(a_text)

    return context


# ユーザー情報一覧画面
class UserProfileView(LoginRequiredMixin, DetailView):
  model = Users     
  template_name ='userprofile.html'
  
  def get_object(self, queryset=None):
    return self.request.user


# ユーザ情報編集画面
class EditUserView(LoginRequiredMixin, UpdateView):
  model = Users     
  form_class = EditUserForm   
  template_name = 'edit-user.html'
  success_url = reverse_lazy('Mondai_app:profile')  
  
  def get_object(self, queryset=None):
    return self.request.user
  
#パスワード変更画面
class PasswordView(PasswordChangeView):
  template_name = 'change-password.html'
  success_url = reverse_lazy('Mondai_app:changedone-password')
  
#パスワード変更完了画面
class PasswordCompleteView(LoginRequiredMixin,PasswordChangeDoneView):
  model = Users
  template_name = 'changedone-password.html'


# お気に入り登録・解除の処理
def favorite(request, pk):
    user = request.user
    if user.is_authenticated:
        # お気に入り登録されているか確認
        try:
           favorite = Favorites.objects.get(user=user, question=pk)
        except:
           favorite = None
        if favorite:
            # お気に入り登録されていたら削除
            favorite.delete()
        else:
            # お気に入り登録されていなかったら追加
            # question_idからカテゴリのインスタンスを取得
            question = Questions.objects.get(id=pk)
            Favorites.objects.create(user=user, question=question)
    # もとのページにリダイレクト
    return redirect(request.META.get('HTTP_REFERER'))


# chatGPT関係：今後改良必要
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain import LLMChain

def write_note(question, correct_answer):
    texts = '「' +question + '」の解説文を書いてください。なお、正解は' + correct_answer + 'です。'

    # 言語モデルとしてOpenAIのモデルを指定
    llm = OpenAI(model_name="gpt-3.5-turbo")

    # プロンプト文
    template = """
    {original_sentences}
    """

    # プロンプトのテンプレート内にある変数部分を設定
    prompt = PromptTemplate(
        input_variables=["original_sentences"],
        template=template,
    )

    # プロンプトを実行させるチェーンを設定
    llm_chain = LLMChain(llm=llm, prompt=prompt,verbose=True)
    response = llm_chain.run(texts)

    return response
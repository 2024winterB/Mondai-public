from django import forms
from .models import Users, Keywords, Questions, Grades
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm
# from django.forms.models import ModelChoiceField
# from django.forms import inlineformset_factory  # formsetを使用するためのモジュール
from django.core.exceptions import ValidationError


# ユーザー登録用
class RegistForm(forms.ModelForm):
    username = forms.CharField(label='名前')
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())

    class Meta:
        model = Users # フォームのデータを保存する先のモデルは Users
        fields = ['username', 'email', 'password'] # 使うフィールドの指定

    # clean_passwordメソッド: パスワードを検証するためのメソッド
    def clean_password(self):
        # フォームからパスワードを取得
        password = self.cleaned_data.get('password')

        # パスワードの検証を試みる
        try:
            validate_password(password)
        except ValidationError as e:
            # エラーが発生した場合、各エラーメッセージをフォームのpasswordフィールドに追加
            for error in e.error_list:
                self.add_error('password', error)

        # 検証が終わったらパスワードを返す
        return password

    # saveメソッド: フォームデータを保存するためのメソッド
    def save(self, commit=False):
        # 親クラスのsaveメソッドを呼び出してUserオブジェクトを取得
        user = super().save(commit=False)

        # パスワードを設定し、Userオブジェクトを保存
        user.set_password(self.cleaned_data['password'])
        user.save()

        # 保存されたUserオブジェクトを返す
        return user


# ログイン用
class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())

# ユーザー情報更新
class EditUserForm(forms.ModelForm):
    class Meta:
        model = Users #データベースUsersを指定
        fields = ['username', 'email']  #使用するフィールドの指定


# キーワード用form
class KeywordForm(forms.ModelForm):
    class Meta:
        model = Keywords
        fields = ['keyword_name', 'search_tag']


class CreateQuestionForm(forms.ModelForm):
  class Meta:
      #フォーム入力するテーブルと変数名を指定
      model = Questions
      fields = ('question', 'equal', 'correct_answer', 'note')

  def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)


# 問題回答用
class TestForm(forms.Form):
    answer = forms.CharField()

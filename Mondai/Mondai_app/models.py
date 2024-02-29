from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.urls import reverse_lazy

# ユーザー情報を管理するためのユーザーマネージャークラス
class UserManager(BaseUserManager):
    # 新しいユーザーを作成するメソッド
    def create_user(self, username, email, password=None):
        # メールアドレスがない場合はエラーを発生させる
        if not email:
            raise ValueError('Enter Email')
        # ユーザーモデルを作成し、メールアドレスを正規化して保存
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        # パスワードを設定して保存
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # 新しいスーパーユーザーを作成するメソッド
    def create_superuser(self, username, email, password):
        # スタッフ権限とスーパーユーザー権限をTrueに設定
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        # 変更を保存
        user.save(using=self._db)
        return user

# ユーザーモデルを定義するクラス
class Users(AbstractBaseUser, PermissionsMixin):
    # ユーザーの名前
    username = models.CharField(max_length=150)
    # ユーザーのメールアドレス（一意である必要があります）
    email = models.EmailField(max_length=255, unique=True)
    # アカウントがアクティブかどうか
    is_active = models.BooleanField(default=True)
    # スタッフ権限を持っているかどうか
    is_staff = models.BooleanField(default=False)

    # ログインに使用するフィールドを指定（この場合はメールアドレス）
    USERNAME_FIELD = 'email'
    # 必須のフィールド（username以外）を指定
    REQUIRED_FIELDS = ['username'] # email を追加

    # ユーザーマネージャーを指定
    objects = UserManager()

    # ユーザーの詳細ページへのURLを取得するメソッド
    def get_absolute_url(self):
        return reverse_lazy('Mondai_app:home')


# カテゴリを定義するクラス
class Keywords(models.Model):
    keyword_name = models.CharField(max_length=50,verbose_name="キーワード名",unique=True)
    search_tag = models.CharField(max_length=10,verbose_name="タグ",null=True, blank=True)
    user = models.ForeignKey(Users,verbose_name="キーワード作成者",on_delete=models.CASCADE)


# 問題を定義するクラス
class Questions(models.Model):
    JUDGE_TYPES = (
        ('1', '○✕判定'),
        ('0', '自己判定'),
    )
    question = models.TextField(verbose_name="問題文")
    correct_answer = models.TextField(verbose_name="正答")
    equal = models.CharField(max_length=10, choices=JUDGE_TYPES, default='1', verbose_name="判定タイプ")
    note = models.TextField(null=True, blank=True,verbose_name="備考・解説", default="")
    keyword = models.ForeignKey(Keywords,verbose_name="キーワードID",on_delete=models.CASCADE)
    user = models.ForeignKey(Users,verbose_name="問題作成者",on_delete=models.CASCADE)


# 成績を定義するクラス
class Grades(models.Model):
    question = models.ForeignKey(Questions,verbose_name="問題ID",on_delete=models.CASCADE)
    score = models.BooleanField(null=True)
    challenge_number = models.IntegerField(null=True, blank=False, verbose_name="回答数", default=0)
    correct_number = models.IntegerField(null=True, blank=False, verbose_name="正答数", default=0)
    correct_rate = models.FloatField(null=True, blank=False, verbose_name="正答率")
    last_challenge_date = models.DateField(null=True, blank=False, default=None)
    last_answer = models.TextField(null=True, blank=False,verbose_name="ユーザーの最終回答", default=None)
    user = models.ForeignKey(Users,verbose_name="回答者",on_delete=models.CASCADE)

    #　データを保存するときにcorrect_rateを計算する
    def save(self, *args, **kwargs):
        # self.correct_numberやself.challenge_numberがNoneでないかどうかを確認する
        if self.correct_number is not None and self.challenge_number is not None:
            try:
                self.correct_rate = (self.correct_number / self.challenge_number) 
            except ZeroDivisionError:
                # ZeroDivisionErrorをexceptブロックでキャッチする
                self.correct_rate = None
        else:
            # どちらかのフィールドがNoneのときは、self.correct_rateにNoneを代入する
            self.correct_rate = None
        super().save(*args, **kwargs)

# お気に入り登録用の中間クラス
class Favorites(models.Model):
    user = models.ForeignKey(Users,verbose_name="ユーザーID",on_delete=models.CASCADE)
    question = models.ForeignKey(Questions,verbose_name="問題ID",on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "question"],
                name="favorite_unique"
            ),
        ]

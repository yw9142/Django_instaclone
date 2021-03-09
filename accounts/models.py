from django.db import models
from django.conf import settings  # django.conf에서 settings를 import
from imagekit.models import \
    ProcessedImageField  # imagekit에서 이미지를 처리하는 필드를 import
from imagekit.processors import \
    ResizeToFill  # imagekit에서 이미지 사이즈를 재조정하는 기능을 import


# 사용자가 업로드한 이미지 파일의 경로를 생성하여 반환해주는 함수
def user_path(instance, filename):
    from random import choice
    import string

    arr = [choice(string.ascii_letters) for _ in range(8)]  # 이미지파일 난수 저장
    pid = ''.join(arr)
    extension = filename.split('.')[-1]  # 파일 확장자명 분리 저장

    # return 'accounts/{}/{}.{}'.format(instance.user.username, pid, extension)
    return f'accounts/{instance.user.username}/{pid}.{extension}'


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    nickname = models.CharField('별명', max_length=20, unique=True)
    about = models.CharField(max_length=300, blank=True)

    GENDER_C = (  # Select box
        ('선택안함', '선택안함'),
        ('여성', '남성'),
        ('남성', '여성'),
    )

    gender = models.CharField('성별(선택사항)', max_length=10, choices=GENDER_C,
                              default='N')

    picture = ProcessedImageField(upload_to=user_path, processors=[
        # upload_to = 저장 위치 처리 항목
        ResizeToFill(150, 150)], format='JPEG', options={'quality': 90},
                                  blank=True)

    def __str__(self):
        return self.nickname

    follow_set = models.ManyToManyField('self',  # 자신을 참조
                                        blank=True,  # 아무도 팔로우를 안한 상태
                                        through='Follow',  # 중간 모델
                                        symmetrical=False, )  # 비대칭 관게

    # 해당 유저를 팔로우하고 있는 유저를 가져오는 속성
    @property
    def get_follower(self):
        return [i.from_user for i in self.follower_user.all()]

    # 해당 유저가 팔로우 하고 있는 유저를 가져오는 속성
    @property
    def get_following(self):
        return [i.to_user for i in self.follow_user.all()]

    # 팔로워 수 가져오는 속성
    @property
    def follower_count(self):
        return len(self.get_follower)

    # 팔로잉 수 가져오는 속성
    @property
    def following_count(self):
        return len(self.get_following)

    # 어떤 유저가 해당 유저의 팔로워인지 확인하는 속성
    def is_follower(self, user):
        return user in self.get_follower

    # 어떤 유저가 해당 유저의 팔로잉인지 확인하는 속성
    def is_following(self, user):
        return user in self.get_following


class Follow(models.Model):
    from_user = models.ForeignKey(Profile, related_name='follow_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(Profile, related_name='follower_user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # 관계가 언제 생겼는지 작성

    def __str__(self):  # 인스턴스 추적 양식 지정
        return f"{self.from_user} -> {self.to_user}"

    class Meta:
        unique_together = (
            ('from_user', 'to_user')  # 유니크한 관계 생성
        )

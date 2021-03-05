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

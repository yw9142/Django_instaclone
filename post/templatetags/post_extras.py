from django import template
import re

# register는 유효한 tag library를 만들기 위한 모듈 레벨의 인스턴스 객체이다.
register = template.Library()


@register.filter
def add_link(value):
    content = value.content  # 전달된 value 객체의 content 멤버변수를 가져온다.
    tags = value.tag_set.all()  # models.py tag_set 안에 전달된 value 객체의 tag_set 전체를 가져오는 queryset을 리턴한다.

    for tag in tags:
        content = re.sub(r'\#' + tag.name + r'\b', '<a href="/post/explore/tags/' + tag.name + '">#' + tag.name + '</a>', content)
    return content

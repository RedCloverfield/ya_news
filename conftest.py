import pytest

from news.models import Comment, News


@pytest.fixture
def comment_author(django_user_model):
    return django_user_model.objects.create(username='Автор комментария')


@pytest.fixture
def author_client(comment_author, client):
    client.force_login(comment_author)
    return client


@pytest.fixture
def news():    
    news = News.objects.create(
        title='Заголовок новости',
        text='Текст новости'
    )
    return news


@pytest.fixture
def pk_for_args(news):
    return news.pk,


@pytest.fixture
def comment(comment_author, news):
    comment = Comment.objects.create(
        news=news,
        author=comment_author,
        text='Текст комментария'
    )
    return comment
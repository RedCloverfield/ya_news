from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test import Client
from django.utils import timezone


from news.forms import BAD_WORDS
from news.models import Comment, News


@pytest.fixture
def comment_author(django_user_model):
    return django_user_model.objects.create(username='Автор комментария')


@pytest.fixture
def comment_reader(django_user_model):
    return django_user_model.objects.create(username='Читатель')


@pytest.fixture
def author_client(comment_author):
    author_client = Client()
    author_client.force_login(comment_author)
    return author_client


@pytest.fixture
def reader_client(comment_reader):
    reader_client = Client()
    reader_client.force_login(comment_reader)
    return reader_client


@pytest.fixture
def news():    
    return News.objects.create(
        title='Заголовок новости',
        text='Текст новости'
    )


@pytest.fixture
def pk_for_args(news):
    return news.pk,


@pytest.fixture()
def list_of_news():
    list_of_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=datetime.today() - timedelta(days=index))
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(list_of_news)


@pytest.fixture
def comment(comment_author, news):
    return Comment.objects.create(
        news=news,
        author=comment_author,
        text='Текст комментария'
    )


@pytest.fixture()
def list_of_comments(news, comment_author):
    for index in range(2):
        comment = Comment.objects.create(
            news=news,
            author=comment_author,
            text=f'Текст комментария {index}'
        )
        comment.created = timezone.now() + timedelta(days=index)
        comment.save()


@pytest.fixture
def comment_form_data():
    return {
        'text': 'Новый текст комментария',
    }


@pytest.fixture
def comment_upd_text(comment, comment_form_data):
    comment.text = comment_form_data['text']
    return comment


@pytest.fixture
def bad_words_data():
    return {
        'text': f'Текст, {BAD_WORDS[0]}, еще текст',
    }

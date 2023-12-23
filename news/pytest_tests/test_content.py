import pytest
from django.conf import settings
from django.urls import reverse


pytestmark = pytest.mark.django_db


@pytest.mark.usefixtures('list_of_news')
def test_news_count_on_home_page(client):
    """
    Проверяет, что количество выводимых на
    главную страницу новостей не превышает 10.
    """
    home_url = reverse('news:home')
    response = client.get(home_url)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.usefixtures('list_of_news')
def test_news_order(client):
    """Проверяет сортировку новостей на главной странице."""
    home_url = reverse('news:home')
    response = client.get(home_url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert sorted_dates == all_dates


@pytest.mark.usefixtures('list_of_comments')
def test_comments_order(client, news, pk_for_args):
    """Проверяет сортировку комментариев на странице новости."""
    url = reverse('news:detail', args=(pk_for_args))
    response = client.get(url)
    assert 'news' in response.context
    all_comments = news.comment_set.all()
    commets_dates = [comment.created for comment in all_comments]
    sorted_comments = sorted(commets_dates)
    assert sorted_comments == commets_dates


@pytest.mark.parametrize(
    'user_client, form_status',
    (
        (pytest.lazy_fixture('client'), False),
        (pytest.lazy_fixture('author_client'), True)
    )
)
def test_comment_form_availability_for_different_users(
    form_status, pk_for_args, user_client
):
    """Тестирует доступность формы создания комментария для пользователей."""
    url = reverse('news:detail', args=(pk_for_args))
    response = user_client.get(url)
    assert ('form' in response.context) is form_status

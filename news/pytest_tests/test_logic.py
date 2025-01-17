from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import WARNING
from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(
    client, comment_form_data, url_news_page
):
    """Проверяет, что анонимный пользователь не может создать комментарий."""
    client.post(url_news_page, data=comment_form_data)
    comment_count = Comment.objects.count()
    assert comment_count == 0


def test_auth_user_can_create_comment(
        author_client, comment_author, comment_form_data, news, url_news_page
):
    """
    Проверяет, что аутентифицированный пользователь
    может создать комментарий.
    """
    response = author_client.post(url_news_page, data=comment_form_data)
    assertRedirects(response, f'{url_news_page}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == comment_form_data['text']
    assert comment.news == news
    assert comment.author == comment_author


def test_user_cant_use_bad_words(author_client, bad_words_data, url_news_page):
    """
    Проверяет, что пользователь не может использовать
    запрещенные слова при создании комментария.
    """
    response = author_client.post(url_news_page, data=bad_words_data)
    assertFormError(response, 'form', 'text', errors=WARNING)
    comment_count = Comment.objects.count()
    assert comment_count == 0


@pytest.mark.parametrize(
    'user_client, authorship, expected_comment_count',
    (
        (pytest.lazy_fixture('author_client'), True, 0),
        (pytest.lazy_fixture('reader_client'), False, 1)
    )
)
def test_delete_comment_availability(
    authorship, comment, expected_comment_count, url_news_page, user_client
):
    """
    Проверяет возможность удалить комментарий
    для автора комментария и другого пользователя.
    """
    url = reverse('news:delete', args=(comment.id,))
    response = user_client.delete(url)
    if authorship:
        assertRedirects(response, f'{url_news_page}#comments')
    else:
        assert response.status_code == HTTPStatus.NOT_FOUND
    comment_count = Comment.objects.count()
    assert comment_count == expected_comment_count


@pytest.mark.parametrize(
    'user_client, authorship, expected_comment',
    (
        (
            pytest.lazy_fixture('author_client'),
            True,
            pytest.lazy_fixture('comment_upd_text')
        ),
        (
            pytest.lazy_fixture('reader_client'),
            False,
            pytest.lazy_fixture('comment')
        )
    )
)
def test_edit_comment_availability(
    authorship,
    comment,
    comment_form_data,
    expected_comment,
    url_news_page,
    user_client
):
    """
    Проверяет возможность редактировать комментарий
    для автора комментария и другого пользователя.
    """
    url = reverse('news:edit', args=(comment.id,))
    response = user_client.post(url, data=comment_form_data)
    if authorship:
        assertRedirects(response, f'{url_news_page}#comments')
    else:
        assert response.status_code == HTTPStatus.NOT_FOUND
    new_comment = Comment.objects.get()
    assert new_comment.text == expected_comment.text

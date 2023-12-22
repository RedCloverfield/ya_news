from http import HTTPStatus

from django.urls import reverse
import pytest
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db # Убрать?
@pytest.mark.parametrize(
        'page, args',
        (
            ('news:home', None),
            ('news:detail', pytest.lazy_fixture('pk_for_args')),
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None),
        )
)
def test_pages_availability_for_anonymous_user(client, page, args): # 1, 2, 6
    url = reverse(page, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
        'user_client, status',
        (
            (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
            (pytest.lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND)
        )
)
@pytest.mark.parametrize(
    'page',
    ('news:edit', 'news:delete')
)
def test_availability_for_comment_edit_and_delete(user_client, status, page, comment): # 3, 5
    url = reverse(page, args=(comment.pk,))
    response = user_client.get(url)
    assert response.status_code == status


@pytest.mark.parametrize(
        'page',
        ('news:edit', 'news:delete')
)
def test_redirect_for_anonymous_client(client, page, comment):
    login_url = reverse('users:login')
    url = reverse(page, args=(comment.pk,))
    redirect_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, redirect_url)

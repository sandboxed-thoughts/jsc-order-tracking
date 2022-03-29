from urllib import request

from django.test import Client, TestCase

from apps.accounts.models import CustomUser as User

from ..admin.client_admin import BuilderAdmin
from ..models import BuilderModel as Builder


class TestBuilderAdmin(TestCase):
    def setUp(self):
        # all tests need access to the client
        self.client = Client()

        # create the superuser to test views
        User.objects.create_superuser(
            email="super@test.usr", first_name="super", last_name="user", password="password"
        )
        self.user = User.objects.get(email="super@test.usr")

    def test_anonymous_user_redirects_to_login(self):
        client = self.client.get("/clients/buildermodel/")
        response = client

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login/?next=/clients/buildermodel/")

    def test_logged_in_user_gets_view(self):
        # user must be logged in before the get request is set
        self.client.force_login(self.user)
        # set the get request
        client = self.client.get("/clients/buildermodel/")
        response = client

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context["results"])
        self.assertQuerysetEqual(response.context["results"], Builder.objects.all())
        self.assertTemplateUsed("/admin/change_list.html")

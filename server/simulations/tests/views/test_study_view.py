from rest_framework import status
from rest_framework.test import APITestCase

from core.factories import UserFactory
from simulations.factories import StudyFactory


class StudyViewSetTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_list_only_returns_own_studies(self):
        own_study = StudyFactory(created_by=self.user)
        StudyFactory(created_by=self.other_user)

        response = self.client.get("/simulations/studies/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [study["id"] for study in response.data]
        self.assertEqual(ids, [own_study.id])

    def test_retrieve_own_study_returns_200(self):
        own_study = StudyFactory(created_by=self.user)

        response = self.client.get(f"/simulations/studies/{own_study.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], own_study.id)

    def test_retrieve_other_users_study_returns_404(self):
        other_study = StudyFactory(created_by=self.other_user)

        response = self.client.get(f"/simulations/studies/{other_study.id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_other_users_study_returns_404(self):
        other_study = StudyFactory(created_by=self.other_user)

        response = self.client.patch(
            f"/simulations/studies/{other_study.id}/", {"title": "Hijacked"}
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_destroy_other_users_study_returns_404(self):
        other_study = StudyFactory(created_by=self.other_user)

        response = self.client.delete(f"/simulations/studies/{other_study.id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

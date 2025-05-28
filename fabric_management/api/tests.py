from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import MaterialType


class MaterialTypeAPITestCase(APITestCase):
    def setUp(self):
        self.material_type = MaterialType.objects.create(
            name="Cotton",
            description="Soft natural fiber"
        )
        # Default router name pattern: modelname-list
        self.list_url = reverse('materialtype-list')

    def test_list_material_types(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.material_type.name)

    def test_retrieve_material_type(self):
        url = reverse('materialtype-detail', args=[self.material_type.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.material_type.name)
        self.assertEqual(response.data['description'],
                         self.material_type.description)

    def test_create_material_type(self):
        data = {
            "name": "Silk",
            "description": "Smooth natural fiber"
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MaterialType.objects.count(), 2)
        self.assertEqual(MaterialType.objects.get(
            id=response.data['id']).name, "Silk")

    def test_update_material_type(self):
        url = reverse('materialtype-detail', args=[self.material_type.id])
        data = {
            "name": "Cotton Updated",
            "description": "Updated description"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.material_type.refresh_from_db()
        self.assertEqual(self.material_type.name, "Cotton Updated")

    def test_delete_material_type(self):
        url = reverse('materialtype-detail', args=[self.material_type.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(MaterialType.objects.filter(
            id=self.material_type.id).exists())

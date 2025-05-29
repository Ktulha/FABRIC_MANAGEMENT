from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Material, Blueprint, ManufacturePlanItem, MaterialType, MaterialSubType, MaterialVariant, ManufactureResource, Shipment, ShipmentItem, ManufacturePlan, ResourcePlan, BlueprintItem


class MaterialModelTest(TestCase):
    def setUp(self):
        self.material_type = MaterialType.objects.create(name='Type1')
        self.material_sub_type = MaterialSubType.objects.create(
            name='SubType1', material_type=self.material_type)
        self.material_sub_type.material_type = self.material_type
        self.material_sub_type.save()
        self.material_variant = MaterialVariant.objects.create(name='Variant1')
        self.blueprint = Blueprint.objects.create(name='Blueprint1')
        self.material = Material(
            name='Material1',
            barcode='123456',
            material_type=self.material_type,
            material_sub_type=self.material_sub_type,
            material_variant=self.material_variant,
            blueprint=self.blueprint,
            image='material_img/test.png'
        )

    def test_material_save_sets_product_name_and_is_product(self):
        self.material.save()
        self.assertTrue(self.material.is_product)
        self.assertEqual(self.material.product_name,
                         f'{self.material.name}_{self.material.material_variant}')

    def test_material_save_raises_value_error_for_mismatched_type(self):
        other_type = MaterialType.objects.create(name='OtherType')
        self.material.material_sub_type.material_type = other_type
        self.material.material_sub_type.save()
        self.material.material_type = self.material_type
        with self.assertRaises(ValueError):
            self.material.save()

    def test_material_str(self):
        self.material.save()
        self.assertIn(self.material.product_name, str(self.material))
        self.assertIn(self.material.barcode, str(self.material))


class BlueprintModelTest(TestCase):
    def setUp(self):
        self.resource = ManufactureResource.objects.create(
            name='Resource1', work_slot_count=2)
        self.blueprint = Blueprint.objects.create(
            name='Blueprint1', resource=self.resource)

    def test_blueprint_str(self):
        self.assertEqual(str(self.blueprint),
                         f'Blueprint:{self.blueprint.name}')


class ManufacturePlanItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.material_type = MaterialType.objects.create(name='Type1')
        self.material_sub_type = MaterialSubType.objects.create(
            name='SubType1', material_type=self.material_type)
        self.material_variant = MaterialVariant.objects.create(name='Variant1')
        self.blueprint = Blueprint.objects.create(name='Blueprint1')
        print('done')
        self.material = Material.objects.create(
            name='Material1',
            barcode='123456',
            material_type=self.material_type,
            material_sub_type=self.material_sub_type,
            material_variant=self.material_variant,
            blueprint=self.blueprint
        )
        self.manufacture_plan = ManufacturePlan.objects.create(
            date='2024-01-01', user=self.user)
        self.plan_item = ManufacturePlanItem(
            manufacture_plan=self.manufacture_plan,
            material=self.material,
            amount=10,
            priority='medium'
        )

    def test_manufacture_plan_item_save_creates_resource_plan(self):
        self.plan_item.save()
        resource_plan = self.manufacture_plan.resource_plan_items.first()
        self.assertIsNotNone(resource_plan)
        self.assertEqual(resource_plan.slots, 1)

    def test_manufacture_plan_item_save_raises_value_error_without_blueprint(self):
        self.plan_item.material.blueprint = None
        self.plan_item.material.save()
        with self.assertRaises(ValueError):
            self.plan_item.save()


class MaterialViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.material_type = MaterialType.objects.create(name='Type1')
        self.material_sub_type = MaterialSubType.objects.create(
            name='SubType1', material_type=self.material_type)
        self.material_variant = MaterialVariant.objects.create(name='Variant1')
        self.blueprint = Blueprint.objects.create(name='Blueprint1')
        self.material_data = {
            'name': 'Material1',
            'barcode': '123456',
            'material_type': self.material_type.id,
            'material_sub_type': self.material_sub_type.id,
            'material_variant': self.material_variant.id,
            'blueprint': self.blueprint.id,
            'image': None,
            'product_name': 'Material1',
            'description': '',
            'is_product': False,
            'supplement_method': 'buy'
        }
        self.list_url = reverse('material-list')

    def test_create_material(self):
        response = self.client.post(
            self.list_url, self.material_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.material_data['name'])

    def test_list_materials(self):
        Material.objects.create(
            name='Material2',
            barcode='654321',
            material_type=self.material_type,
            material_sub_type=self.material_sub_type,
            material_variant=self.material_variant,
            blueprint=self.blueprint,
            image='material_img/test.png'
        )
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_retrieve_material(self):
        material = Material.objects.create(
            name='Material3',
            barcode='789012',
            material_type=self.material_type,
            material_sub_type=self.material_sub_type,
            material_variant=self.material_variant,
            blueprint=self.blueprint,
            image='material_img/test.png'
        )
        url = reverse('material-detail', args=[material.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], material.name)

    def test_update_material(self):
        material = Material.objects.create(
            name='Material4',
            barcode='345678',
            material_type=self.material_type,
            material_sub_type=self.material_sub_type,
            material_variant=self.material_variant,
            blueprint=self.blueprint,
            image='material_img/test.png'
        )
        url = reverse('material-detail', args=[material.id])
        update_data = {'name': 'Material4Updated'}
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Material4Updated')

    def test_delete_material(self):
        material = Material.objects.create(
            name='Material5',
            barcode='987654',
            material_type=self.material_type,
            material_sub_type=self.material_sub_type,
            material_variant=self.material_variant,
            blueprint=self.blueprint,
            image='material_img/test.png'
        )
        url = reverse('material-detail', args=[material.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

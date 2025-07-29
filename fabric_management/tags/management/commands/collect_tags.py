from django.core.management.base import BaseCommand
from tags.models import Tag, ProductTag, MaterialTag
from sales.models import Product
from blueprints.models import Material
from alive_progress import alive_bar
from django.db import transaction


class Command(BaseCommand):
    help = 'Collect and add tags from Product and Material name fields'

    def handle(self, *args, **options):
        self.stdout.write('Starting tag collection...')

        # Collect all tag names from products and materials
        product_tags_data = {}
        material_tags_data = {}
        tags_data = {}

        products = Product.objects.all()
        materials = Material.objects.all()
        products_dict = {p.pk: p for p in products}
        materials_dict = {m.pk: m for m in materials}

        # Collect tag names from products
        for product in products:
            if product.name:
                item = product.name.upper().replace('1,5', '1.5')
                tag_names = [tag.strip() for tag in item.split(
                    ',') if tag.strip() and len(tag.strip()) >= 3]
                first_word = item.split(',')[0].split(
                    ' ')[0].upper().replace(',', '')
                if first_word and len(first_word) >= 3:
                    tag_names.append(first_word)
                for tag_name in tag_names:
                    tags_data[tag_name] = tag_name
                    product_tags_data[(product.pk, tag_name)] = {
                        'product': product.pk,
                        'tag': tag_name
                    }

        # Collect tag names from materials
        for material in materials:
            if material.name:
                item = material.name.upper().replace('1,5', '1.5')
                tag_names = [tag.strip()for tag in item.split(
                    ',') if tag.strip() and len(tag.strip()) >= 3]
                first_word = item.split(',')[0].split(
                    ' ')[0].upper().replace(',', '')
                if first_word and len(first_word) >= 3:
                    tag_names.append(first_word)
                for tag_name in tag_names:
                    tags_data[tag_name] = tag_name
                    material_tags_data[(material.pk, tag_name)] = {
                        'material': material.pk,
                        'tag': tag_name
                    }

        existing_tags = Tag.objects.filter(name__in=tags_data.keys())
        existing_tags_dict = {t.name: t for t in existing_tags}
        tags_to_create = []
        for tag_name in tags_data.keys():
            if tag_name not in existing_tags_dict:
                tags_to_create.append(Tag(name=tag_name))
        Tag.objects.bulk_create(tags_to_create)
        all_tags = Tag.objects.filter(name__in=tags_data.keys())
        tags_dict = {tag.name: tag for tag in all_tags}
        print('tags created:', len(tags_to_create))

        existing_product_tags = ProductTag.objects.filter(
            product__pk__in=[p for p, t in product_tags_data.keys()],
            tag__name__in=[t for p, t in product_tags_data.keys()]
        )

        product_tags_to_create = {}

        existing_product_tags_dict = {}

        for p in existing_product_tags:
            key = (
                p.product.pk,
                p.tag.name
            )
            existing_product_tags_dict[key] = p
        for key, data in product_tags_data.items():
            if key not in existing_product_tags_dict:
                product_tags_to_create[key] = ProductTag(
                    product=products_dict[data['product']],
                    tag=tags_dict[data['tag']])
        if product_tags_to_create:
            ProductTag.objects.bulk_create(product_tags_to_create.values())
        print('product tags created:', len(product_tags_to_create))

        existing_material_tags = MaterialTag.objects.filter(
            material__pk__in=[m for m, t in material_tags_data.keys()],
            tag__name__in=[t for m, t in material_tags_data.keys()]
        )

        material_tags_to_create = {}

        existing_material_tags_dict = {}

        for p in existing_material_tags:
            key = (
                p.material.pk,
                p.tag.name
            )
            existing_material_tags_dict[key] = p
        for key, data in material_tags_data.items():
            if key not in existing_material_tags_dict:
                material_tags_to_create[key] = MaterialTag(
                    material=materials_dict[data['material']],
                    tag=tags_dict[data['tag']])
        if material_tags_to_create:
            MaterialTag.objects.bulk_create(material_tags_to_create.values())
        print('material tags created:', len(material_tags_to_create))

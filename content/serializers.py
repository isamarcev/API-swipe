from rest_framework import serializers

from content import models
from users import models as userModels
from content.services.service_serializer import update_related_object


class ComplexContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = userModels.Contact
        fields = ['first_name', 'last_name', 'email', 'phone']


class ComplexNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ComplexNews
        fields = ['title', 'description', 'complex', 'id', 'created']
        read_only_fields = ['id', 'created']


class ComplexBenefitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ComplexBenefits
        fields = ['id', 'parking',
                  'school', 'playground', 'hospital' ]


class ComplexDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ComplexDocument
        fields = ['id', 'title', 'complex', 'file']


class ComplexImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ComplexImage
        fields = '__all__'


class ComplexSerializer(serializers.ModelSerializer):
    complex_contact = ComplexContactSerializer()
    complex_benefits = ComplexBenefitsSerializer(many=False, required=False)
    complex_news = ComplexNewsSerializer(many=True, read_only=True)
    complex_images = ComplexImageSerializer(many=True, read_only=True)
    complex_documents = ComplexDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = models.Complex
        fields = ['id', 'owner', 'complex_contact', 'complex_benefits',
                  'description', 'address', 'min_price', 'price_per_m2',
                  'area_from', 'area_to', 'map_lat', 'map_long', 'status',
                  'type', 'klass', 'technology', 'territory',
                  'distance_to_sea', 'invoice', 'cell_height', 'gas',
                  'electricity', 'heating', 'water_cupply', 'sewerage',
                  'formalization', 'payment_form', 'purpose', 'payments_part',
                  'complex_news', 'complex_images', 'complex_documents']
        read_only_fields = ['id', 'owner', 'created_date',]

    def create(self, validated_data):
        contact_data = validated_data.pop('complex_contact')
        benefits_data = validated_data.pop('complex_benefits')
        complex_obj = models.Complex.objects.create(**validated_data)
        userModels.Contact.objects.create(**contact_data, complex=complex_obj,
                                          contact_type='Отдел продаж')
        models.ComplexBenefits.objects.create(complex=complex_obj,
                                              **benefits_data)
        return complex_obj

    def update(self, instance, validated_data):
        update_related_object(self, instance, validated_data,
                              field='complex_contact')
        update_related_object(self, instance, validated_data,
                              field='complex_benefits')
        return super(ComplexSerializer, self).update(instance, validated_data)


class ComplexCreateSerializer(ComplexSerializer):

    class Meta(ComplexSerializer.Meta):
        exclude = ['complex_news', 'complex_images', 'complex_documents']


class ApartmentImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ApartmentImage
        fields = '__all__'


class ComplexForApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Complex
        fields = ["id", "name"]


class ApartmentSerializer(serializers.ModelSerializer):
    apartment_images = ApartmentImageSerializer(many=True, required=False)

    class Meta:
        model = models.Apartment
        fields = ["id", "owner", "number", "corpus", "section", "floor",
                  "rises",'address', 'complex', 'foundation', 'purpose',
                  'rooms', 'plan', 'condition', 'area', 'kitchenArea',
                  "has_balcony","heating", "payment_options", "comission",
                  "communication_type", "description", "price", "schema",
                  "apartment_images", "is_viewed", "price_per_square_meter"]
        read_only_fields = ["price_per_square_meter", "is_viewed", "owner"]

    def create(self, validated_data):
        apartment_images = validated_data.pop('apartment_images')
        apartment_obj = models.Apartment.objects.create(**validated_data)
        if apartment_images:
            models.ApartmentImage.objects.create(**apartment_images,
                                                 apartment=apartment_obj)
        return apartment_obj

    def update(self, instance, validated_data):
        apartment_images = validated_data.pop('apartment_images')
        if apartment_images:
            models.ApartmentImage.objects.update(apartment_images,
                                                 apartment=instance)
        return super(ApartmentSerializer, self).update(instance, validated_data)


class AdvertisementSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Advertisement


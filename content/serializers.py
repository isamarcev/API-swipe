import datetime
from django.core.files.base import ContentFile
from django.db.models import Max, Count
from rest_framework import serializers

import base64
from drf_extra_fields.fields import Base64ImageField, HybridImageField

from content import models
from content.services.service_serializer import update_related_object

from users import models as userModels
from users.models import CustomUser


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


class CorpusListingField(serializers.RelatedField):
    def to_representation(self, value):
        flat_for_corpus = models.Apartment.objects.filter(corpus=value.title).\
            count()
        corpus_info = value.title, flat_for_corpus
        return corpus_info


class ComplexSerializer(serializers.ModelSerializer):
    complex_contact = ComplexContactSerializer()
    complex_benefits = ComplexBenefitsSerializer(many=False, required=False)
    complex_news = ComplexNewsSerializer(many=True, read_only=True)
    complex_images = ComplexImageSerializer(many=True, read_only=True)
    complex_documents = ComplexDocumentSerializer(many=True, read_only=True)
    complex_corpus = CorpusListingField(many=True,
                                        read_only=True)

    class Meta:
        model = models.Complex
        fields = ['id', "name", 'owner', 'complex_contact', 'complex_benefits',
                  'description', 'address', 'min_price', 'price_per_m2',
                  'area_from', 'area_to', 'map_lat', 'map_long', 'status',
                  'type', 'klass', 'technology', 'territory',
                  'distance_to_sea', 'invoice', 'cell_height', 'gas',
                  'electricity', 'heating', 'water_cupply', 'sewerage',
                  'formalization', 'payment_form', 'purpose', 'payments_part',
                  'complex_news', 'complex_images', 'complex_documents',
                  'complex_corpus']
        read_only_fields = ['id', 'owner', 'created_date', 'complex_corpus']

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


class ComplexRestrictedSerializer(ComplexSerializer):

    class Meta(ComplexSerializer.Meta):
        fields = ("id", "complex_images", "address", "area_from", "min_price",
                  "name")
        read_only_fields = ("id", "complex_images", "address", "area_from",
                            "min_price", "name")


class ComplexCreateSerializer(ComplexSerializer):

    class Meta(ComplexSerializer.Meta):
        exclude = ['complex_news', 'complex_images', 'complex_documents']


class ApartmentImageListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        self.context.get('apartment').apartment_images.all().delete()
        count = 1
        new_images = []
        for elem in validated_data:
            image = models.ApartmentImage(image=elem.get('image'),
                                          order=count,
                                          apartment=self.context.get('apartment'))
            new_images.append(image)
            count += 1
        return models.ApartmentImage.objects.bulk_create(new_images)


class ApartmentImageSerializer(serializers.ModelSerializer):
    image = HybridImageField()
    order = serializers.IntegerField(required=False)

    class Meta:
        model = models.ApartmentImage
        fields = ("image", "order")
        list_serializer_class = ApartmentImageListSerializer


class ComplexForApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Complex
        fields = ["id", "name"]


class ApartmentSerializer(serializers.ModelSerializer):
    apartment_images = ApartmentImageSerializer(many=True, required=False)
    complex = serializers.PrimaryKeyRelatedField(
        queryset=models.Complex.objects.all())

    class Meta:
        model = models.Apartment
        fields = ["id", "owner", "number", "corpus", "section", "floor",
                  "rises", 'address', 'complex', 'foundation', 'purpose',
                  'rooms', 'plan', 'condition', 'area', 'kitchenArea',
                  "has_balcony", "heating", "payment_options", "comission",
                  "communication_type", "description", "price", "schema",
                  "apartment_images", "price_per_square_meter",
                  "created_date"]
        read_only_fields = ["price_per_square_meter", "is_viewed", "owner",
                            "created_date"]

    def create(self, validated_data):
        apartment_images = validated_data.pop('apartment_images')

        apartment_obj = models.Apartment.objects.create(**validated_data,
                                                        owner=self.context.
                                                        get('owner'))
        models.Advertisement.objects.create(apartment=apartment_obj,
                                            created_by=apartment_obj.owner)
        try:
            image_serializer = ApartmentImageSerializer(
                data=apartment_images,
                context={'apartment': apartment_obj}, many=True)
            image_serializer.is_valid(raise_exception=True)
            image_serializer.save()
        except KeyError:
            pass
        return apartment_obj

    def update(self, instance, validated_data):
        try:
            apartment_images = validated_data.pop('apartment_images')
            image_serializer = ApartmentImageSerializer(
                data=apartment_images,
                context={'apartment': instance},
                many=True)
            image_serializer.is_valid(raise_exception=True)
            image_serializer.save()
        except KeyError:
            pass
        return super(ApartmentSerializer, self).update(instance, validated_data)


class UserShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("id", "first_name", "last_name", "is_developer", "avatar")


class ApartmentDetailSerializer(serializers.ModelSerializer):
    owner = UserShortSerializer()
    max_floor_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Apartment
        fields = ("id", "number", "floor",
                  "max_floor_count", "address", 'foundation', 'purpose',
                  "owner", 'rooms', 'plan', 'condition', 'area', 'kitchenArea',
                  "has_balcony", "heating", "payment_options", "comission",
                  "communication_type", "description", "price",
                  "apartment_images")

    def get_max_floor_count(self, obj):
        floor = models.Apartment.objects.filter(section=obj.section).\
            values_list('floor')
        max_count = 0
        for element in floor:
            if element[0] > max_count:
                max_count = element[0]
        return max_count


class ApartmentOwnerSerializer(ApartmentDetailSerializer):
    viewed_and_favourite = serializers.SerializerMethodField()

    class Meta(ApartmentDetailSerializer.Meta):
        fields = ApartmentDetailSerializer.Meta.fields +\
                 ("viewed_and_favourite", )

    def get_viewed_and_favourite(self, obj):
        users = CustomUser.objects\
            .filter(is_developer=False, is_staff=False)
        favourite_counter = len([1 for element in users
                                 if obj in element.favourite_apartment.all()])
        return {'viewed': len(obj.is_viewed.all()),
                "favourite": favourite_counter}


class AdvertisementSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Advertisement
        fields = ["id", "apartment", "is_big", "is_up", "is_turbo", "add_text",
                  "add_color", "text", "color"]
        read_only_fields = ["apartment"]
        
    def update(self, instance, validated_data):
        if validated_data.get('is_up'):
            flat = instance.apartment
            flat.created_date = datetime.datetime.now()
            flat.save()
        return super(AdvertisementSerializer, self).update(instance,
                                                           validated_data)


class ApartmentRestrictedSerializer(ApartmentSerializer):
    apartment_ad = AdvertisementSerializer()

    class Meta(ApartmentSerializer.Meta):
        fields = ("id", "address", "area", "price", "created_date",
                  "apartment_ad", "floor", "apartment_images")


class ComplaintSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Complaint
        fields = '__all__'
        read_only_fields = ("created", "is_reviewed", "user")

    def create(self, validated_data):
        complaint = models.Complaint.objects.create(
            **validated_data, user=self.context.get("user"))
        return complaint


class ComplexAndApartmentSerializer(serializers.Serializer):
    complex = ComplexRestrictedSerializer(many=True, read_only=True)
    apartment = ApartmentRestrictedSerializer(many=True, read_only=True)


class ApartmentModerationList(ApartmentRestrictedSerializer):

    class Meta(ApartmentRestrictedSerializer.Meta):
        fields = ("id", "address", "area", "price", "created_date",
                  "floor", "apartment_images")


class ApartmentModerationObject(serializers.ModelSerializer):
    apartment_images = ApartmentImageSerializer(many=True, required=False,
                                                read_only=True)
    owner = UserShortSerializer(read_only=True)

    class Meta:
        model = models.Apartment
        fields = ["id", "moderation_status", "owner", "number", "floor",
                  "moderation_decide", 'address', 'foundation', 'purpose',
                  'rooms', 'plan', 'condition', 'area', 'kitchenArea',
                  "has_balcony", "heating", "payment_options", "comission",
                  "description", "price", "apartment_images", "created_date"]
        read_only_fields = ("owner", "number", "floor", 'address',
                            'foundation', 'purpose','rooms', 'plan',
                            'condition', 'area', 'kitchenArea', "has_balcony",
                            "heating", "payment_options", "comission",
                            "description", "price", "apartment_images",
                            "created_date")

    def update(self, instance, validated_data):
        if validated_data.get("moderation_decide") == "Подтверждено":
            instance.is_moderated = True
        return super(ApartmentModerationObject, self).update(instance,
                                                             validated_data)

    def validate_moderation_decide(self, value):
        moderation_status = self.initial_data.get("moderation_status")
        if value == 'Отклонено' and not moderation_status:
            raise serializers.ValidationError(
                'При отклонении объявления нужно обязательно выбрать причину.'
            )
        return value



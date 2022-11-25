import datetime

from rest_framework import serializers

from content import models
from users import models as userModels
from content.services.service_serializer import update_related_object
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


class ApartmentImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ApartmentImage
        fields = ("image", )


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
                  "rises",'address', 'complex', 'foundation', 'purpose',
                  'rooms', 'plan', 'condition', 'area', 'kitchenArea',
                  "has_balcony","heating", "payment_options", "comission",
                  "communication_type", "description", "price", "schema",
                  "apartment_images", "is_viewed", "price_per_square_meter",
                  "created_date"]
        read_only_fields = ["price_per_square_meter", "is_viewed", "owner",
                            "created_date"]

    def create(self, validated_data):
        apartment_obj = models.Apartment.objects.create(**validated_data)
        models.Advertisement.objects.create(apartment=apartment_obj,
                                            created_by=apartment_obj.owner)
        try:
            apartment_images = validated_data.pop('apartment_images')
            models.ApartmentImage.objects.create(**apartment_images,
                                                 apartment=apartment_obj)
        except KeyError:
            pass
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
    complex = ComplexRestrictedSerializer(many=True, allow_null=True)
    apartment = ApartmentRestrictedSerializer(many=True)


class ApartmentModerationList(ApartmentRestrictedSerializer):

    class Meta(ApartmentRestrictedSerializer.Meta):
        fields = ("id", "address", "area", "price", "created_date",
                  "floor", "apartment_images")


class ApartmentModerationObject(serializers.ModelSerializer):
    apartment_images = ApartmentImageSerializer(many=True, required=False)
    # moderation_status = serializers.ChoiceField((
    #     ('price', 'Некорректная цена'),
    #     ('photo', 'Некорректное фото'),
    #     ('description',
    #      'Некорректное описание')
    # ))
    class Meta:
        model = models.Apartment
        fields = ["id", "moderation_status", "owner", "number", "floor",
                  "moderation_decide", 'address', 'foundation', 'purpose',
                  'rooms', 'plan', 'condition', 'area', 'kitchenArea',
                  "has_balcony", "heating", "payment_options", "comission",
                  "description", "price", "apartment_images", "created_date"]





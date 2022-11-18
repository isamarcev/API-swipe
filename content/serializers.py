from rest_framework import serializers

from content import models
from users import models as userModels


class ComplexContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = userModels.Contact
        fields = ['first_name', 'last_name', 'email', 'phone']


class ComplexNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ComplexNews
        fields = ['title', 'description', 'id', 'complex', 'created']


class ComplexBenefitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ComplexBenefits
        fields = ['id', 'parking',
                  'school', 'playground', 'hospital' ]


class ComplexDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ComplexDocument
        fields = '__all__'


class ComplexImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ComplexImage
        fields = '__all__'


class ComplexSerializer(serializers.ModelSerializer):
    complex_contact = ComplexContactSerializer(many=False, read_only=False)
    complex_benefits = ComplexBenefitsSerializer(many=False, required=False)

    class Meta:
        model = models.Complex
        fields = ['id', 'owner', 'complex_contact', 'complex_benefits',
                  'description', 'address', 'map_lat', 'map_long', 'status',
                  'type', 'klass', 'technology', 'territory',
                  'distance_to_sea', 'invoice', 'cell_height', 'gas',
                  'electricity', 'heating', 'water_cupply', 'sewerage',
                  'formalization', 'payment_form', 'purpose', 'payments_part']
        read_only_fields = ['owner', 'created_date', ]

    # def create(self, validated_data):


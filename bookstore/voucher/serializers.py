from rest_framework.serializers import ModelSerializer
from .models import *

class VoucherSerializer(ModelSerializer):
    class Meta:
        model = Voucher
        fields = '__all__'

class VoucherDetailSerializer(ModelSerializer):
    class Meta:
        model = Voucher_detail
        fields = '__all__'
from rest_framework.serializers import ModelSerializer
from .models import *

class VoucherSerializers(ModelSerializer):
    class Meta:
        model = Voucher
        fields = '__all__'

class DetailSerializers(ModelSerializer):
    class Meta:
        model = Voucher_detail
        fields = '__all__'
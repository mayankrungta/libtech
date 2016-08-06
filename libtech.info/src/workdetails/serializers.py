from rest_framework import serializers
from .models import Workdetail, MyWorkdetails

class WorkdetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workdetail
        field = ('id', 'title', 'slug', 'description', 'price', 'sale-price')

        '''
class MyWorkdetailsSerializer(serializers.ModelSerializer):
    workdetail = WorkdetailSerializer()
    class Meta:
        model = MyWorkdetails
        field = ('user', 'workdetails', 'workdetail')
        '''

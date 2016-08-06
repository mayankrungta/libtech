from rest_framework import serializers
from .models import Broadcast, MyBroadcasts

class BroadcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Broadcast
        field = ('id', 'name', 'description')

        '''
class MyBroadcastsSerializer(serializers.ModelSerializer):
    broadcast = BroadcastSerializer()
    class Meta:
        model = MyBroadcasts
        field = ('user', 'broadcasts', 'broadcast')
        '''

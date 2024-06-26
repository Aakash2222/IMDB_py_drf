from rest_framework import serializers
from .models import StreamPlatform,WatchList, Review

class WatchListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='watchlist-detail')
    owner = serializers.ReadOnlyField(source='WatchList.title')

    class Meta:
        model = WatchList
        # fields = '__all__'
        fields = ['title','owner','url','storyline','platform','active','created']

class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
    watchlist = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = StreamPlatform
        fields = '__all__'

    # Field level validation
    def validate_name(self,value):
        if len(value)<2:
            raise serializers.ValidationError("Name is too short")
        return value
     
    # Object level validation
    def validate(self, data):
        if data['name'] == data['about']:
            raise serializers.ValidationError('Name and about should not be same')
        return data

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    watchlist  = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        fields = '__all__'
        # exclude = ('watchlist',)
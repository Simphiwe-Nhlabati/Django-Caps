from rest_framework import serializers
from .models import Article, Publisher
from newsletter.models import Newsletter
from accounts.models import CustomUser


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 
                  'name', 
                  'editors', 
                  'journalists']
        # read_only_fields = ['id']
        # extra_kwargs = {
        #     'editors': {'required': False},
        #     'journalists': {'required': False}
        # } 
        
    
class JournalistSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id',
                  'username',
                  'email',
                  'first_name',
                  'last_name']


class ArticleSerializer(serializers.ModelSerializer):
    
    journalist = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=CustomUser.objects.filter(position='journalist'),
        required=True
    )
    editors = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CustomUser.objects.filter(position='editor'),
        required=True
    )
    
    class Meta:
        model = Article
        fields = ['id', 
                  'title', 
                  'content', 
                  'publisher', 
                  'journalist',
                  'editors', 
                  'created_at']
        # read_only_fields = ['id', 'created_at']
        # extra_kwargs = {
        #     'journalist': {'required': False}
        # }
        

class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ['id', 
                  'title', 
                  'content', 
                  'publisher', 
                  'journalist', 
                  'created_at']
        # read_only_fields = ['id', 'created_at']
        # extra_kwargs = {
        #     'journalist': {'required': False}
        # }
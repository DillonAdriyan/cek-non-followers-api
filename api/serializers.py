from rest_framework import serializers

# serializers.py 

class UploadFileSerializer(serializers.Serializer):
    followers_file = serializers.FileField()
    following_file = serializers.FileField()
    
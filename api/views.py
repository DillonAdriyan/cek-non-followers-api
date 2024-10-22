import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
import requests
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserLocation

@csrf_exempt  # Nonaktifkan CSRF untuk permintaan POST ini
def save_location(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            
            # Simpan lokasi ke database
            UserLocation.objects.create(latitude=latitude, longitude=longitude)
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'failed'}, status=400)




class FacebookProfileView(APIView):
    def get(self, request, *args, **kwargs):
        access_token = settings.INSTAGRAM_ACCESS_TOKEN  # Your Facebook token with public_profile scope

        url = "https://graph.facebook.com/me"
        params = {
            'fields': 'id,name,picture',  # Requesting basic fields
            'access_token': access_token
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            return Response(data)
        else:
            return Response({'error': 'Failed to retrieve data', 'details': response.json()}, status=response.status_code)
            
class InstagramDataView(APIView):
    permission_classes = [IsAuthenticated]  # Sesuaikan izin jika perlu
  
    def get(self, request, *args, **kwargs):
        access_token = settings.INSTAGRAM_ACCESS_TOKEN

        url = "https://graph.instagram.com/me"
        params = {
            'fields': 'id,username,followers_count,follows_count',
            'access_token': access_token
        }
        response = requests.get(url, params=params)
        print(response.status_code)
        print(response.text)  # Menampilkan respons dari API Instagram
        if response.status_code == 200:
            data = response.json()
            return Response(data)
        else:
            return Response({'error': 'Failed to retrieve data'}, status=400)
# Fungsi untuk ekstraksi username followers
def extract_usernames_followers(followers_file):
    try:
        data = json.load(followers_file)
        usernames = [entry['value'] for group in data for entry in group['string_list_data']]
        return usernames
    except Exception as e:
        raise ValueError(f"Error processing followers file: {str(e)}")

# Fungsi untuk ekstraksi username following
def extract_usernames_following(following_file):
    try:
        data = json.load(following_file)
        if 'relationships_following' in data:
            relationships = data['relationships_following']
            usernames = []
            for group in relationships:
                if 'string_list_data' in group:
                    for entry in group['string_list_data']:
                        usernames.append(entry.get('value'))
            return usernames
        else:
            raise ValueError("Invalid 'relationships_following' key in following JSON.")
    except Exception as e:
        raise ValueError(f"Error processing following file: {str(e)}")

# Fungsi untuk memeriksa akun yang tidak mengikuti balik
def check_non_followers(following_usernames, followers_usernames):
    non_followers = [user for user in following_usernames if user not in followers_usernames]
    return non_followers

# APIView untuk menangani unggahan file followers dan following serta memproses data
class CheckFollowersAPIView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        try:
            # Ambil file followers dan following dari request
            followers_file = request.FILES.get('followers_file')
            following_file = request.FILES.get('following_file')

            # Ekstrak username followers
            followers_usernames = extract_usernames_followers(followers_file)

            # Ekstrak username following
            following_usernames = extract_usernames_following(following_file)

            # Cek akun yang tidak mengikuti balik
            non_followers = check_non_followers(following_usernames, followers_usernames)

            return Response({'non_followers': non_followers}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

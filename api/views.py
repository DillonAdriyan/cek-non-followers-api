import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status

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

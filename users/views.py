from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from users.models import User
from users.serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.views import APIView
from drf_yasg import openapi


# Create your views here.

def home(request):
    return render(request, 'home.html')


def get_object(pk: int):
    """
    Get user by their ID.
    """
    try:
        return User.objects.get(pk=pk)
    except User.DoesNotExist:
        return JsonResponse({'message' : 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)

class UserList(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve a list of all users.",
        responses={200: UserSerializer(many=True), 400: 'Bad Request'},
    )
    def get(self, request: Request):
        # Get all users
        users = User.objects.all()

        # Get the user by their name
        name = request.query_params.get('name', None)
        if name is not None:
            users = users.filter(name__icontains=name)

        # serialize a QuerySet
        users_serializer = UserSerializer(users, many=True)
        # return the serialized data as a JsonResponss
        return JsonResponse(users_serializer.data, safe=False)
    
class AddUsers(APIView):
    @swagger_auto_schema(
        operation_description="Create a new user.",
        request_body=UserSerializer,
        responses={201: UserSerializer, 400: 'Bad Request', 500: 'Internal Server Error'},
    )
    def post(self, request):
        # parse the request into json
        try: 
            users_data = JSONParser().parse(request)
        except:
            return JsonResponse({'message' : 'Invalid request body'}, status=status.HTTP_400_BAD_REQUEST)
        # serialize the json data and store as the data attribute of the serializer
        users_serializer = UserSerializer(data=users_data)
        if users_serializer.is_valid():
            users_serializer.save()
            return JsonResponse(users_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(users_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDetail(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve a user by their ID.",
        responses={200: UserSerializer}
    )
    def get(self, request: Request, pk: int):
        user = get_object(pk)
        if user is None:
            return JsonResponse({'message' : 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        user_serializer = UserSerializer(user)
        return JsonResponse(user_serializer.data)
    
class UserUpdate(APIView):
    @swagger_auto_schema(
        operation_description="Update a user by their ID.",
        request_body=UserSerializer,
        responses={200: UserSerializer, 400: 'Bad Request'}
    )
    def put(self, request: Request, pk: int):
        user = get_object(pk)
        if user is None:
            return JsonResponse({'message' : 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        try: 
            user_data = JSONParser().parse(request)
        except:
            return JsonResponse({'message' : 'Invalid request body'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_serializer = UserSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data)
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDelete(APIView):
    @swagger_auto_schema(
        operation_description="Delete a user by their ID.",
        responses={204: 'No Content'}
    )
    def delete(self, request: Request, pk: int):
        user = self.get_object(pk)
        if user is None:
            return JsonResponse({'message' : 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            number, _ = user.delete()
        except:
            return JsonResponse({'message' : 'The user could not be deleted'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return JsonResponse({'message' : f'{number} user was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

# @swagger_auto_schema(
#     method='get',
#     responses={200: UserSerializer(many=True)},
#     operation_description="Retrieve a list of users. Optionally filter by 'name' query parameter."
# )
# @swagger_auto_schema(
#     method='post',
#     request_body=UserSerializer,
#     responses={201: UserSerializer, 400: 'Bad Request'},
#     operation_description="Create a new user."
# )
# @api_view(['GET', 'POST'])
# def users_list(request: Request):
#     if request.method == 'GET':
#         # Get all users
#         users = User.objects.all()

#         # Get the user by their name
#         name = request.query_params.get('name', None)
#         if name is not None:
#             users = users.filter(name__icontains=name)

#         # serialize a QuerySet
#         users_serializer = UserSerializer(users, many=True)
#         # return the serialized data as a JsonResponss
#         return JsonResponse(users_serializer.data, safe=False)
    
#     elif request.method == 'POST':
#         # parse the request into json
#         try: 
#             users_data = JSONParser().parse(request)
#         except:
#             return JsonResponse({'message' : 'Invalid request body'}, status=status.HTTP_400_BAD_REQUEST)
#         # serialize the json data and store as the data attribute of the serializer
#         users_serializer = UserSerializer(data=users_data)
#         if users_serializer.is_valid():
#             users_serializer.save()
#             return JsonResponse(users_serializer.data, status=status.HTTP_201_CREATED)
#         return JsonResponse(users_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# @api_view(['GET', 'PUT', 'DELETE'])
# def user_detail(request: Request, pk: int):
#     try:
#         user: User = User.objects.get(pk=pk)
#     except User.DoesNotExist:
#         return JsonResponse({'message' : 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)
    

#     if request.method == 'GET':
#         user_serializer: UserSerializer = UserSerializer(user)
#         return JsonResponse(user_serializer.data)
    
#     elif request.method == 'PUT':
#         try: 
#             user_data = JSONParser().parse(request)
#         except:
#             return JsonResponse({'message' : 'Invalid request body'}, status=status.HTTP_400_BAD_REQUEST)
        
#         user_serializer = UserSerializer(user, data=user_data)
#         if user_serializer.is_valid():
#             user_serializer.save()
#             return JsonResponse(user_serializer.data)
#         return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == 'DELETE':
#         try:
#             number, _ = user.delete()
#         except:
#             return JsonResponse({'message' : 'The user could not be deleted'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         return JsonResponse({'message' : f'{number} user was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)



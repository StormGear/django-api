from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from users.models import User
from users.serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.request import Request

# Create your views here.

def home(request):
    return render(request, 'home.html')

@api_view(['GET', 'POST'])
def users_list(request: Request):
    """
    Handles the retrieval and creation of users.
    GET:
    - Retrieves a list of users.
    - Optionally filters users by the 'name' query parameter.
    - Returns a JSON response containing the serialized user data.
    POST:
    - Parses the request data to create a new user.
    - Validates and saves the user data.
    - Returns a JSON response containing the serialized user data if successful.
    - Returns a JSON response with errors if the data is invalid.
    Args:
        request (Request): The HTTP request object.
    Returns:
        JsonResponse: A JSON response containing the serialized user data or errors.
        None: If the request method is not GET or POST.
    """
    if request.method == 'GET':
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
    
    elif request.method == 'POST':
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
    
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request: Request, pk: int):
    try:
        user: User = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return JsonResponse({'message' : 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)
    

    if request.method == 'GET':
        user_serializer: UserSerializer = UserSerializer(user)
        return JsonResponse(user_serializer.data)
    
    elif request.method == 'PUT':
        try: 
            user_data = JSONParser().parse(request)
        except:
            return JsonResponse({'message' : 'Invalid request body'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_serializer = UserSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data)
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        try:
            number, _ = user.delete()
        except:
            return JsonResponse({'message' : 'The user could not be deleted'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return JsonResponse({'message' : f'{number} user was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

import json
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from helloDanhApi.models import CustomUser, Alert, AlertPlacement

@csrf_exempt
def login_user(request):
    '''Handles the authentication of a user

    Method arguments:
      request -- The full HTTP request object
    '''

    req_body = json.loads(request.body.decode())

    if request.method == 'POST':
        # Use the built-in authenticate method to verify
        username = req_body['username']
        password = req_body['password']
        authenticated_user = authenticate(username=username, password=password)

        # If authentication was successful, respond with their token
        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            custom_user = CustomUser.objects.get(user=authenticated_user)
            data = json.dumps({"valid": True, "token": token.key, "user_id": custom_user.id})
            return HttpResponse(data, content_type='application/json')

        else:
            # Bad login details were provided. So we can't log the user in.
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type='application/json')


@csrf_exempt
def register_user(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # Load the JSON string of the request body into a dict
    req_body = json.loads(request.body.decode())

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    new_user = User.objects.create_user(
        username=req_body['email'],
        email=req_body['email'],
        password=req_body['password'],
        first_name=req_body['first_name'],
        last_name=req_body['last_name']
    )


    custom_user = CustomUser.objects.create(
        address=req_body['address'],
        phone_number=req_body['phone_number'],
        user=new_user
    )

    # Commit the user to the database by saving it
    custom_user.save()

    # Use the REST Framework's token generator on the new user account
    token = Token.objects.create(user=new_user)

    # Create default alerts to user upon registration
    default_alert_red = Alert.objects.create(
        alert='Fill this alert with an urgent message to let your contacts know you need immediate help! Remember that the greetings are prewritten for you. You are just writing the body of the email!',
        alert_placement=AlertPlacement.objects.get(pk=1),
        user=custom_user,
        subject='Urgent Message: Code Red'

    )
    default_alert_yellow = Alert.objects.create(
        alert='Fill this alert with a cautious message to let your contacts know to keep an eye out for you! Remember that the greetings are prewritten for you. You are just writing the body of the email!',
        alert_placement=AlertPlacement.objects.get(pk=2),
        user=custom_user,
        subject='Code Yellow. Please read.'
    )
    default_alert_green = Alert.objects.create(
        alert='Fill this alert with a message to let your contacts know you are okay! Remember that the greetings are prewritten for you. You are just writing the body of the email!',
        alert_placement=AlertPlacement.objects.get(pk=3),
        user=custom_user,
        subject='Code Green. Please read.'
    )

    # Add default alerts
    default_alert_red.save()
    default_alert_yellow.save()
    default_alert_green.save()



    # Return the token to the client
    data = json.dumps({"token": token.key})
    return HttpResponse(data, content_type='application/json')


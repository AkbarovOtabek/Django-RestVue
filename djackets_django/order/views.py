import stripe

from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from .serializers import *

# @api_view(['POST'])
# @authentication_classes([authentication.TokenAuthentication])
# @permission_classes([permissions.IsAuthenticated])
# def checkout(request):
#   serializer = OrderSerializer(data=request.data)

#   if serializer.is_valid():
#     stripe.api_key = settings.STRIPE_SECRET_KEY
#     paid_amount = sum(item.get('quantity')*item.get('product').price for item in serializer.validated_data['items'])

#     try:
#         charge = stripe.Charge.create(
#           amount = int(paid_amount*100),
#           currency = 'USD',
#           description='Charge from Djackets',
#           source=serializer.validated_data['stripe_token']
#       )
#         serializer.save(user=request.user, paid_amount=paid_amount)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     except Exception:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    # ⬇️ добавили context={'request': request}
    serializer = OrderSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    items = serializer.validated_data['items']
    paid_amount = sum(i['quantity'] * i['product'].price for i in items)

    try:
        charge = stripe.Charge.create(
            amount=int(paid_amount * 100),
            currency='usd',  # можно в нижнем регистре
            description='Charge from Djackets',
            source=serializer.validated_data['stripe_token'],
        )
    except stripe.error.StripeError as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    serializer.save(paid_amount=paid_amount)  # user берётся из HiddenField
    return Response(serializer.data, status=status.HTTP_201_CREATED)

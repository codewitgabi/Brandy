from django.shortcuts import render
from .models import Message
from .serializers import MessageSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model


User = get_user_model()


class CreateMessage(generics.CreateAPIView):
	serializer_class = MessageSerializer
	permission_classes = [IsAuthenticated]


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_messages(request, id):
	sender = User.objects.get(id= request.user.id)
	receiver = User.objects.get(id= id)
	
	sender_messages = Message.objects.filter(
		sender= sender,
		receiver= receiver)
	receiver_messages = Message.objects.filter(
		sender= receiver,
		receiver= sender)
	
	db_messages = sender_messages.union(
		receiver_messages).order_by("date_sent")
	
	db_messages = list(db_messages.values())
	
	chat_messages = []
	
	for message in db_messages:
		message["sender_id"] = User.objects.get(id= message["sender_id"]).username
		#message["date_created"] = str(message["date_created"])[:5]
		chat_messages.append(message)
		
	return Response({"messages": chat_messages})
	
	
from rest_framework.permissions import BasePermission
from tailor_api.models import Tailor

class IsAccountOwner(BasePermission):
	def has_object_permission(self, request, view, obj):
		return request.user.id == obj.id
		

class IsTailorAccountOwner(BasePermission):
	def has_object_permission(self, request, view, obj):
		tailor = Tailor.objects.get(id=obj.id)
		return  request.user == tailor.user



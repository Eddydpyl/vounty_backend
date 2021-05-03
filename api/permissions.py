from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class SafeMethods(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_staff


class IsUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and (obj == request.user or request.user.is_staff)


class IsUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user and (obj == request.user or request.user.is_staff)


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and (obj.user == request.user or request.user.is_staff)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user and (obj.user == request.user or request.user.is_staff)

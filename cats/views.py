from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.throttling import AnonRateThrottle, ScopedRateThrottle
from rest_framework.pagination import PageNumberPagination

from .models import Achievement, Cat, User
from .permissions import OwnerOrReadOnly, ReadOnly
from .pagination import CatsPagination
from .serializers import AchievementSerializer, CatSerializer, UserSerializer
from .throttling import WorkingHoursRateThrottle


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly, )
    # pagination_class = CatsPagination
    pagination_class = None
    throttle_classes = (WorkingHoursRateThrottle, ScopedRateThrottle)
    throttle_scope = 'low_request'
    filter_backends = (
        DjangoFilterBackend, filters.SearchFilter,
        filters.OrderingFilter
    )
    filterset_fields = ('color', 'birth_year')
    search_fields = ('name', 'owner__username')
    ordering_fields = ('name', 'birth_year')

    ordering = ('id')

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer

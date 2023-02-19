import os.path
from base64 import b64encode
from collections import Counter
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from django.core.files.storage import FileSystemStorage
from .models import Meal, MealCategory, MealClick, MealPhoto
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from .serializers import MenuSerializer, MealTypeSerializer, NewMealSerializer, MealPhotoSerializer
from rest_framework.response import Response
from rest_framework.decorators import action


class Menu(viewsets.ModelViewSet):
    serializer_class = MenuSerializer
    queryset = Meal.objects.all()
    filter_backends = [SearchFilter]
    search_fields = [
        "name",
        "detail",
        "price",
        "size",
        "category__meal_type",
        "photo__path"
    ]

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            return NewMealSerializer
        else:
            return super().get_serializer_class()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        instance_meal = Meal.objects.get(id=serializer.data['id'])
        MealClick.objects.create(meal=instance_meal, click_date=timezone.now())
        return Response(serializer.data)

    # def update(self, request, *args, **kwargs):
    #     print(request.data)
    #     category = request.data.pop('category')
    #     print(category)
    #     cat_id = MealCategory.objects.get(meal_type=category)
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.data['category'] = cat_id.id
    #     self.perform_update(serializer)
    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         instance._prefetched_objects_cache = {}
    #     return Response(serializer.data)
    #
    # def perform_update(self, serializer):
    #     serializer.save()
    #
    # def partial_update(self, request, *args, **kwargs):
    #     kwargs['partial'] = True
    #     return self.update(request, *args, **kwargs)

    @action(methods=['post'], detail=False, url_path='photo_upload')
    def upload(self, request, *args, **kwargs):
        photo = request.data.get('file')
        index_dot = photo.name.find('.')
        name = photo.name[:index_dot]
        meal = Meal.objects.get(name=name)
        FileSystemStorage(location=os.path.join(Path(__file__).resolve().parent.parent,
                                                f'cafe_core_app\static\images\meal_img\meal_{meal.id}')).save(
            photo.name, photo)
        obj_photo = MealPhoto.objects.create(path=os.path.join(Path(__file__).resolve().parent.parent,
                                                               f'cafe_core_app\static\images\meal_img\meal_{meal.id}\{photo.name}'),
                                             title=datetime.now())
        meal.photo.add(obj_photo.id)
        return Response(status=status.HTTP_201_CREATED)

    # def list(self, request, *args, **kwargs):
    #     object = Meal.objects.all()
    #     print(object)
    #     serializer = MenuSerializer(object)
    #     print(serializer.data)
    #     return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='get-stat')
    def stat(self, request):
        queryset = MealClick.objects.filter(meal=request.data['id'])
        stat = []
        for i in queryset:
            stat.append(i.click_date)
        counter = Counter(stat)
        meal_name = Meal.objects.get(id=request.data['id'])
        x = []
        y = []
        for key, value in counter.items():
            x.append(key)
            y.append(value)
        plt.title(f'Статистика блюда {meal_name}')
        plt.xlabel('Дата')
        plt.ylabel('Количество выборов блюд')
        plt.bar(x, y)
        plt.gcf().autofmt_xdate()
        plt.savefig(os.path.join(Path(__file__).resolve().parent.parent, 'cafe_core_app\static\images\stat\img.png'),
                    dpi=175)
        path_img = os.path.join(Path(__file__).resolve().parent.parent, 'cafe_core_app\static\images\stat\img.png')
        plt.close()
        # dct = {'results': path_img} # передача ссылки на изображение 1 способ
        with open(path_img, 'rb') as f:
            a = b64encode(f.read())
        dct = {'result': a}  # передача закодированного изображения 2 способ
        return Response(dct, status.HTTP_201_CREATED)


class MealType(viewsets.ModelViewSet):
    serializer_class = MealTypeSerializer
    queryset = MealCategory.objects.all()


class GetMealPhoto(viewsets.ModelViewSet):
    serializer_class = MealPhotoSerializer
    queryset = MealPhoto.objects.all()

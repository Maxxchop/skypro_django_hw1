import json

from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from ads.models import Ad, Category, User, Location
from ads.serializers import UserListSerializer, UserDetailSerializer, UserCreateSerializer, UserUpdateSerializer, \
    UserDestroySerializer, LocationSerializer
from skypro_django_hw1 import settings


def root(request):

    return JsonResponse({"status": "ok"}, status=200)
#    return JsonResponse(csv_to_json('./ads.csv'), safe=False, status=200)


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

# ------------------- Ad views ---------------------
class AdListView(ListView):
    model = Ad
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        category_id = request.GET.get("category_id", None)
        if category_id:
            self.object_list = self.object_list.filter(category_id__exact=category_id)

        name_text = request.GET.get("text", None)
        if name_text:
            self.object_list = self.object_list.filter(name__icontains=name_text)

        location_name = request.GET.get("location", None)
        if location_name:
            self.object_list = self.object_list.filter(author__locations__name__icontains=location_name)

        price_from = request.GET.get("price_from", None)
        price_to = request.GET.get("price_to", None)
        if price_from:
            self.object_list = self.object_list.filter(price__gte=price_from)
        if price_to:
            self.object_list = self.object_list.filter(price__lte=price_to)

        #self.object_list = self.object_list.select_related("user").prefetch_related("skills").order_by('text')
        self.object_list = self.object_list.order_by("-price")

        page_number = request.GET.get('page', 1)
        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_obj = paginator.get_page(page_number)

        ads = []
        for ad in page_obj:
            ads.append({
                'id': ad.id,
                'name': ad.name,
                "author": ad.author.username,
                "price": ad.price,
                'description': ad.description,
                'is_published': ad.is_published,
                'category': ad.category.name,
                'image': ad.image.url if ad.image else None
            })
        response = {
            "num_pages": paginator.num_pages,
            "total": paginator.count,
            "items": ads
        }

        return JsonResponse(response, safe=False)


class AdDetailView(DetailView):
    model = Ad

    def get(self, *args, **kwargs):
        ad = self.get_object()

        return JsonResponse({
            'id': ad.id,
            'name': ad.name,
            "author": ad.author.username,
            "price": ad.price,
            'description': ad.description,
            'is_published': ad.is_published,
            'category': ad.category.name,
            'image': ad.image.url if ad.image else None
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(CreateView):
    model = Ad
    fields = ['name', 'author', 'price', 'description', 'is_published', 'category', 'image']

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)

        ad = Ad.objects.create(
            name=ad_data["name"],
            price=ad_data["price"],
            description=ad_data["description"],
            is_published=ad_data["is_published"],
        )
        ad.author = get_object_or_404(User, pk=ad_data["author_id"])
        ad.category = get_object_or_404(Category, pk=ad_data['category_id'])
        ad.save()

        return JsonResponse({
            'id': ad.id,
            'name': ad.name,
            "author": ad.author.username,
            "price": ad.price,
            'description': ad.description,
            'is_published': ad.is_published,
            'category': ad.category.name,
            'image': ad.image.url if ad.image else None
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdUpdateView(UpdateView):
    model = Ad
    fields = ['name', 'price', 'description', 'category']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)
        self.object.name = ad_data["name"]
        self.object.author_id = ad_data["author_id"]
        self.object.price = ad_data["price"]
        self.object.description = ad_data["description"]
        self.object.category_id = ad_data["category_id"]

        self.object.save()

        return JsonResponse({
            'id':  self.object.id,
            'name':  self.object.name,
            "author":  self.object.author.username,
            "price":  self.object.price,
            'description':  self.object.description,
            'is_published':  self.object.is_published,
            'category':  self.object.category.name,
            'image':  self.object.image.url if self.object.image else None
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdImageView(UpdateView):
    model = Ad
    fields = ['name', 'image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES["image"]
        self.object.save()

        return JsonResponse({
            'id':  self.object.id,
            'name':  self.object.name,
            "author":  self.object.author.username,
            "price":  self.object.price,
            'description':  self.object.description,
            'is_published':  self.object.is_published,
            'category':  self.object.category.name,
            'image':  self.object.image.url if self.object.image else None
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


# ------------------- Category views ---------------------
class CatListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by("name")

        cats = []
        for cat in self.object_list:
            cats.append({
                "id": cat.id,
                "name": cat.name
            })

        return JsonResponse(cats, safe=False)


class CatDetailView(DetailView):
    model = Category

    def get(self, *args, **kwargs):
        cat = self.get_object()

        return JsonResponse({
            "id": cat.id,
            "name": cat.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class CatCreateView(CreateView):
    model = Category
    fields = ['user']

    def post(self, request, *args, **kwargs):
        cat_data = json.loads(request.body)

        cat = Category.objects.create(
            name=cat_data["name"]
        )

        return JsonResponse({
            "id": cat.id,
            "name": cat.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class CatUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        cat_data = json.loads(request.body)
        self.object.name = cat_data["name"]
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class CatDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


# ------------------- User views ---------------------
class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDestroySerializer

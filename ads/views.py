import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView

from ads.models import Ad, Category, User
from csv_to_json_ad import csv_to_json
from skypro_django_hw1 import settings


def root(request):

    return JsonResponse({"status": "ok"}, status=200)
#    return JsonResponse(csv_to_json('./ads.csv'), safe=False, status=200)


class AdListView(ListView):
    model = Ad
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        search_text = request.GET.get("text", None)
        if search_text:
            self.object_list = self.object_list.filter(name=search_text)

        #self.object_list = self.object_list.select_related("user").prefetch_related("skills").order_by('text')

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
            "items": ads,
            "num_pages": paginator.num_pages,
            "total": paginator.count
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
        self.object.price = ad_data["price"]
        self.object.description = ad_data["description"]
        self.object.category = ad_data["category"]


        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            "slug": self.object.slug,
            'text': self.object.text,
            'status': self.object.status,
            'created': self.object.created,
            'user': self.object.user_id,
            'skills': list(self.object.skills.all().values_list('name', flat=True))
        })

@method_decorator(csrf_exempt, name='dispatch')
class AdView(View):
    def get(self, request):
        ads = Ad.objects.all()

        response = []
        for ad in ads:
            response.append({
                "id": ad.id,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price,
                "description": ad.description,
                "address": ad.address,
                "is_published": ad.is_published
            })
        return JsonResponse(response, safe=False)

    def post(self, request):
        ad_data = json.loads(request.body)

        ad = Ad()
        ad.name = ad_data["name"]
        ad.author = ad_data["author"]
        ad.price = ad_data["price"]
        ad.description = ad_data["description"]
        ad.address = ad_data["address"]
        ad.is_published = ad_data["is_published"]

        ad.save()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published
        })


@method_decorator(csrf_exempt, name='dispatch')
class CatView(View):

    def get(self, request):
        cats = Category.objects.all()

        response = []
        for cat in cats:
            response.append({
                "id": cat.id,
                "name": cat.name
            })

        return JsonResponse(response, safe=False)

    def post(self, request):
        cat_data = json.loads(request.body)

        cat = Category()
        cat.name = cat_data["name"]

        cat.save()

        return JsonResponse({
            "id": cat.id,
            "name": cat.name
        })


class CatDetailView(DetailView):
    model = Category

    def get(self, *args, **kwargs):
        cat = self.get_object()

        return JsonResponse({
            "id": cat.id,
            "name": cat.name
        })

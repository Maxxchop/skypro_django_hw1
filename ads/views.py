from django.http import JsonResponse
from django.shortcuts import render

from my_csv import csv_to_json


def root(request):

#    return JsonResponse({"status": "ok"}, status=200)
    return JsonResponse(csv_to_json('./ads.csv'), safe=False, status=200)


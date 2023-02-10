from django.shortcuts import render
from django.http import HttpResponse


def barcode_lookup(request):
    HttpResponse(render(request, 'BCscanner/scanner.html'))




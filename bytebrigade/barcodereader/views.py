from django.shortcuts import render
from django.http import HttpResponse


def barcode_lookup(request):
    return HttpResponse(render(request, 'BCscanner/scanner.html'))




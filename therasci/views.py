from django.http import JsonResponse
from django.views import View
from .main import data_scraping


class ScrapRasci(View):

    def get(self, request,*args, **kwargs):
        if request.GET.get('value') is not None:
            try:
                data = data_scraping(str(request.GET.get('value')))
                return JsonResponse({"data":data, "success":True, "error":None, "message": "data scrapped successfully"})
            except Exception as e:
                return JsonResponse({"data":[], "success":False, "error":str(e), "message":"there is error in scraping"})
        return JsonResponse({"data":[], "success":False, "error":None, "message":"value was not found in api url"})
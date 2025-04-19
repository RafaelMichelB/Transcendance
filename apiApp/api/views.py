from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import cache
from django.http import JsonResponse
import sys
# Create your views here.

print("VIEW IMPORTEEE", file=sys.stderr)
def getSimulationState(request):

    apikey = request.GET.get('apikey')
    print(f"[DEBUG] API Key reçue : {apikey}", file=sys.stderr)
    
    if not apikey:
        return JsonResponse({'error': 'API key manquante'}, status=400)
    
    data = cache.get(f'simulation_state_{apikey}')
    print(f"[DEBUG] Données récupérées du cache : {data}", file=sys.stderr)
    
    if data:
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Simulation introuvable'}, status=404)
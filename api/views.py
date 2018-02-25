from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from trades.models import Contract, Trade
from django.utils.translation import gettext as _
from django.core import serializers

def index(request):
    return HttpResponse(_("Estás en la API, por favor ejecuta un método concreto."))

'''
summary of all the contracts already registered
'''
def contracts(request):
    contracts = Contract.objects.all().values();#.filter();
    aContracts = [];
    for contract in contracts:
        aContracts.append(contract);
    return JsonResponse({"contracts": aContracts})

'''
contract detail containing some statistics about its trades
'''
def contract(request, address):
    contract = get_object_or_404(Contract, address=address);
    oTrades = get_trades(contract);
    oContract = {
        "min": oTrades["min"],
        "max": oTrades["max"],
        "avg": oTrades["avg"],
    };
    response = JsonResponse(oContract);
    response['Access-Control-Allow-Origin'] = "*";
    return response;

def trim_trailing(value):
    s = str(value);
    return s.rstrip('0').rstrip('.') if '.' in s else s

'''
gets all the trades of a token
and some statistics among them
'''
def trades(request, address):
    contract = get_object_or_404(Contract, address=address)
            
    return JsonResponse(get_trades(contract), content_type="application/json");
    #trades =Trade.objects.filter(address=address).values();
'''

@param contract: Contract object
@return: object with the trades 
'''   
def get_trades(contract):
    trades = contract.trade_set.all().values();
    aTrades = [];
    minPrice = 0;
    maxPrice = 0;
    count = 0;
    total = 0;
    for oTrade in trades:
        trade = Trade.objects.get(id=oTrade["id"])
        oTrade["cheapest"] = trade.is_the_cheapest();
        aTrades.append(oTrade);
        if minPrice==0 or minPrice>oTrade["price"]:
            minPrice = oTrade["price"];
        if maxPrice==0 or maxPrice<oTrade["price"]:
            maxPrice = oTrade["price"];
        total += oTrade["price"];
        count +=1;
    
    return {
        "trades": aTrades,
        "min": trim_trailing(minPrice),
        "max": trim_trailing(maxPrice),
        "avg": trim_trailing(total/count)
    }

from django.utils.translation import gettext as _
from django.db import models

'''
Blockchain contract for the intended trade
Here we can index its workflow (pendent, validated,...)
'''    
class Contract(models.Model):
    CONTRACT_STATUS = (
        ('P', _('Pendent')),
        ('V', _('Validated')),
    )
    address = models.CharField(
        _('contract address'),
        max_length=200, 
        primary_key = True, 
        help_text = _('unique address for the contract within the blockchain')
    )
    ticker = models.CharField(
        _('coin code'),
        null = True,
        max_length = 10,
        help_text = _('to be filled once utility contract reviewed, please see the coin code')
    )
    name = models.CharField(
        _('coin name'),
        null = True,
        max_length = 128,
        help_text = _('to be filled once utility contract reviewed, please see the coin name')
    )
    status = models.CharField(
        _('contract status'),
        default = 'P',
        max_length=1, 
        choices=CONTRACT_STATUS,
        help_text = _('informs about the validity of the contract')
    )
    date_creation = models.DateTimeField(
        _('date creation'),
        auto_now_add=True
    )
    date_update = models.DateTimeField(
        _('date update'),
        auto_now=True
    )
    
    def __str__(self):
        return self.name
    
    def get_by_natural_key(self):
        return self.address
    
class Trade(models.Model):
    address = models.CharField(max_length=200)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    price = models.DecimalField(
        decimal_places = 24,
        max_digits = 34,
        help_text = _('how many ethers per coin'),
    )
    date_creation = models.DateTimeField(
        _('date creation'),
        auto_now_add=True
    )
    
    def __str__(self):
        return self.address
    
    def get_natural_key(self, address):
        return self.get(address=address)
    
    def get_by_natural_key(self, address):
        return self.get(address=address)
    
    
    def natural_key(self, address):
        return self.get(address=address)
    
    def save(self, *args, **kwargs):
        '''
        TODO verificar que no se repita address + contract
        '''
        super().save(*args, **kwargs)  # Call the "real" save() method.
    '''
    Let's see if this trade is the cheapest of its contract
    '''
    def is_the_cheapest(self):
        
        trades = Trade.objects.filter(contract = self.contract).order_by('price', 'date_creation')
        for item in trades:
            if (item.price<self.price):
                return False
            else:
                if item.price==self.price:
                    if item.date_creation<self.date_creation:
                        return False
                    else:
                        return True
        
        
        return False
    
    is_the_cheapest.boolean = True

'''    
class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__' 
'''
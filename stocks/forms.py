from django import forms

from stocks.models import Stock, UserStock
from stocks.tasks import get_stock_info

class StockForm(forms.ModelForm):
    
    class Meta:
        model = Stock
        fields = ('acronym', 'is_brazilian')
        
    def search_stock(self):
        acronym = self.data['acronym'].upper()
        is_brazilian = True
        
        try:
            stock_db = Stock.objects.get(acronym=acronym)
        except Stock.DoesNotExist:
            stock_db = None
            
        if stock_db is not None:
            return None, stock_db

        stock_name = get_stock_info(acronym, is_brazilian)
        if stock_name is None:
            return "Ativo não encontrado!", stock_name
        
        stock = Stock()
        stock.acronym = acronym
        stock.is_brazilian = True
        stock.name = stock_name
        
        return None, stock

class UserStockForm(forms.ModelForm):
    
    class Meta:
        model = UserStock
        fields = ('max_price', 'min_price',  'update_frequency')
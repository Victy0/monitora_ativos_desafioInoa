from django import forms

from stocks.models import Stock, UserStock

class StockForm(forms.ModelForm):
    
    class Meta:
        model = Stock
        fields = ('acronym', 'is_brazilian')
        
    def search_stock(self):
        acronym = self.data['acronym']
        try:
            stock_db = Stock.objects.get(acronym=acronym)
        except Stock.DoesNotExist:
            stock_db = None
            
        if stock_db is not None:
            return None, stock_db
        
        # Procurar se ativo existe pela API
        return "Consumo da API não implementado!", stock_db

class UserStockForm(forms.ModelForm):
    
    class Meta:
        model = UserStock
        fields = ('max_price', 'min_price',  'update_frequency')
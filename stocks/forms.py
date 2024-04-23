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
            
        stock_name, current_price = get_stock_info(acronym, is_brazilian)
            
        if stock_db is not None:
            return None, stock_db, current_price

        if stock_name is None:
            return "Ativo não encontrado!", None, None
        
        stock = Stock()
        stock.acronym = acronym
        stock.is_brazilian = True
        stock.name = stock_name
        
        return None, stock, current_price

class UserStockForm(forms.ModelForm):
    
    class Meta:
        model = UserStock
        fields = ('max_price', 'min_price',  'update_frequency')
        
    def validate_data(self):
        max_price = self.data['max_price']
        min_price = self.data['min_price']
        update_frequency = self.data['update_frequency']
        
        if max_price is None:
            return "Limite Máximo precisa ser preenchido!"
        if min_price is None:
            return "Limite Mínimo precisa ser preenchido!"
        if update_frequency is None:
            return "Periodicidade precisa ser preenchido!"
        
        if float(min_price) >= float(max_price):
            return "Valor do Limite Mínimo precisa ser menor que valor do Limite Máximo!"
        
        return None
    
    def translate_model_to_form_edit(user_stock):
        form = UserStockForm()
        form.data['max_price'] = str(user_stock.max_price)
        form.data['min_price'] = str(user_stock.min_price)
        form.data['update_frequency'] = str(user_stock.update_frequency)
        
        current_price = get_stock_info(user_stock.stock.acronym, True)[1]
        
        return form, current_price
from django.db import models
from django.utils import timezone
from django.utils.dateformat import format
from django.utils.translation import gettext_lazy as _

from users.models import User


class Stock(models.Model):
    id_stock = models.AutoField(_("identificador do registro de ativo"), primary_key=True)
    name = models.CharField(_("nome do ativo"), max_length=50)
    acronym = models.CharField(_("sigla do ativo"), max_length=10, unique=True)
    is_brazilian = models.BooleanField(_("indicativo se ativo é brasileiro"), default=True)
    creation_date = models.DateTimeField(_("data de criação do registro de ativo no sistema"), default=timezone.now)
    
    class Meta:
        db_table = "stock"
        
    def __str__(self):
        return self.name + '(' + self.acronym + ')'
    
    def serialize_stock_for_create(self):
        return {
            'id_stock': self.id_stock,
            'name': self.name,
            'acronym': self.acronym,
            'is_brazilian': self.is_brazilian
        }
    
    @staticmethod
    def get_created_or_create(stock_params):
        if stock_params['id_stock'] is not None:
            return Stock.objects.get(id_stock=stock_params['id_stock'])
        
        stock = Stock()
        stock.acronym = stock_params['acronym']
        stock.name = stock_params['name']
        stock.is_brazilian = True
        stock.save()
        
        return stock
    
class UserStock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, db_index=True)
    max_price = models.DecimalField(_("valor máximo do túnel estático definido pelo usuário"), max_digits=10, decimal_places=2, default=0)
    min_price = models.DecimalField(_("valor mínimo do túnel estático definido pelo usuário"), max_digits=10, decimal_places=2, default=0)
    update_frequency = models.IntegerField(_("frequencia em minutos de atualização dos dados do ativo definido pelo usuário"), default=0)
    update_date = models.DateTimeField(_("data de criação/atualização do registro"), default=timezone.now)
    
    class Meta:
        db_table = "user_stock"
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'stock'], name='unique_user_stock_combination'
            )
        ]
        
    def __str__(self):
        return '(Usuário: ' + str(self.user.email) + '; Ativo: ' + str(self.stock.acronym) + ')'
    
    def update_register(self, form):
        self.max_price = form.data['max_price']
        self.min_price = form.data['min_price']
        if self.update_frequency != form.data['update_frequency']:
            if not UserStock.objects.filter(stock=self.stock, update_frequency=self.update_frequency, update_date__lt=self.update_date).exists():
                PriceQuoteHistory.objects.filter(stock=self.stock, update_frequency=self.update_frequency, update_date__lte=self.update_date).delete()
            self.update_date = timezone.now().isoformat()
        self.update_frequency = form.data['update_frequency']
        self.save()
    
    @staticmethod
    def get_options_to_update_frequency():
        return ['3', '5', '15', '30', '60']
    
    @staticmethod
    def translate_form_to_model(form):
        user_stock = UserStock()
        user_stock.max_price = form.data['max_price']
        user_stock.min_price = form.data['min_price']
        user_stock.update_frequency = int(form.data['update_frequency'])
        return user_stock
    
    @staticmethod
    def exists_register(user, stock):
        if UserStock.objects.filter(user=user, stock=stock).exists():
            return True
        return False
    
class PriceQuoteHistory(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    price_quote = models.DecimalField(_("preço da cotação no momento da monitorização"), max_digits=10, decimal_places=2, default=0)
    creation_date = models.DateTimeField(_("data de criação do registro de cotação monitorada"), default=timezone.now)
    update_date = models.DateTimeField(_("data de atualização do registro em caso de não alteração da cotação monitorada desde último monitoramento"), default=timezone.now)
    update_frequency = models.IntegerField(_("frequencia em minutos de atualização dos dados da cotação"), null=True)
    
    class Meta:
        db_table = "price_quote_history"
        constraints = [
            models.UniqueConstraint(
                fields=['stock', 'creation_date'], name='unique_stock_creation_date_combination'
            )
        ]
        
    def __str__(self):
        return '(Ativo: ' + str(self.id_stock) + ';' + 'Data:' + format(self.creation_date, 'DD/MM/YYYY %H:%M') + ')'
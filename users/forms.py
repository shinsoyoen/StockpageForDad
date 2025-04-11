from django import forms
from .models import TransactionHistory

class TransactionForm(forms.ModelForm):
    TYPE_CHOICES = [
        ('매매', '매매'),
        ('매도', '매도'),
    ]

    category = forms.ChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.Select(attrs={ 'class': 'form-select','id': 'category','required': True,
        })
    )

    class Meta:
        model = TransactionHistory
        fields = ['category','trans_date','price', 'quantity','memo'] 
        widgets = {
            'price': forms.TextInput(attrs={'class': 'form-control','required': True,'placeholder': '숫자를 입력하세요.', 'id': 'price'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control','required': True,'placeholder': '숫자를 입력하세요.', 'id': 'quantity'}),
            'memo': forms.Textarea(attrs={'class': 'form-control','required': False,'placeholder': '메모를 작성하세요.','rows': 3,'id': 'memo'}),
            'trans_date': forms.HiddenInput(),
        }

    def clean_price(self):
        raw_price = self.cleaned_data.get('price', '')
        price = str(raw_price).replace(',', '')
        if not price.isdigit():
            raise forms.ValidationError('숫자만 입력해주세요.')
        return int(price)

    def clean_quantity(self):
        raw_quantity = self.cleaned_data.get('quantity', '')
        quantity = str(raw_quantity).replace(',', '')
        if not quantity.isdigit():
            raise forms.ValidationError('숫자만 입력해주세요.')
        return int(quantity)

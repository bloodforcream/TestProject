from django.shortcuts import render

from core.forms import TransferForm
from core.tools import transfer_to_inn


def home(request):
    context = {}
    if request.method == 'GET':
        transferform = TransferForm()
        transferform.set_users_choices()
        context['transferform'] = transferform
        return render(request, 'core/home.html', context)

    else:
        transferform = TransferForm(request.POST)
        transferform.set_users_choices()
        if transferform.is_valid():
            data = transferform.cleaned_data
            response = transfer_to_inn(data)
            context['response'] = response
        context['transferform'] = transferform
        return render(request, 'core/home.html', context)

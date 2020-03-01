from django.shortcuts import render

from core.forms import TransferForm
from core.tools import transfer_to_inn


def home(request):
    context = {}
    if request.method == 'GET':
        transfer_form = TransferForm()
        context['transfer_form'] = transfer_form
        return render(request, 'core/home.html', context)

    else:
        transfer_form = TransferForm(request.POST)
        if transfer_form.is_valid():
            data = transfer_form.cleaned_data
            response = transfer_to_inn(data)
            context['response'] = response
        context['transfer_form'] = TransferForm()
        return render(request, 'core/home.html', context)

from django.shortcuts import render, get_object_or_404
from .models import Service, ServiceCategory


def services_list(request):
    category_id = request.GET.get('cat', '')
    services = Service.objects.filter(is_active=True).select_related('category')
    if category_id:
        services = services.filter(category_id=category_id)
    categories = ServiceCategory.objects.all()
    return render(request, 'services/list.html', {
        'services': services,
        'categories': categories,
        'selected_cat': category_id,
    })


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk, is_active=True)
    doctors = service.doctors.filter(is_active=True)
    return render(request, 'services/detail.html', {
        'service': service,
        'doctors': doctors,
    })

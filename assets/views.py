from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum,Avg,Count,F, Q
from django.contrib.auth.mixins import LoginRequiredMixin

from assets.models import Asset, Department, User, MaintenanceLog
from assets.mixins import ManagerOrAdminRequiredMixin
from assets.forms import CustomCreationForm


class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = "assets/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        
        total_cost = Asset.objects.aggregate(total=Sum('cost'))['total'] or 0
        context['total_asset_value'] = total_cost

       
        context['assets_by_type'] = Asset.objects.values('asset_type').annotate(count=Count('id'))

        cost_by_department = Department.objects.annotate(total_cost=Sum('departments__assets__cost'))
        context['costs'] = cost_by_department

        
        return context

class AssetListView(LoginRequiredMixin, ListView):
    model = Asset
    template_name = "assets/asset_list.html"
    context_object_name = "assets"
    paginate_by = 5

    def get_queryset(self):
        querySet = Asset.objects.select_related('assigned_to').all().annotate(repair_total=Sum('maintenance_logs__cost'))

        asset_type = self.request.GET.get('asset_type')
        search_query = self.request.GET.get('search')

        if asset_type:
            querySet = querySet.filter(asset_type=asset_type)

        if search_query:
            querySet = querySet.filter(
                Q(name__icontains=search_query)|
                Q(assigned_to__username__icontains=search_query)
            )
        
        return querySet
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        params = self.request.GET.copy()
        params.pop('page', None)
        context['query_string'] = params.urlencode()
        context['asset_types'] = Asset.ASSET_TYPES
        return context   
       
class MaintenanceCreateView(CreateView):
    model = MaintenanceLog
    template_name = "assets/maintenance_form.html"
    fields = ['description', 'cost', 'date_repaired']

    def form_valid(self, form):
        asset = Asset.objects.get(pk=self.kwargs['pk'])
        form.instance.asset = asset
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'asset_maintenance_logs',
            kwargs={'pk': self.kwargs['pk']}
        )
    
class AssetCreateView(ManagerOrAdminRequiredMixin,CreateView):
    model = Asset
    template_name = "assets/asset_form.html"
    fields = ['name', 'asset_type', 'cost', 'assigned_to']
    success_url = reverse_lazy('asset-list')

    def form_valid(self, form):
        print(f"Creating asset: {form.instance.name}")
        return super().form_valid(form)

class SignUpView(ManagerOrAdminRequiredMixin,CreateView):
    form_class = CustomCreationForm
    success_url = reverse_lazy('dashboard')
    template_name = "registration/register.html"

class AssetUpdateView(ManagerOrAdminRequiredMixin,UpdateView):
    model = Asset
    template_name = "assets/asset_form.html"
    fields = ['name', 'asset_type', 'cost', 'assigned_to']
    success_url = reverse_lazy('asset-list')


class AssetDeleteView(ManagerOrAdminRequiredMixin, DeleteView):
    model = Asset
    template_name = "assets/asset_confirm_delete.html"
    success_url = reverse_lazy('asset-list')

class AssetMaintenanceView(ManagerOrAdminRequiredMixin, ListView):
     template_name = "assets/asset_maintenance_logs.html"
     context_object_name = "maintenance_records"

     def get_queryset(self):
         asset  = get_object_or_404(Asset, pk=self.kwargs['pk'])
         return asset.maintenance_logs.all()
     
     def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         context['asset'] = get_object_or_404(Asset, pk=self.kwargs['pk'])
         return context

class AssetHistoryView(ManagerOrAdminRequiredMixin, ListView):
     template_name = "assets/asset_history.html"
     context_object_name = "history_records"

     def get_queryset(self):
         asset  = get_object_or_404(Asset, pk=self.kwargs['pk'])
         return asset.history.all()
     
     def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         context['asset'] = get_object_or_404(Asset, pk=self.kwargs['pk'])
         return context
    
class AssetRevertView(ManagerOrAdminRequiredMixin, View):
     def post(self, request, pk, history_id):
         asset = get_object_or_404(Asset, pk=pk)
         historical_record = get_object_or_404(asset.history.model, history_id=history_id)
         historical_record.instance.save()
         messages.success(request, f"Asset Successfully Reverted to the state from {historical_record.history_date}.")
         return redirect('asset_history', pk=pk)
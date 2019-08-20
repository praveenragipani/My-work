from asset_mgmt.models import (AssetCatalog, CONTENT_TYPES, TableauServer, TableauSite, BusinessArea, AlteryxStudio,
                               User, DataSource, BusinessCapability, LineOfBusiness, UserProfile, AssetType,
                               AnalyticType, AnalyticFocus, UtilizationCategory, ProviderFocus)
from django import forms
from django.db.models import Q
import django_filters


class AssetFilter(django_filters.FilterSet):
    asset_type = django_filters.ModelChoiceFilter(queryset=AssetType.objects.all(), widget=forms.Select(attrs={'class': "ui fluid search selection dropdown"}))
    product_business = django_filters.ModelMultipleChoiceFilter(queryset=LineOfBusiness.objects.all(), widget=forms.SelectMultiple(attrs={'class': "ui fluid search dropdown"}))
    asset_developer = django_filters.ModelChoiceFilter(queryset=UserProfile.objects.filter(bcbsnc_user__is_superuser=False), widget=forms.Select(attrs={'class': "ui fluid search selection dropdown"}))
    business_owner = django_filters.ModelChoiceFilter(queryset=UserProfile.objects.filter(bcbsnc_user__is_superuser=False), widget=forms.Select(attrs={'class': "ui fluid search selection dropdown"}))
    business_area = django_filters.ModelChoiceFilter(queryset=BusinessArea.objects.all(), widget=forms.Select(attrs={'class': "ui fluid search selection dropdown"}))
    analytic_focus = django_filters.ModelChoiceFilter(queryset=AnalyticFocus.objects.all(), widget=forms.Select(attrs={'class': "ui fluid search selection dropdown"}))
    provider_focus = django_filters.ModelChoiceFilter(queryset=ProviderFocus.objects.all(), widget=forms.Select(attrs={'class': "ui fluid search selection dropdown"}))
    analytic_type = django_filters.ModelChoiceFilter(queryset=AnalyticType.objects.all(), widget=forms.Select(attrs={'class': "ui fluid search selection dropdown"}))
    utilization_category = django_filters.ModelMultipleChoiceFilter(queryset=UtilizationCategory.objects.all(), widget=forms.SelectMultiple(attrs={'class': "ui fluid search dropdown"}))

    asset_server = django_filters.ModelChoiceFilter(queryset=TableauServer.objects.all(), widget=forms.Select(attrs={'class': "ui fluid search selection dropdown"}))
    asset_site = django_filters.ModelChoiceFilter(queryset=TableauSite.objects.all(), widget=forms.Select(attrs={'class': "ui fluid search selection dropdown"}))
    asset_studio = django_filters.ModelChoiceFilter(queryset=AlteryxStudio.objects.all(), widget=forms.Select(attrs={'class': "ui fluid search selection dropdown"}))
    content_type = django_filters.ChoiceFilter(choices=CONTENT_TYPES, widget=forms.Select(attrs={'class': "ui fluid search selection dropdown"}))
    data_source = django_filters.ModelMultipleChoiceFilter(queryset=DataSource.objects.all(), widget=forms.SelectMultiple(attrs={'class': "ui fluid search dropdown"}))
    capability_business = django_filters.ModelMultipleChoiceFilter(queryset=BusinessCapability.objects.all(), widget=forms.SelectMultiple(attrs={'class': "ui fluid search dropdown"}))

    class Meta:
        model = AssetCatalog
        fields = ['content_type', 'asset_server', 'asset_site', 'asset_studio', 'asset_developer',
                  'business_area', 'data_source', 'product_business', 'capability_business', 'business_owner',
                  'analytic_focus', 'provider_focus', 'analytic_type', 'utilization_category']

    @property
    def qs(self):
        parent = super(AssetFilter, self).qs
        return parent.filter(asset_active=True)

    @property
    def total(self):
        parent = super(AssetFilter, self).qs
        parent = parent.filter(asset_active=True)
        return parent.count()
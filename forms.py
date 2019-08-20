from django import forms
from asset_mgmt.models import AssetCatalog, BusinessArea, AnalyticFocus, ProviderFocus


class AssetEditForm(forms.ModelForm):
    business_area = forms.ModelChoiceField(queryset=BusinessArea.objects.all(), empty_label=None, required=False,
                                           label="Business Process Area")
    analytic_focus = forms.ModelChoiceField(queryset=AnalyticFocus.objects.all(), empty_label=None, required=False,
                                           label="Analytic Focus")
    provider_focus = forms.ModelChoiceField(queryset=ProviderFocus.objects.all(), empty_label=None, required=False,
                                           label="Provider Program")

    class Meta:
        model = AssetCatalog
        fields = ['description', 'business_area', 'product_business', 'business_owner', 'analytic_focus',
                  'provider_focus', 'analytic_type', 'utilization_category', 'repo_location',
                  'doc_location', 'asset_active']
        widgets = {
            'product_business': forms.SelectMultiple(attrs={'class': "ui fluid search dropdown"}),
            'utilization_category': forms.SelectMultiple(attrs={'class': "ui fluid search dropdown"}),
            'business_area': forms.Select(attrs={'class': "ui fluid search selection dropdown"}),
            'business_owner': forms.Select(attrs={'class': "ui fluid search selection dropdown"}),
            'analytic_focus': forms.Select(attrs={'class': "ui fluid search selection dropdown"}),
            'provider_focus': forms.Select(attrs={'class': "ui fluid search selection dropdown"}),
            'analytic_type': forms.Select(attrs={'class': "ui fluid search selection dropdown"}),
            'asset_active': forms.CheckboxInput(attrs={'class': "ui toggle checkbox"}),
            'description': forms.Textarea(attrs={'rows': 8}),
        }

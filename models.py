from django.db import models
from bcbsnc_mgmt.models import (User, TableauServer, TableauSite, AlteryxStudio, BusinessCapability, BusinessArea,
                                LineOfBusiness, DataSource, AssetType, UserProfile, AnalyticType, AnalyticFocus,
                                ProviderFocus, UtilizationCategory)
import datetime

# Create your models here.
CONTENT_TYPES = (
    ('Alteryx App', 'Alteryx App'),
    ('Alteryx Workflow', 'Alteryx Workflow')
)


class AssetCatalog(models.Model):
    """
    Asset (Information Products)
    """
    name = models.CharField('Information Product', max_length=100)
    description = models.TextField('Description', blank=True, default='', null=True)
    asset_type = models.ForeignKey(AssetType, verbose_name='Type', null=True, blank=True, on_delete=models.SET_NULL)
    asset_id = models.CharField('Product ID', max_length=100, blank=True, default='')
    content_type = models.CharField('Content Type', max_length=20, choices=CONTENT_TYPES, blank=True, default='')
    asset_server = models.ForeignKey(TableauServer, verbose_name='Server', null=True, blank=True, on_delete=models.SET_NULL)
    asset_site = models.ForeignKey(TableauSite, verbose_name='Site', null=True, blank=True, on_delete=models.SET_NULL, related_name='site_assets')
    asset_studio = models.ForeignKey(AlteryxStudio, verbose_name='Studio', null=True, blank=True, on_delete=models.SET_NULL, related_name='studio_assets')
    asset_developer = models.ForeignKey(UserProfile, null=True, verbose_name='Developer', blank=True, on_delete=models.SET_NULL, related_name='develop_asset')
    project_name = models.CharField('Project', max_length=100, blank=True)
    asset_url = models.URLField('URL', blank=True)
    image_url = models.CharField('Preview Image', max_length=100, blank=True)
    use_count = models.PositiveIntegerField('Run or Views', default=0)
    asset_status = models.CharField('Status', max_length=50, blank=True, default='New')
    created_at = models.DateField('Created', null=True, default=datetime.date.today)
    modified_at = models.DateField('Modified', null=True, default=datetime.date.today)
    published_at = models.DateField('Published', null=True, default=datetime.date.today)
    content_id = models.PositiveIntegerField('Content ID', null=True, default=0)
    business_area = models.ForeignKey(BusinessArea, verbose_name='Business Process Area', related_name='bparea_asset', blank=True, null=True, on_delete=models.SET_NULL)
    data_source = models.ManyToManyField(DataSource, verbose_name='Data Source', related_name='source_asset', blank=True)
    product_business = models.ManyToManyField(LineOfBusiness, verbose_name='Line of Business', related_name='group_asset', blank=True)
    capability_business = models.ManyToManyField(BusinessCapability, verbose_name='Capability', related_name='capability_asset', blank=True)
    business_owner = models.ForeignKey(UserProfile, null=True, verbose_name='Business Owner', blank=True, on_delete=models.SET_NULL, related_name='owner_assets')
    repo_location = models.CharField('Repository', max_length=150, blank=True, default='')
    doc_location = models.CharField('Documentation', max_length=150, blank=True, default='')
    jira_location = models.CharField('JIRA Ticket', max_length=150, blank=True, default='')
    analytic_focus = models.ForeignKey(AnalyticFocus, null=True, verbose_name='Analytic Focus Area', blank=True, on_delete=models.SET_NULL, related_name='analyticarea_asset')
    provider_focus = models.ForeignKey(ProviderFocus, null=True, verbose_name='Provider Program', blank=True, on_delete=models.SET_NULL, related_name='provider_asset')
    analytic_type = models.ForeignKey(AnalyticType, null=True, verbose_name='Analytic Type', blank=True, on_delete=models.SET_NULL, related_name='analytictype_asset')
    utilization_category = models.ManyToManyField(UtilizationCategory, verbose_name='Utilization Category', related_name='utilization_asset', blank=True)
    asset_active = models.BooleanField('Active', default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-use_count']
        verbose_name = 'Information Product'



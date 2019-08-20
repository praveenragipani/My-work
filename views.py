from django.shortcuts import render, get_object_or_404, redirect
from asset_mgmt.models import AssetCatalog, UserProfile
from asset_users.models import AssetUserView, AssetUserFavorite, AssetUserSearch
from asset_mgmt.filters import AssetFilter
from django.db.models import Q
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from asset_mgmt.forms import AssetEditForm
from django.contrib import messages
from datetime import timezone
from django.http.request import QueryDict, MultiValueDict
from asset_catalog.settings import LOGIN_URL
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


# def asset_main(request):
#     return render(request, "asset_mgmt/asset.html")

class AssetDetailView(LoginRequiredMixin, DetailView):
    template_name = 'asset_mgmt/detail.html'
    login_url = LOGIN_URL
    model = AssetCatalog
    context_object_name = 'asset'

    def get_object(self):
        asset = get_object_or_404(AssetCatalog, pk=self.kwargs['pk'])
#        user = UserProfile.objects.all().filter(bcbsnc_user=self.request.user).first()
        user = self.request.user.profile
        view = AssetUserView.objects.filter(user=user, asset=asset)
        if view:
            view.first().delete()

        AssetUserView.objects.create(user=user, asset=asset)
        return asset

    def get_context_data(self, **kwargs):
        context = super(AssetDetailView, self).get_context_data(**kwargs)
        context['now'] = '07/23/2019'
        context['fav'] = AssetUserFavorite.objects.filter(user=self.request.user.profile, asset=self.object).exists()

        return context

    def post(self, request, *args, **kwargs):
        asset = self.get_object()
        self.object = self.get_object()
        context = super(DetailView, self).get_context_data(**kwargs)
        bookmark, created = AssetUserFavorite.objects.get_or_create(user=self.request.user.profile, asset=asset)
        if not created:
            bookmark.delete()
            context['fav'] = False
        else:
            context['fav'] = True

        return self.render_to_response(context=context)


class AssetUpdateView(LoginRequiredMixin, UpdateView):
    model = AssetCatalog
    login_url = LOGIN_URL
    template_name = 'asset_mgmt/update.html'
    form_class = AssetEditForm
    context_object_name = 'asset'

    def form_valid(self, form):
        instance = form.save()
        messages.success(
            self.request, 'Product Update: It has been successfully updated!')
        return redirect('/assets/detail/%s' % instance.pk)


def search(request, search_id=0):
    if not request.user.is_authenticated:
        return redirect(LOGIN_URL)
    query_dict = QueryDict('', mutable=True)
    if search_id and request.GET == query_dict:
        print(request.GET)
        search_text = AssetUserSearch.objects.get(pk=search_id).search_criteria
        search_user = json.loads(search_text)
        for key in list(search_user):
            if search_user[key] == [""]:
                del search_user[key]
        if 'name' in search_user:
            search_user['name'] = search_user['name'][0]
        asset_list = AssetCatalog.objects.all()
        tag_search = search_user.get('name', '')
        if tag_search:
            asset_list = asset_list.filter(Q(name__icontains=tag_search) | Q(description__icontains=tag_search) |
                                           Q(business_area__name__icontains=tag_search) |
                                           Q(product_business__name__icontains=tag_search) |
                                           Q(capability_business__name__icontains=tag_search)).distinct()
        type_asset = ''

        total_assets = asset_list.count()

        query_dict.update(MultiValueDict(search_user))
        asset_filter = AssetFilter(query_dict, queryset=asset_list)

    else:
        asset_list = AssetCatalog.objects.all()
        tag_search = request.GET.get('tag_search', '')
        type_asset = request.GET.get('asset_type', '')
        if tag_search:
            asset_list = asset_list.filter(Q(name__icontains=tag_search) | Q(description__icontains=tag_search) |
                                           Q(business_area__name__icontains=tag_search) |
                                           Q(product_business__name__icontains=tag_search) |
                                           Q(capability_business__name__icontains=tag_search)).distinct()
        total_assets = asset_list.count()
        asset_filter = AssetFilter(request.GET, queryset=asset_list)

    page = request.GET.get('page', 1)

    paginator = Paginator(asset_filter.qs, 30)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'asset_mgmt/asset.html', {'filter': asset_filter, 'product_name': tag_search, 'type_asset': type_asset, 'total': total_assets, 'products': products})


def save_quick_search(request):
    search_name = request.POST.get('search_name', '')
    user_search = {}
    search_filters = {'name', 'product_business', 'business_area', 'analytic_focus', 'provider_focus',
                      'utilization_category'}
    filter_empty = True
    for item in search_filters:
        user_search[item] = list(request.POST.get(item, '').split(','))
        if request.POST.get(item, ''):
            filter_empty = False
    asset_list = AssetCatalog.objects.all()
    total_assets = asset_list.count()
    query_dict = QueryDict('', mutable=True)
    query_dict.update(MultiValueDict(user_search))
    asset_filter = AssetFilter(query_dict, queryset=asset_list)

    if not search_name:
        messages.warning(request, 'Saving QUICK SEARCH: Please, provide a name for this quick search!')

    elif filter_empty:
        messages.warning(request, 'Saving QUICK SEARCH: Please, add some filter to this quick search!')

    else:

        previous_search = AssetUserSearch.objects.filter(name=search_name, user=request.user.profile)
        if previous_search.exists():
            messages.warning(request, 'Saving QUICK SEARCH: You already have a saved search using this name.')
        else:
            search_text = json.dumps(user_search)
            new_search = AssetUserSearch.objects.create(name=search_name, user=request.user.profile, search_criteria=search_text)
            if new_search:
                print('Done')
                messages.success(request, 'Saving QUICK SEARCH: Your search was saved successfully!')

    return render(request, 'asset_mgmt/asset.html', {'filter': asset_filter,
                                                          'product_name': request.POST.get('tag_search', ''),
                                                          'type_asset': '', 'total': total_assets, 'messages': 'OK'})


def get_assets(request):
    if request.is_ajax():
        tag_search = request.GET.get('sea', '')
        assets = AssetCatalog.objects.filter(Q(name__icontains=tag_search) | Q(description__icontains=tag_search))
        assets = assets.filter(asset_active=True)[:10]
        results = {'results': {}}
        print('B')
        for asset in assets:
            category = asset.asset_type.name
            if category.startswith('Alteryx'):
                category = asset.content_type
            if category not in results['results']:
                results['results'][category] = {'name': category, 'results': []}
            asset_json = {}
            asset_json['title'] = asset.name
            asset_json['description'] = asset.description
            asset_json['image'] = ''
            asset_json['url'] = asset.asset_url
            results['results'][category]['results'].append(asset_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'text/json'
    return HttpResponse(data, mimetype)
import datetime as dt
from operator import itemgetter

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext
from django.db.models import Count

from etcetera.reports import models as reports
from etcetera.reports import forms as rpforms
from etcetera.checkout import models as checkout
from etcetera.extras.search import get_query

def incr_item(dict, key):
    try:
        item = dict[key]
    except KeyError:
        item = 0
    dict[key] = item + 1

@login_required
def index(request):
    paged_objects = None
    q = None
    form = rpforms.SearchForm()
    if request.GET and request.GET.get('q'):
        form = rpforms.SearchForm(request.GET)
        if form.is_valid():
            data = form.cleaned_data
            if data['q'] and data['q'].strip() and form.get_list():
                # This sends a query to search middleware, if such
                # query exists. It gets a Q object back which is used
                # in a Django filter to get our queryset.
                report_query = get_query(data['q'], form.get_list())
                paged_objects = reports.Report.objects.filter(
                    report_query
                )
                q = data['q']
    else:
        paged_objects = reports.Report.objects.all()
    # Repackage everything into paged_objects using Paginator.
    paginator = Paginator(paged_objects, 20)
    # Make sure the page request is an int -- if not, then deliver page 1.
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
    # If the page request is out of range, deliver the last page of results.
    try:
        paged_objects = paginator.page(page)
    except (EmptyPage, InvalidPage):
        paged_objects = paginator.page(paginator.num_pages)
    # Bundle everything into the context and send it out.
    context = {
        'paged_objects': paged_objects,
        'object_list': paged_objects.object_list,
        'form': form,
        'q': q,
    }
    return render_to_response(
        "reports/index.html",
        context,
        context_instance=RequestContext(request)
    )

@login_required
def detail(request, slug, view_type='equipmenttypes'):
    if view_type not in ['equipmenttypes','departments',]:
        raise Http404
    annotated_set = None
    # Get our report from the Database!
    rp = get_object_or_404(reports.Report.objects.select_related(), slug=slug)
    # Get our checkouts applicable from the database
    cos = checkout.Checkout.objects.select_related().filter(
        canceled=False).filter(completion_date__range=(
            rp.start_date, rp.end_date)).filter(
        department__in=rp.organizationalunits.all).filter(
        equipment_list__equipment_type__in=rp.equipmenttypes.all)
    # If it's a department page, get annotated set based on above checkouts
    if view_type == 'departments':
        annotated_set = rp.organizationalunits.filter(
            checkouts__in=cos).annotate(
            checkout_count=Count('checkouts'))
            # for ou in rp.organizationlunits:
            # Not really sure what to do here.
    # If it's an equipmenttypes page, get annotated set
    # based on above checkouts
    if view_type == 'equipmenttypes':
        annotated_set = rp.equipmenttypes.filter(
            equipment__checkouts__in=cos).annotate(
            checkout_count=Count('equipment__checkouts'))
    context = {
        'object': rp,
        'view_type': view_type,
        'annotated_set': annotated_set,
    }
    return render_to_response(
        "reports/detail.html",
        context,
        context_instance=RequestContext(request)
    )

@login_required
def edit(request, slug):
    rp = get_object_or_404(reports.Report, slug=slug)
    if request.method == 'POST':
        form = rpforms.ReportModelForm(request.POST, instance=rp)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'reports-detail',
                args=(rp.slug, 'equipmenttypes',),
            ))
    else:
        form = rpforms.ReportModelForm(instance=rp)
    context = {
        'object': rp,
        'form': form,
    }
    return render_to_response(
        "reports/edit.html",
        context,
        context_instance=RequestContext(request)
    )

@login_required
def new(request):
    if request.method == 'POST':
        form = rpforms.ReportModelForm(request.POST)
        if form.is_valid():
            rp = form.save()
            # Assign the user as the created_by person
            rp.created_by = request.user
            rp.save()
            return HttpResponseRedirect(reverse(
                'reports-detail',
                args=(rp.slug, 'equipmenttypes',),
            ))
    else:
        form = rpforms.ReportModelForm()
    context = {
        'form': form,
    }
    return render_to_response(
        "reports/edit.html",
        context,
        context_instance=RequestContext(request)
    )

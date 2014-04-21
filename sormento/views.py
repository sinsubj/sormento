# Create your views here.
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, render_to_response, redirect
from models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from forms import *
from utils import RootMixin, get_by_depth, get_root_list, get_random_m_and_p, get_random
from django.db.models.query import QuerySet
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def home(request):
    context = RequestContext(request)
    root_list = get_root_list(request)
    random_m, random_p = get_random_m_and_p(request)

    return render_to_response('home.html', {'root_list':root_list, 'random_p':random_p, 'random_m':random_m}, context)

def user_login(request):
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Sormento account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    else:
        # No context variables to pass to the template system, hence the blank dictionary object...
        return render_to_response('login.html', {}, context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def root_detail(request, root_slug):
    context = RequestContext(request)
    root = Source.objects.get(slug=root_slug)
    # mementos = root.memento_set.all()
    mementos = Memento.objects.filter(source__root__iexact=root_slug)
    root_list = get_root_list(request)
    nodes = Source.objects.filter(root__istartswith=root_slug)
    random_m, random_p = get_random(nodes)

    context_dict = {'source':root, 'mementos':mementos, 'root_list':root_list, 'nodes':nodes,
                    'random_p':random_p, 'random_m':random_m}
    return render_to_response('root_detail.html', context_dict, context)

@login_required
def source_detail(request, root_slug, source_slug=None):
    context = RequestContext(request)
    source = Source.objects.get(root__istartswith=root_slug, slug=source_slug)
    query = root_slug + " > " + source.title
    nodes = Source.objects.filter(root__istartswith=query)
    root_list = get_root_list(request)
    random_m, random_p = get_random(nodes)

    context_dict = {'nodes':nodes, 'root_list':root_list, 'random_p':random_p, 'random_m':random_m}
    return render_to_response('root_detail.html', context_dict, context)

@login_required
def memento_detail(request, pk):
    context = RequestContext(request)
    memento = Memento.objects.get(pk=pk)
    root_list = get_root_list(request)

    context_dict = {'m':memento, 'root_list':root_list}
    return render_to_response('memento_detail.html', context_dict, context)

@login_required
def add_memento(request, source=None):
    context = RequestContext(request)

    if request.method == 'POST':
        form = MementoForm(request.POST)

        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view. The user will be shown the homepage.
            return home(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = MementoForm()
        if source:
            # http://stackoverflow.com/questions/291945/how-do-i-filter-foreignkey-choices-in-a-django-modelform
            form.fields['source'].queryset = Source.objects.get(slug=source).get_descendants(include_self=True)

    root_list = get_root_list(request)
    # Bad form (or form details), no form supplied; render the form with error messages (if any).
    return render_to_response('add_memento.html', {'form':form, 'root_list':root_list}, context)

@login_required
def edit_memento(request, pk=None):
    context = RequestContext(request)
    memento = Memento.objects.get(pk=pk)

    if request.method == 'POST':
        form = MementoForm(request.POST, instance=memento)

        if form.is_valid():
            form.save(commit=True)
            return home(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = MementoForm(instance=memento)

    root_list = get_root_list(request)
    # Bad form (or form details), no form supplied; render the form with error messages (if any).
    return render_to_response('edit_memento.html', {'form':form, 'pk':pk, 'root_list':root_list}, context)

def node_detail(request, root_slug, node_slug):
    context = RequestContext(request)



#class CategoryCreate(CreateView):
#    model = Category
#    template_name_suffix = '_create_form'
#    success_url = '/smt'
#
#
#class CategoryUpdate(UpdateView):
#    model = Category
#    template_name_suffix = '_create_form'


#class RootAdd(CreateView):
#    form_class = RootForm
#    model = Root
#    template_name_suffix = '_add_form'
#    success_url = '/smt'
#
#    def form_valid(self, form):
#        form.instance.user = self.request.user
#        return super(RootAdd, self).form_valid(form)

#class CategoryDelete(DeleteView):
#    model = Category
#    template_name = 'sormento/source_type_delete_form.html'
#    success_url = 'index'


# def add_source_type(request):
#     # Get the context from the request.
#     context = RequestContext(request)
#
#     # A HTTP POST?
#     if request.method == 'POST':
#         form = CategoryForm(request.POST)
#
#         # Have we been provided with a valid form?
#         if form.is_valid():
#             # Save the new category to the database.
#             form.save(commit=True)
#
#             # Now call the index() view.
#             # The user will be shown the homepage.
#             return HttpResponseRedirect('/sormento/')
#         else:
#             # The supplied form contained errors - just print them to the terminal.
#             print form.errors
#     else:
#         # If the request was not a POST, display the form to enter details.
#         form = CategoryForm()
#
#     # Bad form (or form details), no form supplied...
#     # Render the form with error messages (if any).
#     return render_to_response('sormento/add_source_type.html', {'form': form}, context)


class MementoDetail(RootMixin, DetailView):
    template_name = "sormento/memento_detail.html"
    model = Memento
    context_object_name = "memento"

    #def get_object(self, request, *args, **kwargs):
    #    self.object = get_object_or_404(Source, user=request.user.id,
    #                                    level=0, slug=self.kwargs.get('category'))
    #    #self.object = Source.objects.filter(user=request.user, parent__slug=self.kwargs.get('category'), slug=self.kwargs.get('title'))
    #    return super(CategoryDetail, self).get(self, request, *args, **kwargs)

    #def get_context_data(self, **kwargs):
    #    context = super(CategoryDetail, self).get_context_data(**kwargs)
    #    context['category'] = Source.objects.get(level=0, slug=self.kwargs.get('category'))
    #    return context


class SourceDetail(RootMixin, SingleObjectMixin, ListView):
    template_name = "sormento/source_detail.html"

    def get(self, request, *args, **kwargs):
        if self.kwargs.get('node'):
            self.object = get_object_or_404(Source, user=request.user.id,
                                            parent__slug=self.kwargs.get('root'),
                                            slug=self.kwargs.get('node'))
            self.page_type = "node"
        else:
            self.object = get_object_or_404(Source, user=request.user.id,
                                            slug=self.kwargs.get('root'),
                                            level=0)
            self.page_type = "root"
        return super(SourceDetail, self).get(self, request, *args, **kwargs)

    def get_queryset(self):
        object_list = get_by_depth(1, 3, self.object)
        #if isinstance(object_list, QuerySet):
        #    object_list = {'mementos': object_list}
        return object_list

    def get_context_data(self, **kwargs):
        # the super method adds page_obj, object_list (from get_queryset), paginator, etc. to context
        context = super(SourceDetail, self).get_context_data(**kwargs)
        context['source'] = self.object
        context['page_type'] = self.page_type
        return context


def track_url(request):
    memento_pk = None
    url = '/'
    if request.method == 'GET':
        if 'mem_pk' in request.GET:
            memento_pk = request.GET['mem_pk']
            try:
                memento = Memento.objects.get(pk=memento_pk)
                memento.views += 1
                memento.save()
                url = "/mementos/" + memento_pk
            except:
                pass

    return redirect(url)
    #def get_context_data(self, request, **kwargs):
    #    self.object = get_object_or_404(Root, user=request.user,
    #                                    source_type__name=self.kwargs.get('type'),
    #                                    slug=self.kwargs.get('slug'))
    #    context = super(RootListView, self).get_context_data(**kwargs)
    #    context['sources'] = self.object
    #    return context

#class RootDetail(SingleObjectMixin, ListView):
#    template_name = "sormento/mainsource_detail.html"
#
#    def get(self, request, *args, **kwargs):
#        self.object = get_object_or_404(Root, user=request.user,
#                                        source_type__name=self.kwargs.get('type'),
#                                        slug=self.kwargs.get('slug'))
#        self.object = self.object.source_set.all()
#        return super(RootDetail, self).get(self, request, *args, **kwargs)
#
#    def get_context_data(self, **kwargs):
#        context = super(RootDetail, self).get_context_data(**kwargs)
#        context['sources'] = self.object
#        return context
#
#    def get_queryset(self):
#        return self.object
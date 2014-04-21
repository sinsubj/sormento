#from django.views.generic.base import ContextMixin
from models import Source, Memento
from django.contrib.auth.decorators import login_required
import re, random
from bs4 import BeautifulSoup

class RootMixin(object):

    def get_context_data(self, **kwargs):
        context = super(RootMixin, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context['category_list'] = get_by_depth(0, 0)
        return context

def get_root_list(request):
    root_list = {}
    if request.user.is_authenticated():
        roots = Source.objects.root_nodes()
        for r in roots:
            sources = Source.objects.filter(root__istartswith=r.title, level=1)
            root_list[r] = sources

    return root_list

def get_random_m_and_p(request):
    random_m = []
    random_p = ""
    if request.user.is_authenticated():
        # http://stackoverflow.com/questions/1731346/how-to-get-two-random-records-with-django
        random_m = Memento.objects.order_by('?')[0]
        soup = BeautifulSoup(random_m.text)
        try:
            random_p = unicode(random.choice(soup('p')))
        except:
            random_p = soup.get_text()
    return random_m, random_p

def get_random(sources):
    try:
        random_m = random.choice(sources).memento_set.order_by('?')[0]
        soup = BeautifulSoup(random_m.text)
        random_p = unicode(random.choice(soup('p')))
    except IndexError:
        random_p = ""
        random_m = []
    except:
        random_p = soup.get_text()
    return random_m, random_p

#def get_all(category):
#    root_list = category.root_set.all()
#    root_dict = {}
#
#    for root in root_list:
#        root_dict[root] = get_dict_of_sources_and_mementos(root)
#
#    return root_dict
#
#def get_dict_of_sources_and_mementos(root):
#    # TOOK HOURS TO COME UP WITH THE FOLLOWING FOUR LINES
#    # get a list of all sources and make a blank dictionary
#    source_list = root.source_set.all()
#    source_dict = {}
#
#    for source in source_list:
#        # for every source, fill the dict with (key: value) pairs of (source: mementos)
#        source_dict[source] = source.memento_set.all()
#    # return the dict so that it can be added to context (as "object_list" in case of ListViews)
#
#    return source_dict
#
def get_by_depth(initial, final, parent=None):
    # TOOK HOURS TO COME UP WITH THE FOLLOWING FOUR LINES
    # get a list of all sources and make a blank dictionary

    # How many times we should do recursion:
    num_loops = final - initial

    if parent:
        if parent.is_leaf_node():
            #return parent.memento_set.all()
            return {"mementos": parent.memento_set.all()}
        object_list = parent.get_children()
    else:
        object_list = Source.objects.filter(level=initial)

    object_dict = {}

    for object in object_list:
        # for every source, fill the dict with (key: value) pairs of (source: mementos)
        if num_loops > 0:
            object_dict[object] = get_by_depth(initial+1, final, object)
        else:
            object_dict[object] = object.get_children()

    # return the dict so that it can be added to context (as "object_list" in case of ListViews)
    return object_dict
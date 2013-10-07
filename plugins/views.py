""" Views for the base application """

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.conf import settings

import evaluation_system.api.plugin_manager as pm
from evaluation_system.model.user import User
from evaluation_system.model.solr import SolrFindFiles

from plugins.utils import get_plugin_or_404
from plugins.models import PluginForm, PluginWeb

import urllib, os
import json

@login_required()
def home(request):
    """ Default view for the root """
    
    tools = pm.getPlugins()    
    return render(request, 'plugins/home.html', {'tool_list': tools})

@login_required()
def detail(request, plugin_name):
    
    plugin = get_plugin_or_404(plugin_name)
    plugin_web = PluginWeb(plugin)
    
    return render(request, 'plugins/detail.html', {'plugin':plugin_web})
  
@login_required()    
def setup(request, plugin_name):
    
    plugin = get_plugin_or_404(plugin_name)
    plugin_web = PluginWeb(plugin)
    
    user = User(request.user.username, request.user.email)
    home_dir = user.getUserHome()
    
    if request.method == 'POST':
        form = PluginForm(request.POST, tool=plugin)
        if form.is_valid():
            # FIRST ATTEMPT FOR SLURM
            # create the output directory if necessary
            d = os.path.join(settings.SLURM_DIR, request.user.username)
            if not os.path.exists(d):
                os.makedirs(d)
            full_path = os.path.join(d, plugin.suggestSlurmFileName())
            config_dict = form.data
            with open(full_path, 'w') as fp:
                plugin.writeSlurmFile(fp, config_dict=config_dict, user=user)    
            plugin.call('sbatch --uid=%s %s' %(request.user.username, full_path))
            return redirect('history:history') #should be changed to result page 
            
    else:   
        config_dict = plugin.setupConfiguration(check_cfg=False, substitute=False)      
        form = PluginForm(initial=config_dict,tool=plugin)
    
    
    return render(request, 'plugins/setup.html', {'tool' : plugin_web, 'form': form,
                                                  'user_home': home_dir})
  
@login_required()  
def dirlist(request):
    r=['<ul class="jqueryFileTree" style="display: none;">']
    files = list()
    try:
        r=['<ul class="jqueryFileTree" style="display: none;">']
        d=urllib.unquote(request.POST.get('dir'))
        for f in sorted(os.listdir(d)):
            if f[0] != '.':
                ff=os.path.join(d,f)
                if os.path.isdir(ff):
                    r.append('<li class="directory collapsed"><a href="#" rel="%s/">%s</a></li>' % (ff,f))
                else:
                    e=os.path.splitext(f)[1][1:] # get .ext and remove dot
                    files.append('<li class="file ext_%s"><a href="#" rel="%s">%s</a></li>' % (e,ff,f))
        r = r+files
        r.append('</ul>')
    except Exception,e:
        r.append('Could not load directory: %s' % str(e))
        r.append('</ul>')
    return HttpResponse(''.join(r))  

@login_required()
def solr_search(request):
    args = dict(request.GET)#self.request.arguments.copy()
    latest = True#bool(request.GET.get('latest', [False]))
    try:
        facets = request.GET['facet']
    except KeyError:
        facets = False
    if 'start' in args: args['start'] = int(request.GET['start']) 
    if 'rows' in args: args['rows'] = int(request.GET['rows'])
    
    metadata = None
    #return HttpResponse(json.dumps(dict(args)))
    if facets:
        args.pop('facet')
        if facets == '*':
            #means select all, 
            facets = None
        results = SolrFindFiles.facets(facets=facets, **args)
    else:
        #return HttpResponse(json.dumps(dict(hallo='was')))
        results = SolrFindFiles.search( _retrieve_metadata = True, **args)
        metadata = results.next()
        results = list(results)
      
    return HttpResponse(json.dumps(dict(data=results, metadata=metadata)), content_type="application/json")



    
    
  

## Rotten Microbes (rotmic) -- Laboratory Sequence and Sample Management
## Copyright 2013 Raik Gruenberg

## This file is part of the rotmic project (https://github.com/graik/rotmic).
## rotmic is free software: you can redistribute it and/or modify
## it under the terms of the GNU Affero General Public License as
## published by the Free Software Foundation, either version 3 of the
## License, or (at your option) any later version.

## rotmic is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Affero General Public License for more details.
## You should have received a copy of the GNU Affero General Public
## License along with rotmic. If not, see <http://www.gnu.org/licenses/>.

import datetime

from django.contrib import admin
import django.contrib.admin.widgets as widgets
import django.utils.html as html
from django.utils.safestring import mark_safe
import django.contrib.messages as messages 

import reversion

from rotmic.models import DnaComponentType, CellComponentType, \
     Unit, Sample, SampleAttachment, \
     Location, Rack, Container, DnaSample, CellSample

from .utils.customadmin import ViewFirstModelAdmin
from .utils import adminFilters as filters

from . import forms

import rotmic.initialTypes as T
import rotmic.templatetags.rotmicfilters as F
import rotmic.utils.ids as I

from .adminBase import BaseAdminMixin

from . import adminUser  ## trigger extension of User
from . import adminComponents ## trigger registration of component admin interfaces


class DnaComponentTypeAdmin( reversion.VersionAdmin, admin.ModelAdmin ):
    
    fieldsets = (
        (None, {
            'fields': (('name', 'subTypeOf',),
                       ('description', 'isInsert',),
                       ('uri',),
                       )
            }
         ),
        )
    
    list_display = ('__unicode__','subTypeOf', 'description', 'isInsert')
    list_display_links = ('__unicode__',)
    list_editable = ('isInsert',)
    
    list_filter = ('subTypeOf', 'isInsert')
                       

admin.site.register(DnaComponentType, DnaComponentTypeAdmin)


class CellComponentTypeAdmin( reversion.VersionAdmin, admin.ModelAdmin ):
    
    fieldsets = (
        (None, {
            'fields': (('name', 'subTypeOf',),
                       ('description',),
                       ( 'allowPlasmids', 'allowMarkers'),
                       ('uri',),
                       )
            }
         ),
        )
    
    list_display = ('__unicode__','subTypeOf', 'description', 'allowPlasmids', 
                    'allowMarkers')
    list_display_links = ('__unicode__',)
    list_editable = ('allowPlasmids','allowMarkers')
    
    list_filter = ('subTypeOf', 'allowPlasmids', 'allowMarkers')

admin.site.register(CellComponentType, CellComponentTypeAdmin)
    

class UnitAdmin( admin.ModelAdmin ):
    
    fieldsets = (
        (None, {
            'fields': (('name', 'unitType',),
                       ('conversion',),
                       )
            }
         ),
        )
    
    list_display = ('name','unitType', 'conversion')
    list_filter = ('unitType',)
    
admin.site.register( Unit, UnitAdmin )


class SampleAttachmentInline(admin.TabularInline):
    model = SampleAttachment
    form = forms.AttachmentForm
    template = 'admin/rotmic/componentattachment/tabular.html'
    can_delete=True
    extra = 1
    max_num = 5

    fieldsets = (
        (None, {
            'fields': ('f', 'description',),
            'description': 'Only attach files that are specific to this very sample\n'\
                           +'Use DNA or Cell attachments otherwise.',
            'classes': ('collapse',),
            
        }),
    )
    

class SampleAdmin( BaseAdminMixin, reversion.VersionAdmin, ViewFirstModelAdmin ):
    form = forms.SampleForm     
    
    change_list_template = 'admin/rotmic/sample/change_list.html'  ## for some reason this is needed.
    
    template = 'admin/rotmic/change_form_viewfirst.html'

    inlines = [ SampleAttachmentInline ]
    date_hierarchy = 'preparedAt'
    
    fieldsets = [
        (None, {
            'fields' : ((('container', 'displayId', 'status'),
                         ('preparedAt',),
                         ('comment'),
                    ))
            } ),
         ('Content', {
             'fields' : ((('concentration','concentrationUnit','amount','amountUnit',),
                         ('solvent','aliquotNr',),
                         )
                        ),
         }
        ), 
          
    ]
    list_display = ('showExtendedId', 'showRack', 'showLocation',
                    'preparedAt', 'registeredBy',
                    'showContent', 'showConcentration', 'showAmount',
                    'showStatus','showEdit')
    
    ordering = ('container', 'displayId')

    save_as = True
    save_on_top = True

    search_fields = ('diplayId', 'name','comment')
    
    list_filter = ('status', filters.SampleLocationFilter, 
                   filters.SampleRackFilter, filters.SampleContainerFilter,
                   filters.SortedUserFilter)
    
    def __init__(self, *args, **kwargs):
        """Disable automatic link generation"""
        super(SampleAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = []
        
    def queryset(self, request):
        """
        Return actual sub-class instances instead of generic Sample super-class
        This method builds on the custom InheritanceManager replacing Sample.objects
        """
        return super(SampleAdmin,self).queryset(request).select_subclasses()
        
    def showRack(self, o):
        if not o.container.rack:
            return u''
        x = o.container.rack
        url = x.get_absolute_url()
        return html.mark_safe('<a href="%s" title="%s">%s</a>' \
                              % (url, x.name, x.displayId) )
    showRack.allow_tags = True
    showRack.short_description = 'Rack'
        
    def showLocation(self, o):
        if not o.container.rack.location:
            return u''
        x = o.container.rack.location
        url = x.get_absolute_url()
        room = 'room %s' % x.room if x.room else ''
        temp = '%s C' % x.temperature if x.temperature else ''
        title = x.name
        title += ' (%s %s)' % (room, temp) if (room or temp) else ''
        return html.mark_safe('<a href="%s" title="%s">%s</a>' \
                              % (url, title, x.displayId) )
    showLocation.allow_tags = True
    showLocation.short_description = 'Location'

    def showComment(self, obj):
        """
        @return: str; truncated comment with full comment mouse-over
        """
        if not obj.comment: 
            return u''
        if len(obj.comment) < 40:
            return unicode(obj.comment)
        r = unicode(obj.comment[:38])
        r = '<a title="%s">%s</a>' % (obj.comment, F.truncate(obj.commentText(), 40))
        return r
    showComment.allow_tags = True
    showComment.short_description = 'Description'
    
    def showStatus(self, obj):
        color = {u'ok': '088A08', # green
                 u'bad': 'B40404', # red
                 u'empty' : 'B40404', # red
                 u'preparing':  '0000FF', # blue
                 }
        return '<span style="color: #%s;">%s</span>' %\
               (color.get(obj.status, '000000'), obj.status)
    showStatus.allow_tags = True
    showStatus.short_description = 'Status'
        

    def showEdit(self, obj):
        return mark_safe('<a href="%s"><img src="http://icons.iconarchive.com/icons/custom-icon-design/office/16/edit-icon.png"/></a>'\
                         % (obj.get_absolute_url_edit() ) )
    showEdit.allow_tags = True    
    showEdit.short_description = 'Edit'     

admin.site.register( Sample, SampleAdmin )


class DnaSampleAdmin( SampleAdmin ):
    form = forms.DnaSampleForm
    
    change_list_template = reversion.VersionAdmin.change_list_template ## revert change from SampleAdmin
    
    fieldsets = [
        (None, {
            'fields' : ((('displayId', 'container', 'status'),
                         ('preparedAt',),
                         ('comment'),
                    ))
            } ),
         ('Content', {
             'fields' : ((('dna',),
                          ('concentration','concentrationUnit','amount','amountUnit',),
                          ('solvent','aliquotNr',),
                         )
                        ),
         }
        ), 
    ]

    list_filter = ('status', filters.DnaSampleLocationFilter, 
                   filters.DnaSampleRackFilter, filters.DnaSampleContainerFilter,
                   filters.SortedUserFilter)
        
    def queryset(self, request):
        """Revert modification made by SampleAdmin"""
        return super(SampleAdmin,self).queryset(request)
    
admin.site.register( DnaSample, DnaSampleAdmin )


class CellSampleAdmin( SampleAdmin ):
    form = forms.CellSampleForm
    
    change_list_template = reversion.VersionAdmin.change_list_template ## revert change from SampleAdmin
    
    fieldsets = [
        (None, {
            'fields' : ((('displayId', 'container', 'status'),
                         ('preparedAt',),
                         ('comment'),
                    ))
            } ),
         ('Content', {
             'fields' : ((('cell',),
                          ('plasmid', 'cellCategory', 'cellType'),
                          ('amount','amountUnit',),
                          ('solvent','aliquotNr',),
                        )),
             'description': 'Select an existing Cell record or create a new Cell record on the fly from plasmid + strain below.'
         }
        ), 
    ]

    list_display = ('showExtendedId', 'showRack', 'showLocation',
                    'preparedAt', 'registeredBy',
                    'showContent', 'showAmount',
                    'showStatus','showEdit')
    
    list_filter = ('status', filters.CellSampleLocationFilter, 
                   filters.CellSampleRackFilter, filters.CellSampleContainerFilter,
                   filters.SortedUserFilter)
        
    def queryset(self, request):
        """Revert modification made by SampleAdmin"""
        return super(SampleAdmin,self).queryset(request)
    
admin.site.register( CellSample, CellSampleAdmin )


class LocationAdmin(BaseAdminMixin, reversion.VersionAdmin, ViewFirstModelAdmin):
    form = forms.LocationForm
    
    change_form_template = 'admin/rotmic/change_form_viewfirst.html'  ## adapt breadcrums to view first admin

    fieldsets = [
        (None, {
            'fields' : ((('displayId', 'name'),
                         ('temperature','room'),
                        )),
            'description' : 'Describe a freezer, row of shelves or similar storage location.',
            }
         )
        ]

    list_display = ('displayId', 'name', 'temperature', 'room',
                    'showRackCount', 'showContainerCount', 'showSampleCount')
    list_filter = ('room', 'temperature')
    search_fields = ('displayId', 'name',)

    save_as = True

admin.site.register( Location, LocationAdmin )


class RackAdmin(BaseAdminMixin, reversion.VersionAdmin, ViewFirstModelAdmin):
    form = forms.RackForm

    change_form_template = 'admin/rotmic/change_form_viewfirst.html'  ## adapt breadcrums to view first admin
    
    fieldsets = [
        (None, {
            'fields' : ((('displayId', 'location', 'name'),
                        )),
            'description' : 'Describe a freezer rack, single shelve or similar holder of containers.'
            }
         )
        ]

    list_display = ('displayId', 'showLocationUrl', 'name',
                    'showContainerCount', 'showSampleCount')
    list_filter = (filters.RackLocationFilter,)
    search_fields = ('displayId', 'name',)

    save_as = True

    def showLocationUrl(self, obj):
        """Table display of linked insert or ''"""
        assert isinstance(obj, Rack), 'object missmatch'
        x = obj.location
        if not x:
            return u''
        url = x.get_absolute_url()
        return html.mark_safe('<a href="%s" title="">%s</a>' \
                              % (url, unicode(x)) )
    showLocationUrl.allow_tags = True
    showLocationUrl.short_description = 'Location'
    

admin.site.register( Rack, RackAdmin )


class ContainerAdmin(BaseAdminMixin, reversion.VersionAdmin, ViewFirstModelAdmin):
    form = forms.ContainerForm

    change_form_template = 'admin/rotmic/change_form_viewfirst.html'  ## adapt breadcrums to view first admin

    fieldsets = [
        (None, {
            'fields' : ((('displayId', 'rack', 'name'),
                         ('containerType',),
                         ('comment',),
                        )),
            'description' : 'Describe a sample container or box.'
            }
         )
        ]

    list_display = ('__unicode__', 'showRackUrl', 'showLocationUrl', 'containerType', 'showSampleCount')
    list_filter =  ('containerType', filters.ContainerLocationFilter, filters.ContainerRackFilter)
    search_fields = ('displayId', 'name','comment')

    save_as = True

    def showLocationUrl(self, obj):
        """Table display of linked insert or ''"""
        assert isinstance(obj, Container), 'object missmatch'
        x = obj.rack.location
        if not x:
            return u''
        url = x.get_absolute_url()
        return html.mark_safe('<a href="%s" title="">%s</a>' \
                              % (url, unicode(x)) )
    showLocationUrl.allow_tags = True
    showLocationUrl.short_description = 'Location'

    def showRackUrl(self, obj):
        """Table display of linked insert or ''"""
        assert isinstance(obj, Container), 'object missmatch'
        x = obj.rack
        if not x:
            return u''
        url = x.get_absolute_url()
        return html.mark_safe('<a href="%s" title="">%s</a>' \
                              % (url, unicode(x)) )
    showRackUrl.allow_tags = True
    showRackUrl.short_description = 'Rack'

admin.site.register( Container, ContainerAdmin )


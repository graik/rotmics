## Rotten Microbes (rotmic) -- Laboratory Sequence and Sample Management
## Copyright 2013 - 2014 Raik Gruenberg

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
import django.forms as forms
from django.core.exceptions import ValidationError
import django.contrib.messages as messages
from django.contrib.auth.models import User

import selectLookups as L
import selectable.forms as sforms

from .baseforms import ModelFormWithRequest

import rotmic.models as M


class SequencingForm(ModelFormWithRequest):
    """Customized Form for Sample add / change. 
    To be overridden rather than used directly."""
    
    ## workaround for selectable focus issue -- AutoComplete fields cannot
    ## be in first position; otherwise pre-selected values (e.g. from URL) 
    ## always fail javascript validation when the cursor is moved away
    dummyfield = forms.CharField(widget=forms.HiddenInput,
                                 required=False,
                                 label='')
    
    def __init__(self, *args, **kwargs):
        """
        Relies on self.request which is created by ModelFormWithRequest
        via custom ModelAdmin.
        """
        super(SequencingForm, self).__init__(*args, **kwargs)

        ## only execute for Add forms without existing instance
        o = kwargs.get('instance', None)
        if not o and self.request: 
            self.initial['orderedBy'] = str(self.request.user.id)

    class Meta:
        model = M.Sequencing
        widgets = {'sample': sforms.AutoComboboxSelectWidget(lookup_class=L.DnaSampleLookup,
                                                             allow_new=False,
                                                             attrs={'size':15}),
                   'orderedBy': sforms.AutoComboboxSelectWidget(lookup_class=L.UserLookup,
                                                                allow_new=False,
                                                                attrs={'size':15}),
                   'comments' : forms.Textarea(attrs={'rows': 5,'cols': 80})
                   }

class SequencingRunForm(forms.ModelForm):
    
    class Meta:
        model = M.SequencingRun
        widgets = {'primer': sforms.AutoComboboxSelectWidget(lookup_class=L.SequencingOligoLookup,
                                                             allow_new=False,
                                                             attrs={'size':15}),
                   'description' : forms.Textarea(attrs={'rows': 2,'cols': 40})
                   }

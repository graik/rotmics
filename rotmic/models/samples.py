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
from datetime import datetime
import re

from django.db import models
from django.db.models import Q
import django.utils.html as html
from django.contrib.auth.models import User, Group

from .usermixin import UserMixin, ReadonlyUrlMixin
from .storage import Container
from .sequencing import Sequencing
import rotmic.utils.inheritance as I


class SampleProvenanceType(models.Model):
    """Classification of relations between samples"""
    
    name = models.CharField('Name', max_length=200, blank=True, 
                            help_text='short descriptive name (must be unique)',
                            unique=True )
    
    requiresSource = models.BooleanField('Requires source', default=True, 
                                          help_text='Links of this type require a source sample.')
    
    description = models.TextField('Description', blank=True, help_text='detailed description' )
    
    isDefault = models.BooleanField('make Default', default=False,
                                    help_text='Make this the default choice of provenance type.')
    
    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        app_label = 'rotmic'
        verbose_name  = 'Provenance Type'
        ordering = ['isDefault', 'name']
    

class SampleProvenance(models.Model):
    """Sample History"""
    
    sample = models.ForeignKey('Sample', related_name='sampleParents')
    
    sourceSample = models.ForeignKey('Sample', null=True, blank=True, related_name='sampleChilds',
                                     verbose_name='from sample')
    
    description = models.CharField( 'Comment', max_length=200,
                                    help_text='',
                                    blank=True )

    provenanceType = models.ForeignKey( SampleProvenanceType, 
                                        verbose_name='via (method)',
                                        help_text="How is this sample derived from it's source?",
                                        blank=True)

    def __unicode__(self):
        """"""
        try:
            r = unicode(self.provenanceType.name)
            if self.sourceSample:
                r += u' from ' + unicode(self.sourceSample)
            return r
        except:
            return 'undefined Sample Provenance'

    class Meta:
        app_label = 'rotmic'
        verbose_name  = 'Sample History'
        verbose_name_plural = 'Sample History'
        ordering = ['sample']


class Sample( UserMixin, ReadonlyUrlMixin ):
    """Base class for DNA, cell and protein samples."""

    displayId = models.CharField('Position', max_length=20,
                                 help_text='Position or label')

    container = models.ForeignKey(Container, related_name='samples',
                                  help_text='Start typing name or ID...')

    aliquotNr = models.PositiveIntegerField('Number of aliquots', 
                                            null=True, blank=True)

    STATUS_CHOICES = (('ok', 'ok'),
                      ('preparing', 'preparing'),
                      ('empty', 'empty'),
                      ('unknown', 'unknown'),
                      ('bad', 'corrupted'),
                      )
    
    status = models.CharField( max_length=30, choices=STATUS_CHOICES, 
                               default='ok', verbose_name='Status')
    
    description = models.TextField('Description', blank=True)

    preparedAt = models.DateField(default=datetime.now().date(), verbose_name="Prepared")
    
    preparedBy = models.ForeignKey(User, null=False, blank=False, 
                                related_name='%(class)s_prepared_by',
                                verbose_name='By')
    
    experimentNr = models.CharField('Experiment Nr.', blank=True, null=True, 
                              max_length=100,
                              help_text='experiment/lab book Nr.' )
    
    solvent = models.CharField('in Buffer/Medium', max_length=100, blank=True)

    concentration = models.FloatField('Concentration', null=True, blank=True)

    concentrationUnit = models.ForeignKey('Unit', 
                                          verbose_name='Conc. Unit',
                                          related_name='concUnit+',  ## supress back-reference
                                          null=True, blank=True,
                                          limit_choices_to = {'unitType': 'concentration'},
                                          on_delete=models.PROTECT)    
    
    amount = models.FloatField('Amount', null=True, blank=True)
    amountUnit = models.ForeignKey('Unit', 
                                   verbose_name='Amount Unit',
                                   related_name='amountUnit+', ## suppress back-reference
                                   null=True, blank=True, 
                                   limit_choices_to = Q(unitType__in=['volume','number', 'mass']),
                                   on_delete=models.PROTECT
                                   )


    provenance =models.ManyToManyField(SampleProvenance, blank=True, null=True, 
                                       related_name='samples+',   ## end with + to suppress reverse relationship
                                       verbose_name='History',
                                       help_text='Sample History')
    
    ## return child classes in queries using select_subclasses()
    objects = I.InheritanceManager()  

    def __unicode__(self):
        return u'%s : %s' % (self.container.displayId, self.displayId)
    
    def clean(self):
        """Prevent that parent class Samples are ever saved through admin."""
        from django.core.exceptions import ValidationError
        if self.__class__ is Sample:
            raise ValidationError('Cannot create generic samples without content.')        
    
    def save(self, *args, **kwargs):
        """Prevent parent class Sample saving at the django core level."""
        if self.__class__ is Sample:
            raise NotImplementedError('Attempt to create generic Sample instance.')
        super(Sample, self).save(*args, **kwargs)
    
    @property
    def content(self):
        """return subtype-specific content object. Needs to be overriden"""
        return self.convertClass().content

    def descriptionText(self):
        """remove some formatting characters from text"""
        r = re.sub('--','', self.description)
        r = re.sub('=','', r)
        r = re.sub('__','', r)
        return r
    descriptionText.short_description = 'description'
    
    def sourceSamples(self):
        """All samples that are registered as source in provenance records"""
        return Sample.objects.filter(sampleChilds__sample__id=self.id)
    
    
    def sameSamples(self):
        """
        Needs to be overriden!
        @return samples that have exactly the same content
        """
        return []
    
    def relatedSamples(self):
        """
        Samples that are related but not identical
        """
        return []

    def subClass(self):
        """
        Identify sample subClass used for this instance.
        @return: class, (either DnaSample, CellSample, ChemicalSample or OligoSample)
        """
        if self.__class__ is not Sample:
            return self.__class__

        for c in [DnaSample, CellSample, ChemicalSample, OligoSample, ProteinSample]:
            try: 
                return c.objects.get(id=self.id).__class__
            except:
                pass

        return self.__class__   
    
    def convertClass(self):
        """
        Convert a generic Sample instance into the best matching specific sample instance.
        @return: instance of specific Sample sub-class.
        """
        return self.subClass().objects.get(id=self.id)

    
    def showVerbose(self):
        """display full chain location / rack / container / sample with links"""
        r = u''
        r += self.container.showVerbose() + ' / '
        
        title = 'Sample\n%s' % self.displayId
        if self.description:
            title += '\n' + self.description

        url = self.get_absolute_url()
        r += '<a href="%s" title="%s">%s</a>' % (url, title, self.displayId) 
        return html.mark_safe(r)
    
    showVerbose.allow_tags = True
    showVerbose.short_description = 'Sample'
    
    def showExtendedId(self):
        """Display Container -- Sample for table views"""
        r = u'%s : %s' % (self.container.displayId, self.displayId)

        title = self.description
        url = self.get_absolute_url()
        return html.mark_safe('<a href="%s" title="%s">%s</a>' % (url, title, r))
    showExtendedId.allow_tags = True
    showExtendedId.short_description = u'Box : ID'
    
    def showContent(self):
        """Table display of linked content or ''"""
        x = self.content
        if not x:
            return u''
        url = x.get_absolute_url()
        return html.mark_safe('<a href="%s" title="%s">%s</a> (%s)' \
                              % (url, x.description, x.displayId, x.name))
    showContent.allow_tags = True
    showContent.short_description = u'Content'
    
    def showType(self):
        """Return type of sample (DNA, Cells, ...)"""
        r = getattr(self._meta, 'verbose_name', 'unknown type')
        r = r.split()[0]
        return r
    showType.short_description = 'Type'

    def showConcentration(self):
        conc = unicode(self.concentration or '')
        unit = unicode(self.concentrationUnit or '')
        return conc + ' '+ unit
    showConcentration.short_description = 'Concentration' 
    
    def showAmount(self):
        amount = unicode( self.amount or '' )
        unit   = unicode( self.amountUnit or '' )
        return amount + ' '+ unit
    showAmount.short_description = 'Amount' 
    
    def showAliquots(self):
        """@return: str; number of aliquots"""
        if not self.aliquotNr:
            return u''
        return unicode(self.aliquotNr)
    showAliquots.short_description = 'Alq.'
    
    def showStatus(self):
        color = {u'ok': '088A08', # green
                 u'bad': 'B40404', # red
                 u'empty' : 'B40404', # red
                 u'preparing':  '0000FF', # blue
                 }
        r = '<span style="color: #%s;">%s</span>' %\
            (color.get(self.status, '000000'), self.get_status_display())
        return html.mark_safe(r)
    showStatus.allow_tags = True
    showStatus.short_description = 'Status'

    class Meta:
        app_label = 'rotmic'
        verbose_name  = 'Sample'
        ordering = ['container', 'displayId']
        unique_together = ('displayId', 'container')
   

class DnaSample( Sample ):
    """Samples linked to DnaComponent"""
    
    dna = models.ForeignKey('DnaComponent',
                            verbose_name = 'DNA construct',
                            related_name = 'dna_samples',
                            )

    def sameSamples(self):
        """
        @return samples that have exactly the same content
        """
        return DnaSample.objects.filter(dna=self.dna).exclude(id=self.id)
    
    def relatedSamples(self):
        """
        Samples that are related but not identical
        """
        return []

    @property
    def content(self):
        return self.dna

    def showContent(self):
        return super(DnaSample, self).showContent()
    showContent.allow_tags = True
    showContent.short_description = 'DNA construct'
    
    def showSequencing(self):
        """
        Show sequencing evaluation of highest priority:
        confirmed > inconsistent > ambiguous > problems > not analyzed
        """
        if self.sequencing.count() == 0:
            return u''
        eval_priority = [ x[0] for x in Sequencing.EVALUATIONS ]

        for e in eval_priority:
            x = self.sequencing.filter(evaluation=e).first()
            if x:
                r = html.mark_safe('<a href="%s">%s</a>' % 
                                   (x.get_absolute_url(), x.showEvaluationIcon()))
                return r
        return u'other'
    showSequencing.allow_tags = True
    showSequencing.short_description = 'Seq'
    
    def showSequencingAll(self):
        """
        Show a sequencing evaluation icon for each registered sequencing.
        """
        r = u''
        eval_priority = [ x[0] for x in Sequencing.EVALUATIONS ]
        
        ## display icon for each seq. records in order of evaluation priority
        for e in eval_priority:
            for x in self.sequencing.filter(evaluation=e):
                r += ' ' + '<a href="%s">%s</a>' % \
                                       (x.get_absolute_url(), x.showEvaluationIcon())
        return html.mark_safe(r)
    showSequencingAll.allow_tags = True
    showSequencingAll.short_description = 'Sequencing'

    class Meta:
        app_label = 'rotmic'
        verbose_name = 'DNA Sample'


class CellSample( Sample ):
    """Samples linked to CellComponent"""
    
    cell = models.ForeignKey('CellComponent',
                            verbose_name = 'Cell',
                            related_name = 'cell_samples',
                            help_text='start typing name or ID of existing cell record...',
                            )

    def sameSamples(self):
        """
        @return samples that have exactly the same content
        """
        return CellSample.objects.filter(cell=self.cell).exclude(id=self.id)
    
    def relatedSamples(self):
        """
        Samples that are related but not identical
        """
        return []

    @property
    def content(self):
        return self.cell

    def showContent(self):
        return super(CellSample, self).showContent()
    showContent.short_description = 'Cell'

    class Meta:
        app_label = 'rotmic'
        verbose_name = 'Cell Sample'


class OligoSample( Sample ):
    """Samples linked to CellComponent"""
    
    oligo = models.ForeignKey('OligoComponent',
                              verbose_name = 'Oligo',
                              related_name = 'oligo_samples',
                              help_text='start typing name or ID of existing cell record...',
                              )

    def sameSamples(self):
        """
        @return samples that have exactly the same content
        """
        return OligoSample.objects.filter(oligo=self.oligo).exclude(id=self.id)
    
    def relatedSamples(self):
        """
        Samples that are related but not identical
        """
        return []

    @property
    def content(self):
        return self.oligo

    def showContent(self):
        return super(OligoSample, self).showContent()
    showContent.short_description = 'Oligo'

    class Meta:
        app_label = 'rotmic'
        verbose_name = 'Oligo Sample'


class ChemicalSample( Sample ):
    """Samples linked to ChemicalComponent"""
    
    chemical = models.ForeignKey('ChemicalComponent',
                              verbose_name = 'Chemical',
                              related_name = 'chemical_samples',
                              help_text='start typing name or ID of existing chemical record...',
                              )

    def sameSamples(self):
        """
        @return samples that have exactly the same content
        """
        return ChemicalSample.objects.filter(chemical=self.chemical).exclude(id=self.id)
    
    def relatedSamples(self):
        """
        Samples that are related but not identical
        """
        return []

    @property
    def content(self):
        return self.chemical

    def showContent(self):
        return super(ChemicalSample, self).showContent()
    showContent.short_description = 'Chemical'

    class Meta:
        app_label = 'rotmic'
        verbose_name = 'Chemical Sample'


class ProteinSample( Sample ):
    """Samples linked to ProteinComponent"""
    
    protein = models.ForeignKey('ProteinComponent',
                              verbose_name = 'Protein',
                              related_name = 'protein_samples',
                              help_text='start typing name or ID of existing protein record...',
                              )

    def sameSamples(self):
        """
        @return samples that have exactly the same content
        """
        return ProteinSample.objects.filter(protein=self.protein).exclude(id=self.id)
    
    def relatedSamples(self):
        """
        Samples that are related but not identical
        """
        return []

    @property
    def content(self):
        return self.protein

    def showContent(self):
        return super(ProteinSample, self).showContent()
    showContent.short_description = 'Protein'

    class Meta:
        app_label = 'rotmic'
        verbose_name = 'Protein Sample'

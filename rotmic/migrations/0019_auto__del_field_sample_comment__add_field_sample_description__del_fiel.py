# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Renaming field 'Sample.comment'
        db.rename_column(u'rotmic_sample', 'comment', 'description')


        # Renaming field 'Component.comment'
        db.rename_column(u'rotmic_component', 'comment', 'description')


        # Renaming field 'Container.comment'
        db.rename_column(u'rotmic_container', 'comment', 'description')


    def backwards(self, orm):

        # renaming field 'Sample.description'
        db.rename_column(u'rotmic_sample', 'description', 'comment')


        # renaming field 'Component.description'
        db.rename_column(u'rotmic_component', 'description', 'comment')


        # renaming field 'Container.description'
        db.rename_column(u'rotmic_container', 'description', 'comment')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'rotmic.cellcomponent': {
            'Meta': {'ordering': "['displayId']", 'object_name': 'CellComponent', '_ormbases': ['rotmic.Component']},
            'componentType': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rotmic.CellComponentType']"}),
            u'component_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['rotmic.Component']", 'unique': 'True', 'primary_key': 'True'}),
            'markers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'as_marker_in_cell'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['rotmic.DnaComponent']"}),
            'plasmid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'as_plasmid_in_cell'", 'null': 'True', 'to': "orm['rotmic.DnaComponent']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'planning'", 'max_length': '30'})
        },
        'rotmic.cellcomponenttype': {
            'Meta': {'ordering': "['subTypeOf__name', 'name']", 'object_name': 'CellComponentType'},
            'allowMarkers': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'allowPlasmids': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'subTypeOf': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subTypes'", 'null': 'True', 'to': "orm['rotmic.CellComponentType']"}),
            'uri': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'rotmic.cellsample': {
            'Meta': {'ordering': "['container', 'displayId']", 'object_name': 'CellSample', '_ormbases': ['rotmic.Sample']},
            'cell': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cell_samples'", 'to': "orm['rotmic.CellComponent']"}),
            u'sample_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['rotmic.Sample']", 'unique': 'True', 'primary_key': 'True'})
        },
        'rotmic.chemicalcomponent': {
            'Meta': {'ordering': "['displayId']", 'object_name': 'ChemicalComponent', '_ormbases': ['rotmic.Component']},
            'cas': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'componentType': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rotmic.ChemicalType']"}),
            u'component_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['rotmic.Component']", 'unique': 'True', 'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'available'", 'max_length': '30'})
        },
        'rotmic.chemicalsample': {
            'Meta': {'ordering': "['container', 'displayId']", 'object_name': 'ChemicalSample', '_ormbases': ['rotmic.Sample']},
            'chemical': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'chemical_samples'", 'to': "orm['rotmic.ChemicalComponent']"}),
            u'sample_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['rotmic.Sample']", 'unique': 'True', 'primary_key': 'True'})
        },
        'rotmic.chemicaltype': {
            'Meta': {'ordering': "['subTypeOf__name', 'name']", 'object_name': 'ChemicalType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'subTypeOf': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subTypes'", 'null': 'True', 'to': "orm['rotmic.ChemicalType']"}),
            'uri': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'rotmic.component': {
            'Meta': {'object_name': 'Component'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'displayId': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifiedAt': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 15, 0, 0)'}),
            'modifiedBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'component_modified_by'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'registeredAt': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 15, 0, 0)'}),
            'registeredBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'component_created_by'", 'to': u"orm['auth.User']"})
        },
        'rotmic.componentattachment': {
            'Meta': {'object_name': 'ComponentAttachment'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'f': ('rotmic.utils.filefields.DocumentModelField', [], {'max_length': '100', 'extensions': '()'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attachments'", 'to': "orm['rotmic.Component']"})
        },
        'rotmic.container': {
            'Meta': {'ordering': "('rack', 'displayId')", 'object_name': 'Container'},
            'containerType': ('django.db.models.fields.CharField', [], {'default': "'box'", 'max_length': '30'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'displayId': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifiedAt': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 15, 0, 0)'}),
            'modifiedBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'container_modified_by'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'rack': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'containers'", 'to': "orm['rotmic.Rack']"}),
            'registeredAt': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 15, 0, 0)'}),
            'registeredBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'container_created_by'", 'to': u"orm['auth.User']"})
        },
        'rotmic.dnacomponent': {
            'Meta': {'ordering': "['displayId']", 'object_name': 'DnaComponent', '_ormbases': ['rotmic.Component']},
            'componentType': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rotmic.DnaComponentType']"}),
            u'component_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['rotmic.Component']", 'unique': 'True', 'primary_key': 'True'}),
            'genbank': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'insert': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'as_insert_in_dna'", 'null': 'True', 'to': "orm['rotmic.DnaComponent']"}),
            'markers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'as_marker_in_dna'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['rotmic.DnaComponent']"}),
            'sequence': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'planning'", 'max_length': '30'}),
            'vectorBackbone': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'as_vector_in_plasmid'", 'null': 'True', 'to': "orm['rotmic.DnaComponent']"})
        },
        'rotmic.dnacomponenttype': {
            'Meta': {'ordering': "['subTypeOf__name', 'name']", 'object_name': 'DnaComponentType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isInsert': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'subTypeOf': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subTypes'", 'null': 'True', 'to': "orm['rotmic.DnaComponentType']"}),
            'uri': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'rotmic.dnasample': {
            'Meta': {'ordering': "['container', 'displayId']", 'object_name': 'DnaSample', '_ormbases': ['rotmic.Sample']},
            'dna': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dna_samples'", 'to': "orm['rotmic.DnaComponent']"}),
            u'sample_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['rotmic.Sample']", 'unique': 'True', 'primary_key': 'True'})
        },
        'rotmic.location': {
            'Meta': {'ordering': "('displayId',)", 'object_name': 'Location'},
            'displayId': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifiedAt': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 15, 0, 0)'}),
            'modifiedBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'location_modified_by'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'registeredAt': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 15, 0, 0)'}),
            'registeredBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'location_created_by'", 'to': u"orm['auth.User']"}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'temperature': ('django.db.models.fields.FloatField', [], {'default': '25.0', 'null': 'True', 'blank': 'True'})
        },
        'rotmic.oligocomponent': {
            'Meta': {'ordering': "['displayId']", 'object_name': 'OligoComponent', '_ormbases': ['rotmic.Component']},
            'componentType': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rotmic.OligoComponentType']"}),
            u'component_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['rotmic.Component']", 'unique': 'True', 'primary_key': 'True'}),
            'meltingTemp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sequence': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'available'", 'max_length': '30'}),
            'templates': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'template_for_oligos'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['rotmic.DnaComponent']"})
        },
        'rotmic.oligocomponenttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'OligoComponentType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'uri': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'rotmic.oligosample': {
            'Meta': {'ordering': "['container', 'displayId']", 'object_name': 'OligoSample', '_ormbases': ['rotmic.Sample']},
            'oligo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'oligo_samples'", 'to': "orm['rotmic.OligoComponent']"}),
            u'sample_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['rotmic.Sample']", 'unique': 'True', 'primary_key': 'True'})
        },
        'rotmic.rack': {
            'Meta': {'ordering': "('location__displayId', 'displayId')", 'object_name': 'Rack'},
            'displayId': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'racks'", 'null': 'True', 'to': "orm['rotmic.Location']"}),
            'modifiedAt': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 15, 0, 0)'}),
            'modifiedBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rack_modified_by'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'registeredAt': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 15, 0, 0)'}),
            'registeredBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rack_created_by'", 'to': u"orm['auth.User']"})
        },
        'rotmic.sample': {
            'Meta': {'ordering': "['container', 'displayId']", 'unique_together': "(('displayId', 'container'),)", 'object_name': 'Sample'},
            'aliquotNr': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'amount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'amountUnit': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'amountUnit+'", 'null': 'True', 'to': "orm['rotmic.Unit']"}),
            'concentration': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'concentrationUnit': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'concUnit+'", 'null': 'True', 'to': "orm['rotmic.Unit']"}),
            'container': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'samples'", 'to': "orm['rotmic.Container']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'displayId': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifiedAt': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 15, 0, 0)'}),
            'modifiedBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sample_modified_by'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'preparedAt': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 11, 15, 0, 0)'}),
            'registeredAt': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 15, 0, 0)'}),
            'registeredBy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sample_created_by'", 'to': u"orm['auth.User']"}),
            'solvent': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'ok'", 'max_length': '30'})
        },
        'rotmic.sampleattachment': {
            'Meta': {'object_name': 'SampleAttachment'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'f': ('rotmic.utils.filefields.DocumentModelField', [], {'max_length': '100', 'extensions': '()'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attachments'", 'to': "orm['rotmic.Sample']"})
        },
        'rotmic.unit': {
            'Meta': {'ordering': "['unitType', 'conversion', 'name']", 'object_name': 'Unit'},
            'conversion': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'unitType': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'rotmic.userprofile': {
            'Meta': {'ordering': "('user',)", 'object_name': 'UserProfile'},
            'ccPrefix': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'chPrefix': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'dcPrefix': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ocPrefix': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'prefix': ('django.db.models.fields.CharField', [], {'default': "'mt'", 'max_length': '5'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['rotmic']
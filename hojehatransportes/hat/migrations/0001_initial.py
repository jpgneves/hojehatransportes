# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Company'
        db.create_table('hat_company', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('transport_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('hat', ['Company'])

        # Adding model 'Region'
        db.create_table('hat_region', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('hat', ['Region'])

        # Adding model 'Strike'
        db.create_table('hat_strike', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hat.Company'])),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('all_day', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('upvotes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('downvotes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hat.Region'])),
            ('canceled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('source_link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('hat', ['Strike'])


    def backwards(self, orm):
        
        # Deleting model 'Company'
        db.delete_table('hat_company')

        # Deleting model 'Region'
        db.delete_table('hat_region')

        # Deleting model 'Strike'
        db.delete_table('hat_strike')


    models = {
        'hat.company': {
            'Meta': {'object_name': 'Company'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'transport_type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'hat.region': {
            'Meta': {'object_name': 'Region'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'hat.strike': {
            'Meta': {'object_name': 'Strike'},
            'all_day': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'canceled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hat.Company']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'downvotes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hat.Region']"}),
            'source_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'upvotes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['hat']

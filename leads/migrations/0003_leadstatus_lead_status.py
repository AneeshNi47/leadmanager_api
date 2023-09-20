from django.db import migrations, models
import django.db.models.deletion

def create_default_leadstatuses(apps, schema_editor):
    LeadStatus = apps.get_model('leads', 'LeadStatus')
    if LeadStatus.objects.count() == 0:
        LeadStatus.objects.bulk_create([
            LeadStatus(status_title='New Lead', status='new_lead', active=True),
            LeadStatus(status_title='Contacted', status='contacted', active=True),
            LeadStatus(status_title='Converted', status='converted', active=True),
            LeadStatus(status_title='Not Converted', status='not_converted', active=False),
        ])

class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0002_lead_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeadStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_title', models.CharField(max_length=150)),
                ('status', models.CharField(max_length=150)),
                ('active', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='lead',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leads', to='leads.leadstatus'),
        ),
        migrations.RunPython(create_default_leadstatuses),
    ]

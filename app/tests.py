from django.test import TestCase
from app.models import Institut, TenantMessage, TenantFolder, TenantDocument, Domaine
from django_tenants.utils import get_tenant_model

class CrossTenantCommunicationTest(TestCase):
    def setUp(self):
        # Create a Master tenant
        self.master_tenant = Institut.objects.create(
            schema_name='public',
            nom='Master Institute',
            tenant_type='master'
        )
        # Domain is required for tenant creation usually, but we are just testing models
        Domaine.objects.create(domain='master.test.com', tenant=self.master_tenant, is_primary=True)

        # Create a Second tenant
        self.second_tenant = Institut.objects.create(
            schema_name='school2',
            nom='Second Institute',
            tenant_type='second'
        )
        Domaine.objects.create(domain='second.test.com', tenant=self.second_tenant, is_primary=True)

    def test_message_creation(self):
        # Master sends message to Second
        msg = TenantMessage.objects.create(
            sender=self.master_tenant,
            receiver=self.second_tenant,
            message="Hello from Master"
        )
        
        self.assertEqual(TenantMessage.objects.count(), 1)
        self.assertEqual(msg.sender, self.master_tenant)
        self.assertEqual(msg.receiver, self.second_tenant)
        self.assertFalse(msg.is_read)

    def test_folder_and_document(self):
        # Master shares a folder
        folder = TenantFolder.objects.create(
            sender=self.master_tenant,
            receiver=self.second_tenant,
            name="Shared Resources"
        )
        
        # Master adds a document to the folder
        doc = TenantDocument.objects.create(
            sender=self.master_tenant,
            receiver=self.second_tenant,
            folder=folder,
            description="Important Doc",
            file="test_file.pdf" # Mock file path
        )

        self.assertEqual(TenantFolder.objects.count(), 1)
        self.assertEqual(TenantDocument.objects.count(), 1)
        self.assertEqual(doc.folder, folder)


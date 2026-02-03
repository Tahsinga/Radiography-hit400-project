from django.core.management.base import BaseCommand
from apps.appointments.models import ScanType, MedicalAidCoverage
from decimal import Decimal

class Command(BaseCommand):
    help = 'Initialize database with sample scan types and medical aid coverage'

    def handle(self, *args, **options):
        # Create ScanTypes
        scan_types_data = [
            {
                'name': 'X-Ray',
                'description': 'Standard X-ray imaging',
                'base_price': Decimal('150.00'),
                'estimated_duration_minutes': 15
            },
            {
                'name': 'CT Scan',
                'description': 'Computed Tomography Scan',
                'base_price': Decimal('500.00'),
                'estimated_duration_minutes': 30
            },
            {
                'name': 'MRI',
                'description': 'Magnetic Resonance Imaging',
                'base_price': Decimal('800.00'),
                'estimated_duration_minutes': 45
            },
            {
                'name': 'Ultrasound',
                'description': 'Ultrasound Imaging',
                'base_price': Decimal('250.00'),
                'estimated_duration_minutes': 20
            },
            {
                'name': 'Mammography',
                'description': 'Breast X-ray imaging',
                'base_price': Decimal('300.00'),
                'estimated_duration_minutes': 25
            },
            {
                'name': 'Fluoroscopy',
                'description': 'Real-time X-ray imaging',
                'base_price': Decimal('400.00'),
                'estimated_duration_minutes': 30
            },
        ]

        for scan_type_data in scan_types_data:
            ScanType.objects.get_or_create(
                name=scan_type_data['name'],
                defaults=scan_type_data
            )
            self.stdout.write(f"Created ScanType: {scan_type_data['name']}")

        # Create Medical Aid Coverage
        medical_aids = [
            {
                'medical_aid_name': 'Medshield',
                'coverage_percentage': 85,
                'requires_authorization': False,
                'description': 'Standard coverage'
            },
            {
                'medical_aid_name': 'Discovery Health',
                'coverage_percentage': 80,
                'requires_authorization': True,
                'description': 'Requires authorization for advanced scans'
            },
            {
                'medical_aid_name': 'Bonitas',
                'coverage_percentage': 75,
                'requires_authorization': False,
                'description': 'Standard coverage'
            },
            {
                'medical_aid_name': 'GEMS',
                'coverage_percentage': 80,
                'requires_authorization': False,
                'description': 'Standard coverage'
            },
            {
                'medical_aid_name': 'Private Patient',
                'coverage_percentage': 50,
                'requires_authorization': False,
                'description': 'Private pay option'
            },
        ]

        for aid_data in medical_aids:
            MedicalAidCoverage.objects.get_or_create(
                medical_aid_name=aid_data['medical_aid_name'],
                defaults=aid_data
            )
            self.stdout.write(f"Created Medical Aid: {aid_data['medical_aid_name']}")

        self.stdout.write(self.style.SUCCESS('Successfully initialized database'))

from django.test import TestCase
from .models import Testimonial
# فرض کنید User و Course وجود دارند
from accounts.models import User
from courses.models import Course

class TestimonialModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com')
        self.course = Course.objects.create(name='Test Course', price=100)

    def test_testimonial_creation(self):
        testimonial = Testimonial.objects.create(student=self.user, course=self.course, rating=5, content='Great!')
        self.assertEqual(testimonial.student_name, self.user.get_full_name())
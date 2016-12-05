from django.contrib.auth.forms import UserCreationForm
from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

from product.forms import ProductForm, CommentForm
from .models import Product, Comment


# Create your tests here.
class TestTaskTest(TestCase):

    def setUp(self):
        User.objects.all().delete()
        Product.objects.all().delete()
        Comment.objects.all().delete()
        self.client = Client()


class TestLike(TestTaskTest):

    def test_add_like_not_logged(self):
        p = Product.objects.create(name='name', description='desc', price=17)

        self.assertEqual(p.total_likes, 0)
        self.client.post(reverse('like', kwargs={'product_slug': p.slug}))

        self.assertEqual(p.total_likes, 0)

    def test_add_like(self):
        credentials = {
            'username': 'testuser',
            'password': 'secret'
        }

        p = Product.objects.create(name='name', description='desc', price=17)
        User.objects.create_user(**credentials)
        self.client.post(reverse('login'), credentials, follow=True)
        self.assertTrue(User.objects.count(), 1)

        self.assertEqual(p.total_likes, 0)
        self.client.post(reverse('like', kwargs={'product_slug': p.slug}))
        self.assertEqual(p.total_likes, 1)


class TestCommentsForm(TestTaskTest):

    def test_add_comment_form_fail(self):
        p = Product.objects.create(name='name', description='desc', price=17)

        bad_form_data = {
            'text': '',
        }

        form = CommentForm(data=bad_form_data)
        self.assertFalse(form.is_valid())

        response = self.client.post(
            reverse('product', kwargs={'product_slug': p.slug}), bad_form_data)
        self.assertFormError(
            response, 'form', 'text', "This field is required.")

        self.assertEqual(Comment.objects.count(), 0)

    def test_add_comment_form_success(self):
        p = Product.objects.create(name='name', description='desc', price=17)

        good_form_data = {
            'text': 'comment text',
        }

        form = CommentForm(data=good_form_data)
        self.assertTrue(form.is_valid())

        self.client.post(reverse('product', kwargs={'product_slug': p.slug}),
                         good_form_data)

        self.assertEqual(Comment.objects.count(), 1)

    def test_old_comment_not_on_page(self):
        p = Product.objects.create(name='name', description='desc', price=17)

        good_form_data = {
            'text': 'comment text',
        }

        response = self.client.get(
            reverse('product', kwargs={'product_slug': p.slug}))

        self.assertNotIn('comment text', response.context['comments'])
        self.assertEqual(Comment.objects.count(), 0)

        self.client.post(
            reverse('product', kwargs={'product_slug': p.slug}),
            good_form_data)

        comment = Comment.objects.first()
        week_ago = timezone.now() - timedelta(days=7)
        comment.created_at = week_ago
        comment.save()

        response = self.client.get(
            reverse('product', kwargs={'product_slug': p.slug}))

        self.assertNotIn(comment, response.context['comments'])
        self.assertEqual(Comment.objects.count(), 1)


class TestProductForm(TestTaskTest):

    def test_add_product_form_fail(self):
        bad_form_data = {
            'name': '',
            'description': 'description for this product',
            'price': -1
        }

        form = ProductForm(data=bad_form_data)
        self.assertFalse(form.is_valid())

        response = self.client.post(reverse('index'), bad_form_data)
        self.assertFormError(
            response, 'form', 'price',
            'Ensure this value is greater than or equal to 0.')
        self.assertFormError(
            response, 'form', 'name', "This field is required.")

        self.assertEqual(Product.objects.count(), 0)

    def test_add_product_form_success(self):
        good_form_data = {
            'name': 'product name',
            'description': 'description for this product',
            'price': 9001
        }

        form = ProductForm(data=good_form_data)
        self.assertTrue(form.is_valid())

        self.client.post(reverse('index'), good_form_data)
        self.assertEqual(Product.objects.count(), 1)


class TestRegister(TestTaskTest):

    def test_register_form_fail(self):
        bad_form_data = {
            'username': '',
            'password1': 'some',
            'password2': 'notsome'
        }

        form = UserCreationForm(data=bad_form_data)
        self.assertFalse(form.is_valid())

        response = self.client.post(reverse('register'), bad_form_data)
        self.assertFormError(
            response, 'form', 'username', 'This field is required.')
        self.assertFormError(
            response, 'form', 'password2',
            "The two password fields didn't match.")

        self.assertEqual(User.objects.count(), 0)

    def test_register_form_success(self):
        good_form_data = {
             'username': 'username',
             'password1': 'password111',
             'password2': 'password111'
        }

        form = UserCreationForm(data=good_form_data)
        self.assertTrue(form.is_valid())

        self.client.post(reverse('register'), good_form_data)
        self.assertEqual(User.objects.count(), 1)


class TestProductModel(TestTaskTest):

    def test_slug_auto_creation(self):
        Product.objects.create(name='name', description='desc', price=17)

        self.assertEqual(Product.objects.all().count(), 1)
        product = Product.objects.first()
        self.assertEqual(product.slug, 'name')

    def test_correct_get_absolute_url(self):
        p = Product.objects.create(name='prodct', description='desc', price=17)

        self.assertEqual(Product.objects.all().count(), 1)
        response = self.client.get(p.get_absolute_url())
        self.assertEqual(p, response.context['product'])


class TestCommentModel(TestTaskTest):

    def test_comment_on_product_page(self):
        p = Product.objects.create(name='name', description='desc', price=17)
        c = Comment.objects.create(product=p, text='test text')

        response = self.client.get(p.get_absolute_url())
        self.assertIn(c, response.context['comments'])

    def test_create_comment(self):
        p = Product.objects.create(name='name', description='desc', price=17)
        c = Comment.objects.create(product=p, text='test text')

        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(c.author, 'Anonymous')

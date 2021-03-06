import unittest

from flask import abort, url_for
from flask_testing import TestCase
from os import getenv
from application import app, db
from application.models import User, Posts

class TestBase(TestCase):

    def create_app(self):
        #pass in test configurations
        config_name = "testing"
        app.config.update(
                SQLALCHEMY_DATABASE_URI='mysql+pymysql://'+str(getenv('FLASK_USER'))+':'+str(getenv('FLASK_PASSWORD'))+'@'+str(getenv('FLASK_HOST'))+'/'+str(getenv('FLASK_DB_TEST')))
        return app

    def setUp(self):
        # Will be called every test

        db.session.commit()
        db.drop_all()
        db.create_all()

        #create test admin and normal user
        admin = User(email="admin@admin.com", first_name="admin", last_name="admin", password="admin")
        user = User(email="tset@user.com", first_name="test", last_name="user", password="test")

        #save users to database
        db.session.add(admin)
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        # Annihilate tables after every test

        db.session.remove()
        db.drop_all()

class UnitTest(TestBase):

    def test_homepage_view(self):
        # Test homepage is accesible while logged out
        response = self.client.get(url_for('home'))
        self.assertEqual(response.status_code, 200)

    def test_posts(self):
        # Testmber of posts in posts table

        # create test post
        post = Posts(title="test", content="this is a test", user_id=2)

        # save post to database
        db.session.add(post)
        db.session.commit()

        self.assertEqual(Posts.query.count(), 1)

    def test_login_view(self):
        # test login page is accessible without login
        response = self.client.get(url_for('login'))
        self.assertEqual(response.status_code, 200)

    def test_user_view(self):
        # test user page is inaccessible without login
        target_url = url_for('account')
        redirect_url = url_for('login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

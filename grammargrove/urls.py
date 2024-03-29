"""
URL configuration for grammargrove project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

import index.views as index
from ops.urls import router as ops_router
from users.urls import router as user_router
from words.urls import router as word_router
from grammarrules.urls import router as grammarrules_router
from uservocabulary.urls import router as uservocabulary_router
from usergrammarrules.urls import router as usergrammarrules_router
from userpreferences.urls import router as userpreferences_router
from quiz.urls import router as quiz_router
from billing.urls import router as billing_router
from feedback.urls import router as feedback_router
from practicesession.urls import router as practice_session_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('-/', include(ops_router.urls), name="ops"),
    path('api/users/', include(user_router.urls), name="users"),
    path('api/words/', include(word_router.urls), name="words"),
    path('api/grammarrules/', include(grammarrules_router.urls), name="grammarrules"),
    path('api/uservocabulary/', include(uservocabulary_router.urls), name="uservocabulary"),
    path('api/usergrammarrules/', include(usergrammarrules_router.urls), name="usergrammarrules"),
    path('api/quiz/', include(quiz_router.urls), name="quiz"),
    path('api/practicesession/', include(practice_session_router.urls), name="quiz"),
    path('api/billing/', include(billing_router.urls), name="billing"),
    path('api/userpreferences/', include(userpreferences_router.urls), name="userpreferences"),
    path('api/feedback/', include(feedback_router.urls), name="feedback"),
    path('', index.home, name='home'),
    path('privacy-policy/', index.privacy_policy, name='privacy-policy'),
    path('login/', index.login, name='login'),
    path('subscription/', index.subscription, name='subscription'),
    path('dashboard/', index.create_view_route("Dashboard"), name='dashboard'),
    path('preferences/', index.create_view_route("Preferences"), name='preferences'),
    path('quiz/', index.create_view_route("Quiz"), name='quiz'),
    path('onboarding/', index.create_view_route("Onboarding"), name='onboarding'),
    path('vocabulary/', index.create_view_route("Vocabulary"), name='vocabulary'),
    path('grammar/', index.create_view_route("Grammar Rules"), name='grammar'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

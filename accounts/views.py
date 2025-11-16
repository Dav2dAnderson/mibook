import json
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
# Create your views here.


@method_decorator(csrf_protect, name='dispatch')
class SecureLoginView(View):
    def get(self, request):
        # login.html sahifani ko‘rsatish
        return render(request, "auth/login.html")
    
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session.cycle_key()
            return JsonResponse({
                "success": True,
                "redirect_url": "/",
                "csrf_token": get_token(request)
            })
        return JsonResponse({"success": False, "error": "Noto'g'ri login yoki parol."}, status=401)


class LogoutView(View):
    def get(self, request):
        return render(request, 'auth/logout.html')
    
    def post(self, request):
        logout(request)
        return redirect('login')
        # return JsonResponse({'success': True, 'redirect_url': "/accounts/login/"})


@method_decorator(csrf_protect, name='dispatch')
class SecureRegisterView(View):
    def get(self, request):
        return render(request, 'auth/register.html')
    
    def post(self, request):
        # ma'lumotlarni olish - JSON yoki form-data
        if request.content_type == "application/json":
            try:
                data = json.loads(request.body.decode("utf-8"))
            except (ValueError, json.JSONDecodeError):
                return JsonResponse({'success': False, "error": "Invalid JSON"}, status=400)

            username = data.get('username', "").strip()
            email = data.get('email', '').strip()
            password1 = data.get("password1", "")
            password2 = data.get("password2", "")
            # qo'shimcha maydonlarni olish ham mumkin (agar bo'lsa)
        else:
            # classical form submit (application/x-www-form-urlencoded)
            username = request.POST.get("username", "").strip()
            email = request.POST.get("email", "").strip()
            password1 = request.POST.get("password1", "")
            password2 = request.POST.get("password2", "")
        
        # oddiy required tekshiruvlar
        if not username or not email or not password1 or not password2:
            return JsonResponse({'success': False, "error": "Barcha maydonlar to'ldirilishi kerak."}, status=400)
        
        # parol tasdiqlanganini tekshirish
        if password1 != password2:
            return JsonResponse({'success': False, "error": "Parol tasdiqlanmadi."}, status=400)
        
        # username yoki email mavjudligini tekshirish
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, "error": "Bu username allaqachon band."}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({"success": False, "error": "Bu email allaqachon ishlatilgan."}, status=400)
        
        # email formatini tekshirish
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({"success": False, "error": "Noto'g'ri email manzil."}, status=400)
        
        # parol darajasini tekshirish 
        try:
            validate_password(password1)
        except ValidationError as exc:
            return JsonResponse({'success': False, "error": str(exc)}, status=400)
        
        # hammasi ok bo'lsa user yaratish
        user = User.objects.create_user(username=username, email=email, password=password1)
        
        # avtomatik login
        login(request, user)
        request.session.cycle_key() # session fixationga qarshi chora

        # javob qaytarish
        # agar AJAX/JSON so'rov bo'lsa JsonResponse, aks holda oddiy redirect
        if "application/json" in request.content_type:
            return JsonResponse({
                "success": True,
                "redirect_url": "/",
                "csrf_token": get_token(request)
            })
        else:
            return redirect("feed_page")
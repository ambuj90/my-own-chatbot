from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect
from .models import ChatMessage
from django.http import HttpResponse
from django.core.management import call_command



def run_migrations(request):
    call_command('migrate')
    return HttpResponse("✅ Migrations completed!")

# 🤖 Bot response using OpenAI
def get_bot_response(user_input):
    openai.api_key = settings.OPENAI_API_KEY

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# 🏠 Home page (chat UI)
# def home(request):
#     return render(request, 'chatbot/chat.html')

def home(request):
    messages = []
    if request.user.is_authenticated:
       messages = ChatMessage.objects.filter(user=request.user).order_by('timestamp')
    return render(request, 'chatbot/chat.html', {'messages': messages})

# 💬 Chatbot API endpoint
@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        user_message = request.POST.get("message")
        if not user_message:
            return JsonResponse({"response": "Please provide a message."})

        bot_reply = get_bot_response(user_message)
        return JsonResponse({"response": bot_reply})

    return JsonResponse({"error": "Invalid request method"}, status=405)

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'chatbot/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'chatbot/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        user_message = request.POST.get("message")
        bot_reply = get_bot_response(user_message)

        if request.user.is_authenticated:
            ChatMessage.objects.create(
                user=request.user,
                user_message=user_message,
                bot_response=bot_reply
            )

        return JsonResponse({"response": bot_reply})

    return JsonResponse({"error": "Invalid request method"}, status=405)
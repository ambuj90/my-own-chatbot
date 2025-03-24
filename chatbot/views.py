from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import ChatMessage

# Basic bot logic (can be replaced with OpenAI or Rasa)
def get_bot_response(user_input):
    if "hello" in user_input.lower():
        return "Hi there! How can I assist you today?"
    return "Sorry, I didn't understand that."

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        user_message = request.POST.get("message")
        bot_reply = get_bot_response(user_message)

        # Save to DB (optional)
        ChatMessage.objects.create(user_message=user_message, bot_response=bot_reply)

        return JsonResponse({"response": bot_reply})
    return JsonResponse({"error": "Invalid request"}, status=400)



def home(request):
    return render(request, 'chatbot/chat.html')
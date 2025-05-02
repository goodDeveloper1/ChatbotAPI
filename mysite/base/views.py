from django.shortcuts import render
from .decorators import rate_limit
from rest_framework.response import Response
from rest_framework.decorators import api_view
import groq
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
groq_ = groq.Groq(api_key=GROQ_API_KEY)


@api_view(["GET"])
def index(request):
    return Response({"Hello": "How are you?"})


@api_view(["POST"])
@rate_limit(3*60*60, 100)  # 3 requests per 10 seconds per IP
def chat(request):
    data = request.data
    comp = groq_.chat.completions.create(messages=data["messages"],
    model=data["model"])
    return Response(comp.dict(), content_type="application/json")


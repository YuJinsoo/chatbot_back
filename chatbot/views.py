from django.shortcuts import render
from django.views import View
from dotenv import load_dotenv
import openai
import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ConversationSerializer, ChatRoomSerializer

#함수형 뷰. 데코레이터
from rest_framework.decorators import api_view, permission_classes
# 클래스형 인증
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from .models import Conversation, ChatRoom

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


class ChatbotView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        conversations = request.session.get('conversations', [])
        # conversations 형식
        ## [{'prompt': '안녕하세요', 'response': '안녕하세요! 무엇을 도와드릴까요?'}, {...}]
        return render(request, 'chat.html', {'conversations': conversations})

    def post(self, request, *args, **kwargs):
        prompt = request.POST.get('prompt') # 내가 입력한 글
        if prompt:
            # 이전 대화 기록 가져오기
            session_conversations = request.session.get('conversations', [])
            previous_conversations = "\n".join([f"User: {c['prompt']}\nAI: {c['response']}" for c in session_conversations])
            print(previous_conversations)
            prompt_with_previous = f"{previous_conversations}\nUser: {prompt}\nAI:"

            # prompt_with_previous 들어가는 양식
            # User: 안녕하세요
            # AI: 안녕하세요! 무엇을 도와드릴까요?
            # User: 두번째 안녕하세요
            # AI: 다시 말씀해주세요. 무엇을 도와드릴까요?
            # User: 방금입력한거
            # AI: response
            model_engine = "text-davinci-003"
            completions = openai.Completion.create(
                engine=model_engine,
                prompt=prompt_with_previous,
                max_tokens=1024,
                n=5,
                stop=None,
                temperature=0.5,
            )
            response = completions.choices[0].text.strip()

            conversation = {'prompt': prompt, 'response': response}

            # 대화 기록에 새로운 응답 추가
            session_conversations.append(conversation)
            request.session['conversations'] = session_conversations

        return self.get(request, *args, **kwargs)
    

class ChatBotAnswer(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        conversations = request.session.get('conversations', [])
        # print(dir(request))
        # print(request.__dict__)
        print(type(request))
        print(dir(request.session))
        
        print(request.auth)
        # conversations 형식
        ## [{'prompt': '안녕하세요', 'response': '안녕하세요! 무엇을 도와드릴까요?'}, {...}]
        return Response({'conversations': conversations})

    def post(self, request, *args, **kwargs):
        # print(request.POST) # <QueryDict: {}>
        # print(request.data) # {'prompt': 'world'} 타입 dict
        # print(request.method) #POST
        # print(hasattr(request, "session")) #True
        # print(hasattr(request, "SESSION")) #False
        # print(request.session)
        
        # prompt = request.POST.get('prompt')
        prompt = request.data.get('prompt')
        print(prompt)
        if prompt:
            session_conversations = request.session.get('conversations', [])
            print(session_conversations)
            # previous_conversations = "\n".join([f"User: {c['prompt']}\nAI: {c['response']}" for c in session_conversations])
            # print(previous_conversations)
            # prompt_with_previous = f"{previous_conversations}\nUser: {prompt}\nAI:"
            
            input = f"User: {prompt}\nAI:"

            model_engine = "text-davinci-003"
            completions = openai.Completion.create(
                engine=model_engine,
                prompt=input, #prompt_with_previous,
                max_tokens=1024,
                n=5,
                stop=None,
                temperature=0.5,
            )
            response = completions.choices[0].text.strip()
            print(response)

            # 시리얼라이저에는 QuerySet? 즉 django orm 오브젝트가 들어가야함
            # conv = Conversation(prompt=prompt, response=response)
            # serializer = ConversationSerializer(conv)
            
            # data로는 dictionary 로 넣어줄 수 있습니다.
            serializer = ConversationSerializer(data={"prompt":prompt, "response": response})
            print(serializer)
            
            # serializer를 생성할 때 data로 생성하지 않으면 호출불가함.
            if serializer.is_valid():
                print('valid!')
                print(request.user)
                # TODO db에 저장하는 것 필요함
                return Response(serializer.data)
            
            return Response(serializer.errors)
        
        return Response({'message': 'prompt is not valid.'})


class DeleteChat(APIView):
    def post(self, request):
        pass


## 방 생성
class CreateChatRoom(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        serializer = ChatRoomSerializer(data={
            'creator': user,
            'title': request.data['title']
        })
        if serializer.is_valid():
            chatroom = serializer.create()
            chatroom.save()
            return Response({'message': 'create chatroom!'}, status=status.HTTP_200_OK)
        return Response({'message': 'fail to create chatroom'}, status=status.HTTP_400_BAD_REQUEST)


## 방 조회
class DetailChatRoom(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, roomid):
        pass


## 방 내용 확인
class DetailChatRoom(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        pass


## 방 삭제
class DeleteChatRoom(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        pass
    

# @api_view(['GET'])
# def hello_rest_api(request):
#     data = {'message': 'Hello, REST API!'}
#     return Response(data)

class Test(APIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]
    
    def get(self, request):
        print(request.query_params)
        # url = "http://127.0.0.1:8000/api/chatbot/test?name=very&a=10"
        # <QueryDict: {'name': ['very'], 'a': ['10']}>
        
        data = {'message': 'Hello, REST API!!'}
        return Response(data)
    
    def post(self, request):
        # print(request.META.keys())
        # 이 값을 settings의 CORS_ALLOWED_ORIGINS 에 추가하면 새로운 접속자도 가능하겠네요! 
        print(request.META.get("HTTP_ORIGIN"))
        # print(request.META.get("HTTP_MY_HEADER")) # 헤더에 추가한 내용은 request.META에서 HTTP_대문자~~로 읽어올 수 있습니다.
        data = {"message": "post request"}
        return Response(data)

hello_rest_api = Test.as_view()
import requests
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView


class FacebookLoginAPIView(APIView):
    FACEBOOK_APP_ID = ''
    FACEBOOK_SECRET_CODE = ''
    APP_ACCESS_TOKEN = '{}|{}'.format(
        FACEBOOK_APP_ID,
        FACEBOOK_SECRET_CODE,
    )

    def post(self, request):
        token = request.data.get('token')
        if not token:
            raise APIException('token require')

        # 프론트로부터 전달받은 token을 Facebook의 debug_token API를 사용해
        # 검증한 결과를 debug_result에 할당
        debug_result = self.debug_token(token)
        return Response(debug_result)

    def debug_token(self, token):
        """
        주어진 token으로 FacebookAPI의 debug_token을 실행, 결과를 리턴
        :param token: 프론트엔드에서 유저가 페이스북 로그인 후 반환된 authResponse내의 accessToken값
        :return: FacebookAPI의 debug_token실행 후의 결과
        """
        url_debug_token = 'https://graph.facebook.com/debug_token'
        url_debug_token_params = {
            'input_token': token,
            'access_token': self.APP_ACCESS_TOKEN,
        }
        response = requests.get(url_debug_token, url_debug_token_params)
        result = response.json()
        if 'error' in result['data']:
            raise APIException('token invalid')
        return result
from flask import Flask, redirect, request, jsonify
from flask import render_template
from flask_sock import Sock

import requests
import global_vars

app = Flask(__name__, static_url_path='')
sock = Sock(app)

@app.context_processor
def inject_user():
    return vars(global_vars)

@app.route('/')
def index():
    return render_template('home.html')

@app.route("/kakao")
def kakaoLogin():
    client_id = "a68f2caf96ab60881b4cf7e9b6b0b2db"
    redirect_uri = "http://127.0.0.1:5000/kakaoCallback"
    kakao_url = f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    return redirect(kakao_url)

@app.route("/kakaoCallback")
def kakaoCallback():
    code = request.args.get("code")
    client_id = "a68f2caf96ab60881b4cf7e9b6b0b2db"
    redirect_uri = "http://127.0.0.1:5000/kakaoCallback"

    token_request = requests.get(f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}")
    token_json = token_request.json()
    print(token_json)

    access_token = token_json.get("access_token")
    profile_request = requests.get("https://kapi.kakao.com/v2/user/me", headers={"Authorization" : f"Bearer {access_token}"},)
    profile_data = profile_request.json()
    print(profile_data) #사용자 정보
    #정보들을 세션이나 JWT에 저장하여 로그인 상태 유지 (백엔드에서 구현)
    #정보들을 db에 저장하여 자동회원가입 기능 (백엔드에서 구현)
    return profile_data

@app.route("/naver") 
def naverLogin():
    client_id = "YXVKk_tK3dZoXiCKDHdQ"
    redirect_uri = "http://127.0.0.1:5000/naverCallback"
    naver_url = f"https://nid.naver.com/oauth2.0/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    return redirect(naver_url)



@app.route("/naverCallback")
def naverCallback():
    params = request.args.to_dict()
    code = params.get("code")

    client_id = "YXVKk_tK3dZoXiCKDHdQ"
    client_secret = "AiwIoCGEqj"
    redirect_uri = "http://127.0.0.1:5000/naverCallback"

    token_request = requests.get(f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}")
    token_json = token_request.json()
    print(token_json)

    access_token = token_json.get("access_token")
    profile_request = requests.get("https://openapi.naver.com/v1/nid/me", headers={"Authorization" : f"Bearer {access_token}"},)
    profile_data = profile_request.json()

    print(profile_data) #사용자 정보
    #정보들을 세션이나 JWT에 저장하여 로그인 상태 유지 (백엔드에서 구현)
    #정보들을 db에 저장하여 자동회원가입 기능 (백엔드에서 구현)
    return profile_data

@app.route("/google")
def googleLogin():
    client_id = "226449188999-bihphp3jma0kkm8derbui6gaik89ura7.apps.googleusercontent.com"
    redirect_uri = "http://127.0.0.1:5000/googleCallback"
    scope = "https://www.googleapis.com/auth/userinfo.email " + \
                "https://www.googleapis.com/auth/userinfo.profile"
    
    google_auth_api = "https://accounts.google.com/o/oauth2/v2/auth"
    google_url =  f"{google_auth_api}?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"
    return redirect(google_url)


@app.route("/googleCallback", methods=['GET'])
def googleCallback():
    params = request.args.to_dict()
    code = params.get("code")
    client_id = "226449188999-bihphp3jma0kkm8derbui6gaik89ura7.apps.googleusercontent.com"
    client_secret = "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"
    google_token_api = "https://oauth2.googleapis.com/token"
    redirect_uri = "http://127.0.0.1:5000/googleCallback"
    grant_type = 'authorization_code'


    profile_request = requests.post(google_token_api, data=dict(
        code=code,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        grant_type=grant_type
    ))

    token_json = profile_request.json()
    access_token = token_json.get("access_token")
    print(access_token)

    profile_request = requests.get("https://www.googleapis.com/oauth2/v2/userinfo", headers={"Authorization" : f"Bearer {access_token}"},)
    profile_data = profile_request.json()
    print(profile_data) #사용자 정보
    #정보들을 세션이나 JWT에 저장하여 로그인 상태 유지 (백엔드에서 구현)
    #정보들을 db에 저장하여 자동회원가입 기능 (백엔드에서 구현)
    return profile_data



@app.route('/login')
def login():
    return render_template('login.html', id='login')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html', id='chatbot')

def create_page(path):
    def inner():
        return render_template('page.html', id=path)
    return inner

for path in ['mypet', 'recommend', 'notification', 'shopping']:
    app.add_url_rule(f'/{path}', path, create_page(path))

@sock.route('/echo')
def echo(ws):
    while True:
        data = ws.receive()
        ws.send(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

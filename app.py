from flask import Flask, request, jsonify, os
import requests

app = Flask(__name__)

GROUP_ID = os.getenv('GROUP_ID')  # Replace with your group ID
RANK_ID = os.getenv('RANK_ID')  # Replace with the rank ID you want to assign
COOKIE = os.getenv('COOKIE')  # Replace with your .ROBLOSECURITY cookie

session = requests.Session()
session.cookies['.ROBLOSECURITY'] = COOKIE

def get_xcsrf_token():
    response = session.post('https://auth.roblox.com/v2/logout', headers={"Content-Type": "application/json"})
    return response.headers['X-CSRF-TOKEN']

@app.route('/rank-user', methods=['POST'])
def rank_user():
    data = request.get_json()
    user_id = data.get('userId')

    if not user_id:
        return jsonify({'message': 'User ID is required'}), 400

    try:
        xcsrf_token = get_xcsrf_token()
        url = f'https://groups.roblox.com/v1/groups/{GROUP_ID}/users/{user_id}'
        headers = {
            'X-CSRF-TOKEN': xcsrf_token,
            'Content-Type': 'application/json'
        }
        response = session.patch(url, json={'roleId': RANK_ID}, headers=headers)

        if response.status_code == 200:
            return jsonify({'message': 'User ranked successfully!'}), 200
        else:
            return jsonify({'message': 'Failed to rank user.', 'details': response.text}), response.status_code

    except Exception as e:
        print(e)
        return jsonify({'message': 'Server error.'}), 500

if __name__ == '__main__':
    app.run(debug=True)

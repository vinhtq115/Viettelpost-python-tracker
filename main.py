import argparse
import requests
import numpy as np
import base64
from cv2 import cv2
from datamodel import TrackingOrder


def getCaptchaChallenge():
    try:
        getCaptcha = requests.get('https://api.viettelpost.vn/api/orders/getCaptcha').json()
        if getCaptcha.get('status') != 200 or getCaptcha.get('data') is None:
            return None

        data = getCaptcha.get('data')
        if data.get('id') is None or data.get('captcha') is None:
            return None
        else:
            encoded_png = data.get('captcha').split(',')[1]
            img_bytes = np.frombuffer(base64.b64decode(encoded_png), np.uint8)
            img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
            return data.get('id'), img

    except (Exception,) as e:
        print(e)
        return None


def getTrackingInfo(captcha_id: str, captcha_answer:str, tracking_number: str):
    try:
        request_data = {
            'captcha': captcha_answer,
            'id': captcha_id,
            'orders': tracking_number
        }
        server_response = requests.post('https://api.viettelpost.vn/api/orders/viewTrackingOrders',
                                        json=request_data).json()
        if server_response.get('status') != 200 or server_response.get('data') is None:
            return None

        return TrackingOrder(server_response.get('data')[0])
    except (Exception,) as e:
        print(e)
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Lấy thông tin vận chuyển của Viettelpost.')
    parser.add_argument('tracking_number', help='Mã vận đơn')

    opt = parser.parse_args()
    tracking_number = opt.tracking_number

    # Get captcha challenge
    captcha = getCaptchaChallenge()
    if captcha is None:
        print('Lỗi lấy captcha.')
        exit(1)

    captcha_id, captcha_img = captcha

    cv2.imshow('Captcha', captcha_img)
    cv2.waitKey(1)

    captcha_answer = input('Nhập mã captcha: ')
    print()
    cv2.destroyAllWindows()

    tracking = getTrackingInfo(captcha_id, captcha_answer, tracking_number)
    print(tracking)


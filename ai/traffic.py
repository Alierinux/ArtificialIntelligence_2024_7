import requests
import base64
import cv2 as cv


def get_res(img, name):
    _, encoded_image = cv.imencode('.jpg', img)
    base64_image = base64.b64encode(encoded_image)
    if name == "vehicle_detect":
        access_token = '24.d76ab3bf74bccbad3c59247e8a89e606.2592000.1722737853.282335-89669108'
        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/vehicle_detect"
        params = {"image": base64_image}
    elif name == "body_attr":
        access_token = '24.4c7dae638c383ffb77f0464552ed10e1.2592000.1722761650.282335-90650439'
        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_attr"
        params = {"image": base64_image, 'type': "gender"}
    elif name == "advanced_general":
        access_token = '24.49a329134f33aac273783c418310f8c9.2592000.1722778224.282335-89523302'
        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general"
        params = {"image": base64_image, "baike_num": 999}
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    return requests.post(request_url, data=params, headers=headers)


def vehicle_detect(img):
    response = get_res(img, "vehicle_detect")
    print(response.text)
    num = 0
    if response:
        data = response.json()
        num = data['vehicle_num']['car']
        for item in data['vehicle_info']:
            location = item['location']
            x1 = location['left']
            y1 = location['top']
            x2 = x1 + location['width']
            y2 = y1 + location['height']
            cv.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            # 定义要绘制的文字
            text = item['type']
            position = (x1, y1 - 2)
            font = cv.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            color = (0, 0, 255)  # 红色
            thickness = 2
            img = cv.putText(img, text, position, font, font_scale, color, thickness, cv.LINE_AA)
    return img, num


def body_attr(img):
    response = get_res(img, "body_attr")
    print(response.text)
    num = 0
    if response:
        data = response.json()
        num = data['person_num']  # 获取检测到的人数
        for item in data['person_info']:
            location = item['location']
            x1 = location['left']
            y1 = location['top']
            x2 = x1 + location['width']
            y2 = y1 + location['height']
            cv.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            # 定义要绘制的文字（可以是得分）
            if item['attributes'] != "":
                # text = item['attributes']['gender']['name']
                text = "person"
            else:
                text = ""
            position = (x1, y1 - 2)
            font = cv.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            color = (0, 0, 255)  # 红色
            thickness = 2
            # 在图像上绘制文字
            img = cv.putText(img, text, position, font, font_scale, color, thickness, cv.LINE_AA)
    return img, num


def general(img,capture_flag):
    num = -1
    msg = ""
    print("capture_flag:",capture_flag)
    if capture_flag:
        print("now")
        response = get_res(img, "advanced_general")
        print(response.text)
        if response:
            num = response.json()['result_num']
            msg = response.json()['result']
        capture_flag = False
    else:
        print("等待点击\"开始识别\"ing")
    return msg, num, capture_flag

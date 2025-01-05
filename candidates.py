from flask import Blueprint, jsonify
import base64
from http import HTTPStatus
from Routes.class_va import VA

can_routes=Blueprint("can_routes",__name__)

#這個應該是database要存的
class Candidates:
    def __init__(self) -> None:
        self.candidates_num=2
        self.candidates_names=["宋鴻明","陳冠廷"]
        self.candidates_img_path=["./1.jpg","./2.jpg"]
        self.va=[VA(),VA()]#TODO

Candidate=Candidates()


def convert_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


#可以用<img src="data:image/jpeg;base64,{{ image_base64 }}" alt="example image">解碼

@can_routes.route('/get_candidates')
def return_candidates_info():
    #Done
    try:
        candidates={}
        for id in range(Candidate.candidates_num):
            with open("Images"+Candidate.candidates_img_path[id], "rb") as image_file:
                candidates[str(id)]={"names":Candidate.candidates_names[id],"img":convert_image_to_base64(image_file)}
        return jsonify(candidates),HTTPStatus.OK
    except Exception as e:
        return jsonify({'message': str(e)}), HTTPStatus.BAD_REQUEST
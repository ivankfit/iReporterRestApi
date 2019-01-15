from flask import Flask,json,jsonify,Blueprint,request
from flask import current_app as app
import os
import datetime
from werkzeug import secure_filename
from app.handy.utils import utils

incident=Blueprint('incident',__name__)
incidents=[]
utils=utils()

@incident.route('/',methods=['GET'])
def index():
    return jsonify({'message':"welcome"}),200

@incident.route('/api/v1/red-flags',methods=['POST'])
def postred_flags():
    data = request.form
    ctype=str(request.headers['Content-Type']).split(';')[0]
    if ctype!='multipart/form-data':
          return jsonify({'msg':'request header type should be form-data'}),400

    if not 'comment' in data:
          return jsonify({'msg': 'comment missing! please supply in the comment'}), 400

    if len(data['comment']) <5:
          return jsonify({'message': 'comment too short! please supply long text'}), 400

    if not 'location' in data:
          return jsonify({'msge': 'location is missing'}),400
    
    PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
    UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
    image=request.files['image']
    img_name = secure_filename(image.filename)
    if not allowed_file(image.filename):
          return jsonify({'msg':'File should be an image '}),400


    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    createfolder(app.config['UPLOAD_FOLDER'])
    saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
    image.save(saved_path)   
    
    latlgvalues=utils.get_latlong(data['location'])

    incident={
          "id":len(incidents)+1,
          "created_on":datetime.datetime.utcnow(),
          "created_by":1,
          "type":data['type'],
          "location":str(latlgvalues),
          "status":'draft',
          "comment":data['comment'],
          'image':str(saved_path)


    }
    incidents.append(incident)
    return jsonify({"success":True,"incident":incident.get('id')}),201

@incident.route('/api/v1/red-flags',methods=['GET'])
def getred_flags():
        return jsonify({'status': 200, 'data':incidents})

  #getting a specific red flag
@incident.route('/api/v1/red-flags/<int:id>',methods=['GET'])
def get_specific_red_flag(id):

      if not item_exists(id, incidents):
            return jsonify({'msg':'item not found'}), 404
      #find the item by id
      for incident in incidents:
            if incident['id'] == id:
                  return jsonify({'data' :incident}),200
      

@incident.route('/api/v1/red-flags/<int:id>/location', methods=['PATCH'])
def edit_location_of_specific_redflag(id):
      data=request.form
      latlgvalues=utils.get_latlong(data['location'])
      if not item_exists(id, incidents):
            return jsonify({'msg': 'item not found'}), 404

            #TODO VALIDATE
      for i in incidents:
            if i['id'] == id:
                  i['location'] =str(latlgvalues)
                  return jsonify({'msg': 'location updated'}), 200
      

@incident.route('/api/v1/red-flags/<int:id>/comment', methods=['PATCH'])
def edit_comment_of_specific_redflag(id):
      if not item_exists(id, incidents):
            return jsonify({'msge': 'item not found'}), 404
      data=request.form
            #TODO VALIDATE
      for i in incidents:
            if i['id'] == id:
                  i['comment'] = data['comment']

                  return jsonify({'msg': 'comment updated'}), 200


@incident.route('/api/v1/red-flags/<int:id>',methods=['PUT'])
def update_specific_red_flag(id):
      if not item_exists(id,incidents):
            return jsonify({'msg':'item not found'}),404
      #CREATE A NEW LIST OBJECT
      data=request.form
            #TODO VALIDATE
      for i in incidents:
            if i['id'] == id:
                  incident_update={
                  "id":id,
                  "last_updated_on":datetime.datetime.utcnow(),
                  "created_by":1,
                  "type":data['type'],
                  "location":data['location'],
                  "status":"draft",
                  "comment":data['comment']
             }
                  i.update(incident_update)
                
      return jsonify({"msg":"updated"}),200

@incident.route('/api/v1/red-flags/<int:id>',methods=['DELETE'])
def delete_red_flags(id):
    #find the item by id
    if not item_exists(id,incidents):
       return jsonify({'msg':'item not found'}),404

    for incident in incidents:
        if incident['id']==id:
           incidents.remove(incident)
    return jsonify({ 'status': 200, 'Message': "item deleted"})
    

def item_exists(item_id,itemlist):
      for item in itemlist:
            if item['id']==item_id:
                  return True
      return False


def createfolder(local_dir):
      newpath=local_dir
      if not os.path.exists(newpath):
            os.makedirs(newpath)
      return newpath


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpeg', 'gif', 'jpg'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
import boto3
#from boto3.dynamodb.conditions import Key,Attr
import face_recognition
import pickle
import os
import numpy as np

s3 = boto3.resource('s3')
db = boto3.resource('dynamodb',region_name='us-east-1')

input_bucket = "input-bucket-project2"
output_bucket = "output-bucket-project2"
table_name = db.Table('People_data')



# Function to read the 'encoding' file
def open_encoding(filename):
	file = open(filename, "rb")
	data = pickle.load(file)
	file.close()
	return data

def face_recognition_handler(event, context):	
	
	# get the Video
	obj_key = event['Records'][0]['s3']['object']['key']
	
	s3.meta.client.download_file(input_bucket, obj_key, '/tmp/'+obj_key)
	
	
	frames_dir = "/tmp/"
	os.system( 'ffmpeg '+ '-i '+ frames_dir+obj_key+ ' -r '+ '1 '+ frames_dir+'image-%3d.jpeg')

	encoding_data = open_encoding('encoding')


	# perform face recognition using inbuilt library.
	for i in os.listdir(frames_dir):
		if i.startswith('image'):

			image = face_recognition.load_image_file(frames_dir+i)
			frame_encoding = face_recognition.face_encodings(image)[0]

			match = face_recognition.compare_faces(encoding_data['encoding'],frame_encoding)
			
	
			if True in match:
				name_index = match.index(True)
				name_found = encoding_data['name'][name_index] 
		
				# Check with DynamoDB then.
				response = table_name.get_item(Key={ 'name': name_found })
				item = response['Item']
				keyname = obj_key.split('.')[0]
				
				with open('/tmp/'+keyname,'w') as f:
					f.write(item['name'] + ',' + item['major'] + ',' + item['year'])
				
				s3.meta.client.upload_file('/tmp/'+keyname, output_bucket, keyname)
				break
	os.system("rm /tmp/image*jpeg")
	os.system("rm /tmp/test_*")
	
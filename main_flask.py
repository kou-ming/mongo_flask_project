from flask import Flask
from flask import url_for,redirect, render_template, request
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["song"]



app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def insert():
    mycol = mydb["song_info"]
    mytag = mydb["tag_info"]
    song_list = []
    tag_list = []
    for song in mycol.find():
        song_list.append(song['SongName'])
    for tag in mytag.find():
        tag_list.append(tag['TagName'])
        
    if request.method == 'POST':
        mycol = mydb["song_info"]
        SongName = request.values['SongName']
        AuthName = request.values['AuthName']
        LikeLevel = request.values['LikeLevel']
        Select_Tag = request.form.getlist('tag')
        mycol.insert_one({"SongName": SongName, "Auth": AuthName, "LikeLevel": LikeLevel, "Tag": Select_Tag})
        song_list.append(SongName)
        return render_template('insert.html', info = song_list, tags = tag_list)
        # if SongName != '':
        #     return insert()
            # return render_template('insert.html', info = song_list, tags = tag_list)

    return render_template('insert.html', info = song_list, tags = tag_list)

@app.route('/tag', methods = ['GET', 'POST'])
def tag():
    mytag = mydb["tag_info"]
    tag_list = []
    # for tag in tag.find():
    #     song_list.append(song['name'])
    if request.method == 'POST':
        TagName = request.values['TagName']
        mytag.insert_one({"TagName": f"{TagName}"})

    return render_template('tag.html')

# @app.route('/')
# def index():
#     return 'Welcome!!!'


@app.route('/write', methods=['GET', 'POST'])
def write():
    mycol = mydb["song_info"]
    mylist = [
        {"name": "安平之光", "auth": "イルカポリス 海豚刑警"},
        {"name": "月旁月光", "auth": "怕胖團"}
    ]
    mycol.insert_many(mylist)
    return insert()


if __name__ == '__main__':
    app.debug = True
    app.run()
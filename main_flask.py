from flask import Flask
from flask import url_for,redirect, render_template, request
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["song"]



app = Flask(__name__)

@app.route('/insert', methods = ['GET', 'POST'])
def insert():
    mysong = mydb["song_info"]
    mytag = mydb["tag_info"]
    song_list = []
    tag_list = []
    for song in mysong.find():
        song_list.append(song['SongName'])
    for tag in mytag.find():
        tag_list.append(tag['TagName'])

    myauth = mydb["author_info"]
    auth_list = []
    for auth in myauth.find():
        auth_list.append(auth['AuthTag'])

    if request.method == 'POST':
        SongName = request.values['SongName']
        AuthName = request.values['AuthName']
        LikeLevel = request.values['LikeLevel']
        Select_Tag = request.form.getlist('Tag')
        if SongName == '' or AuthName == '' :
            info = '歌曲名或作者名不得為空'
        else:
            if len(list(myauth.find({"AuthTag": AuthName}))) == 0:
                myauth.insert_one({"AuthTag": AuthName})
                auth_list.append(AuthName)
            mysong.insert_one({"SongName": SongName, "Auth": AuthName, "LikeLevel": LikeLevel, "Tag": Select_Tag})
            song_list.append(SongName)
            info = f"成功新增！ 歌曲名：{SongName}, 作者名：{AuthName}, 喜好程度：{LikeLevel}, 標籤："
            for tag in Select_Tag:
                info += tag + ' '
        return render_template('insert.html', info = info, tags = tag_list, auths = auth_list)
        # if SongName != '':
        #     return insert()
            # return render_template('insert.html', info = song_list, tags = tag_list)

    return render_template('insert.html', tags = tag_list, auths = auth_list)

@app.route('/tag', methods = ['GET', 'POST'])
def tag():
    mytag = mydb["tag_info"]
    tag_list = []
    for tag in mytag.find():
        tag_list.append(tag['TagName'])
    # for tag in tag.find():
    #     song_list.append(song['name'])
    if request.method == 'POST':
        TagName = request.values['TagName']
        mytag.insert_one({"TagName": f"{TagName}"})

    return render_template('tag.html')

@app.route('/songlist', methods = ['GET', 'POST'])
def songlist():
    mysong = mydb['song_info']
    song_list = []
    for song in mysong.find():
        song_list.append(song)

    mytag = mydb["tag_info"]
    tag_list = []
    for tag in mytag.find():
        tag_list.append(tag['TagName'])

    myauth = mydb["author_info"]
    auth_list = []
    for auth in myauth.find():
        auth_list.append(auth['AuthTag'])

    # if request.method == 'POST':
    #     TagName = request.values['TagName']

    return render_template('songlist.html', songlist = song_list, song_num = len(song_list), taglist = tag_list, authlist = auth_list)

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

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('test.html')

# @app.route('/home', methods=['GET', 'POST'])
# def home():
#     return render_template('home.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
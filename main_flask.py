from flask import Flask
from flask import url_for,redirect, render_template, request, jsonify
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["song"]



app = Flask(__name__)

def or_filter(or_filter_list):
    print('or_filter')
    song_list = []
    mysong = mydb["song_info"]
    for or_song_name in or_filter_list:
        for song in mysong.find({"Tag": or_song_name}):
            if song not in song_list:
                # print(song)
                song_list.append(song)
    return song_list

def and_filter(song_list, and_filter_list):
    print('and_filter\n')
    new_song_list = song_list
    for and_song_tag in and_filter_list:
        new_song_list = []
        for song in song_list:
            if and_song_tag in song['Tag']:
                new_song_list.append(song)
        song_list = new_song_list
    print('and_filter_end')
    return new_song_list


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
        Select_Tag.append(AuthName)
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
    info = '尚未選擇任何選項'
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


    if request.method == 'POST':
        info = ''
        data = request.get_json()
        button_values = data.get('buttons', [])
        or_filter_list = []
        and_filter_list = []
        pre_filter = 0
        input_num = 0;
        # print("接收到的按鈕值:", button_values)
        flag = True     #排序是否有錯
        for button_name in button_values:
            if button_name[0] != str(input_num):
                info = '過濾器排序有問題'
                flag = False
                break
            else:
                info += button_name[2:] + ' '
                print(button_name[2:])
            input_num = (input_num+1)%2

            if button_name[0] == '1':
                if button_name[2:] == 'OR':
                    pre_filter = 0
                elif button_name[2:] == 'AND':
                    pre_filter = 1
            else:
                if pre_filter == 0:
                    or_filter_list.append(button_name[2:])
                elif pre_filter == 1:
                    and_filter_list.append(button_name[2:])
        if len(button_values) != 0 and flag:
            song_list = []
            song_list = or_filter(or_filter_list)
            song_list = and_filter(song_list, and_filter_list)
        elif not flag:
            song_list = []
        else:
            song_list = []
            for song in mysong.find():
                song_list.append(song)
            info = '全歌單'
        for song in song_list:
            song['_id'] = str(song['_id'])
        response_data = {
            'songs': song_list,
            'len': len(song_list),
            'info': info
        }
        return jsonify(response_data)

    return render_template('songlist.html', songlist = song_list, song_num = len(song_list), taglist = tag_list, authlist = auth_list, info=info)

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
    if request.method == 'POST':
        data = request.get_json()
        button_values = data.get('buttons', [])
        print("接收到的按鈕值:", button_values)

    return render_template('test.html')

# @app.route('/home', methods=['GET', 'POST'])
# def home():
#     return render_template('home.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
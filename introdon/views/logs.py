#
# @app.route('/')
# # @login_required
# def setting_game():
#
#     return render_template('games/index.html')
#
# @app.route('/games/start', methods=['POST'])
# # @login_required
# def start_game():
#
#     # songDBのレコード数をカウント
#     songs_count = Song.query.count()
#
#     # 登録曲が少なすぎる場合は「曲が少なくて作れません」
#     if songs_count < MAX_QUESTION:
#         flash('曲が少なくて作れません')
#     else:
#         # 正解を作る
#         correct = []
#         for i in range(MAX_QUESTION):
#             while True:
#                 index = random.randint(1, songs_count)
#                 if index not in correct:
#                     correct.append(index)
#                     break
#         # 選択肢を作成
#         select = [[0 for i in range(4)] for j in range(10)]
#         for i in range(MAX_QUESTION):
#             select[i][random.randint(0, MAX_SELECT -1)] = correct[i]
#             for j in range(MAX_SELECT):
#                 if select[i][j] == 0:
#                     while True:
#                         index = random.randint(1, songs_count)
#                         if index not in select[i]:
#                             select[i][j] = index
#                             break
#         # メソッド引数用のdictを作る
#         records={}
#         for i in range(MAX_QUESTION):
#             records["question" + str(i+1) + "_correct_track_id"] = correct[i]
#             for j in range(MAX_SELECT):
#                 records["question" + str(i + 1) + "_select" + str(j +1) + "_track_id"] = select[i][j]
#
#         item = Game(**records)
#         db.session.add(item)
#         db.session.commit()
#
#     flash('新しくゲームが作成されました')
#     return render_template('games/start.html')
#


#
# # song登録画面
# @app.route('/admin/song', methods=['POST'])
# # @login_required
# def add_song():
#     term = request.form['term']
#     limit = request.form['limit']
#     attribute = request.form['attribute']
#
#     # api接続
#     ITUNES_URI = 'https://itunes.apple.com/search'
#
#     params = {
#         'media': 'music',
#         'country': 'jp',
#         'lang': 'ja_jp',
#         'term': term,
#         'limit': limit,
#         'attribute': attribute
#     }
#
#     if attribute == 'all':
#         params.pop('attribute')
#
#     res = requests.get(ITUNES_URI, params)
#     _status_code = res.status_code
#     _json = res.json()
#
#     if _status_code == 200:
#         track_ids = []
#         for result in _json['results']:
#             track_ids.append(result['trackId'])
#
#         duplicate = Song.query.with_entities(Song.track_id).filter(Song.track_id.in_(track_ids)).all()
#         dup_track_id = []
#         for dup in duplicate:
#             dup_track_id.append(dup[0])
#         print('duplicateTrackId: ', dup_track_id)
#
#         items = []
#         for result in _json['results']:
#             if result['trackId'] not in dup_track_id:
#                 dt = result['releaseDate']
#                 dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
#
#                 item = Song(
#                     track=result['trackName'],
#                     track_id=result['trackId'],
#                     artist=result['artistName'],
#                     artist_id=result['artistId'],
#                     genre=result['primaryGenreName'],
#                     jacket_img=result['artworkUrl100'],
#                     preview=result['previewUrl'],
#                     release_date=dt
#                 )
#                 items.append(item)
#
#         db.session.add_all(items)
#         db.session.commit()
#
#         flash('新曲が登録されました')
#
#     else:
#         flash('楽曲の取得に失敗しました・・')
#         print('status code: ', _status_code)
#
#     return redirect('/admin/song')
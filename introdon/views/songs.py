from datetime import datetime

import requests
from flask import request, redirect, flash

from introdon import app, db
from introdon.models.songs import Song


# song登録画面
@app.route('/admin/song', methods=['POST'])
def add_song():
    term = request.form['term']
    limit = request.form['limit']
    attribute = request.form['attribute']

    # api接続
    ITUNES_URI = 'https://itunes.apple.com/search'

    params = {
        'media': 'music',
        'country': 'jp',
        'lang': 'ja_jp',
        'term': term,
        'limit': limit,
        'attribute': attribute
    }

    if attribute == 'all':
        params.pop('attribute')

    res = requests.get(ITUNES_URI, params)
    _status_code = res.status_code
    _json = res.json()

    if _status_code == 200:
        # todo:Duplicateエラーしないようにする。同じ曲をinsertしない
        # すでに曲が登録している場合は省く
        track_ids = []
        for result in _json['results']:
            track_ids.append(result['trackId'])

        duplicate = Song.query.with_entities(Song.track_id).filter(Song.track_id.in_(track_ids)).all()
        dup_track_id = []
        for dup in duplicate:
            dup_track_id.append(dup[0])
        print('duplicateTrackId: ', dup_track_id)

        items = []
        for result in _json['results']:
            if result['trackId'] not in dup_track_id:
                dt = result['releaseDate']
                dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))

                item = Song(
                    track=result['trackName'],
                    track_id=result['trackId'],
                    artist=result['artistName'],
                    artist_id=result['artistId'],
                    genre=result['primaryGenreName'],
                    jacket_img=result['artworkUrl100'],
                    preview=result['previewUrl'],
                    release_date=dt
                )
                items.append(item)

        db.session.add_all(items)
        db.session.commit()

        flash('新曲が登録されました')

    else:
        flash('楽曲の取得に失敗しました・・')
        print('status code: ', _status_code)

    return redirect('/admin/song')

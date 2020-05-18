<template>
  <div>
    <h3>Setting</h3>

    <h1>ゲームをはじめよう</h1>
    <p>曲を絞り込む</p>

    <div class="form-group">
      <label for="inputArtist">アーティスト</label>
      <input class="form-control" id="inputArtist" placeholder="特定しない" type="text" v-model="setData.artist">

      <label for="inputGenre">ジャンル</label>
      <input class="form-control" id="inputGenre" placeholder="特定しない" type="text" v-model="setData.genre">
    </div>

    <label for="inputReleaseFrom">年代</label>
    <div class="form-group form-inline" id="inputReleaseFrom">

      <select class="form-control" name="release_from" v-model="setData.release_from">
        <option selected v-bind:value="init_from">特定しない</option>
        <option :key="age"
                v-for="age in ages">
          {{age}}
        </option>
      </select>

      <i class="fas fa-long-arrow-alt-right fa-fw fa-2x"></i>

      <select class="form-control" id="inputReleaseEnd" name="release_end" v-model="setData.release_end">
        <option selected v-bind:value="init_end">特定しない</option>
        <option :key="age"
                v-for="age in ages">
          {{age}}
        </option>
      </select>
    </div>

    <button class="btn btn-primary" v-on:click="postJson">スタート</button>

  </div>
</template>

<script>
  export default {
    name: "Setting",
    data() {
      return {
        init_from: 1900,
        init_end: 2100,
        ages: [1960, 1970, 1980, 1990, 2000, 2010, 2020],
        setData: {
          artist: '',
          genre: '',
          release_from: 1900,
          release_end: 2100,
        }
      }
    },
    methods: {
      postJson() {
        this.axios.post('/game/start', this.setData)
            .then((response) => {
              console.log(response);
            })
            .catch((e) => {
              console.log(e);
            });
      }
    }
  }
</script>

<style scoped>

</style>

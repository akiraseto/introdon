<template>
  <div>

    <h5>Home</h5>

    <h1 class="display-1">クイズ! Intro Don!!</h1>

    <div class="form-group">
      <label for="inputArtist">ユーザーネーム</label>
      <input class="form-control" id="inputArtist" placeholder="特定しない" type="text" v-model="setData.artist">

      <label for="inputGenre">パスワード</label>
      <input class="form-control" id="inputGenre" placeholder="特定しない" type="text" v-model="setData.genre">
    </div>

    <button class="btn btn-primary" v-on:click="postJson">ログイン</button>

    <button class="btn btn-secondary m-3 inline" onclick="location.href='/user/new'">アカウントを作る</button>

    <button class="btn btn-secondary m-3 inline" onclick="location.href='/game/setting'">簡易版で遊ぶ</button>


  </div>


</template>

<script>
  export default {
    name: "Home",
    data() {
      return {
        setData: {
          username: '',
          password: '',
        },
        getData: {},

      }
    },
    methods: {
      postJson() {
        this.axios.post('/', this.setData)
            .then((response) => {
              console.log(response);
            })
            .catch((e) => {
              console.log(e);
            });
      },
      getJson() {
        this.axios.get('/')
            .then((response) => {
              this.getData = response.data;
              console.log(response.data);
            })
            .catch((e) => {
              console.log(e);
            });
      }
    },
    created() {
      this.getJson()
    },


  }
</script>

<style scoped>

</style>

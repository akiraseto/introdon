<template>
  <div>

    <h1>Test</h1>
    <!--    <input @click="getJson" type="button" value="jsonを取得">-->
    {{ jsonData }}
    {{ jsonData.name }}

  </div>
</template>

<script>
  export default {
    name: "Test",
    data() {
      return {
        jsonData: null
      }
    },
    methods: {
      getJson() {
        this.axios.get('/game/test')
            .then((response) => {
              this.jsonData = response.data;
              console.log(response.data);
            })
            .catch((e) => {
              console.log(e);
              this.jsonData = 'error'
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

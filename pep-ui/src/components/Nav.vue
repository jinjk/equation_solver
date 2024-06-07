<script>
export default {
    data() {
        return {
            keyword: null
        }
    },
    methods: {
        searchText() {
            console.log('searching for', this.keyword)
            this.$emitter.emit('search', this.keyword)
        }
    }
}
</script>

<template>
    <nav class="navbar navbar-expand-md fixed-top">
      <div class="collapse navbar-collapse" id="navbarsExampleDefault">
        <ul class="navbar-nav mr-auto">
        </ul>
        <form class="form-inline my-2 my-lg-0 bg-light" @submit.prevent="searchText">
          <input class="form-control mr-sm-2" v-model="keyword" type="text" placeholder="Search" aria-label="Search">
          <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
        </form>
      </div>
    </nav>
</template>
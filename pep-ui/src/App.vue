<script>
import Nav from './components/Nav.vue'
import BookViewer from './components/BookViewer.vue'
import Sidebar from './components/Sidebar.vue'

export default {
  components: {
    Nav, BookViewer, Sidebar
  },

  mounted() {
    const bootstrap = document.createElement('script')
    bootstrap.setAttribute('src', '/js/bootstrap.min.js')
    document.body.appendChild(bootstrap)
    const popper = document.createElement('script')
    popper.setAttribute('src', '/js/popper.min.js')
    document.body.appendChild(popper)

    // execute some code after the script is loaded
    const emitter = this.$emitter
    bootstrap.onload = function () {
      console.log('bootstrap loaded')
      emitter.emit("bootstrap-loaded", true);
    }
  }
}
</script>

<template>
  <Nav />
  <div class="container-fluid">
    <div class="row">
      <main role="main" class="col-md-9 ml-sm-auto col-lg-10">
        <BookViewer />
      </main>
      <Sidebar />
    </div>
  </div>

</template>

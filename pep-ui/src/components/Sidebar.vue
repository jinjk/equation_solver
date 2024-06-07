<script>
import bookProvider from '@/features/books/book-provider.js';
import { ref } from 'vue'
export default {
    data() {
        return {
            searchRes: [],
            selectedItem: null,
            keyword: null
        }
    },

    mounted() {
        this.$emitter.on('search', async (keyword) => {
            this.keyword = keyword
            this.searchRes = await bookProvider.findText(keyword)
            console.log('searchRes', this.searchRes)
        })
    },

    methods: {
        selectSearchRes(item) {
            this.selectedItem = item
            this.$emitter.emit('show-selected', item, this.keyword)
        }
    }
}
</script>

<template>
    <nav class="col-md-2 d-none d-md-block bg-light sidebar">
        <div class="sidebar-sticky">
            <div class="nav flex-column">
                <div class="card nav-item" v-for="item in searchRes">
                    <div class="btn-link" @click="selectSearchRes(item)">
                        <div class="card-body">
                            <h5 class="card-title">{{ item._source.text }}</h5>
                            <h6 class="card-subtitle mb-2 text-muted">第{{ item._source.page }}页</h6>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </nav>
</template>

<script>
import bookProvider from '@/features/books/book-provider.js';
import appConfig from '@/features/config/app-config';
import { ref } from 'vue';

export default {
    data() {
        return {
            book: null,
            searchRes: null,
            currentNum: ref(1)
        }
    },
    async created() {
        this.book = await bookProvider.getBookInfo();
        this.searchRes = await bookProvider.findText('夏天')
    },
    mounted() {
        this.$emitter.on("bootstrap-loaded", (data) => {
            console.log('update carousel here')
            $('#myCarousel').carousel(0)
            $('#myCarousel').on('slide.bs.carousel', function (event) {
                let img = $(event.relatedTarget).children("img")
                if (img.attr('src') != img.attr('data-src')) {
                    img.attr("src", img.attr('data-src'))
                }
            })
        });

        this.$emitter.on('show-selected', (item) => {
            if (this.currentNum == item._source.page) return
            this.currentNum = item._source.page
            console.log('page', item._source.page)
            const lastActive = $('.carousel-item.active')
            $('#myCarousel').carousel(item._source.page-1)
            lastActive.removeClass('active')
        })
    },
    methods: {
        imageUrl(page) {
            return `${appConfig.getConfig().serviceUrl}/images/cropped_${page}.jpg`;
        },
        isActive(n) {
            return n == this.currentNum;
        }
    }
}
</script>

<template>
    <!-- myCarousel start -->
    <div id="myCarousel" class="carousel slide" data-interval="false">
        <div class="carousel-inner">
            <div v-for="n in book?.pageCount" class="carousel-item" :class="{active: isActive(n)}" >
                <img :src="imageUrl(n)" :data-src="imageUrl(n)" v-if="n == currentNum">
                <img :src="imageUrl(n)" :data-src="imageUrl(n)" v-else>
            </div>
        </div>
        <a class="carousel-control-prev" href="#myCarousel" role="button" data-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="sr-only">Previous</span>
        </a>
        <a class="carousel-control-next" href="#myCarousel" role="button" data-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="sr-only">Next</span>
        </a>
    </div>
</template>
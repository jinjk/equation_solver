<script>
import bookProvider from '@/features/books/book-provider.js';
import appConfig from '@/features/config/app-config';

var bookViewer = null;

function highLightText(count, ctx, canvasSize, imageSize, postion) {
    const scaleX = canvasSize.width / imageSize.width
    const scaleY = canvasSize.height / imageSize.height
    const x = postion.X * scaleX
    const y = postion.Y * scaleY
    const width = postion.Width * scaleX
    const height = postion.Height * scaleY

    if (count % 2 == 1) {
        ctx.clearRect(x, y + height-2, x + width, y + height+2)
    }
    else {
        // draw a linefrom (x, y + height) to (x + width, y + height)
        ctx.beginPath()
        ctx.moveTo(x, y + height+2)
        ctx.lineTo(x + width, y + height+2)
        // set line width = 2 and color = red
        ctx.lineWidth = 2
        ctx.strokeStyle = 'red'
        ctx.stroke()
    }
    setTimeout(() => {
        if (count > 0) {
            count--;
            highLightText(count, ctx, canvasSize, imageSize, postion)
        }
    }, 200);
}

function resizeCanvas() {
    const canvas = $(`.carousel-item.active canvas`)
    if (canvas.length == 0) {
        return
    }
    const img = $(`.carousel-item.active img`)
    const imagePos = img.position();
    canvas.css({top: imagePos.top, left: imagePos.left, position:'absolute'});
    canvas.width(img.width());
    canvas.height(img.height());
}

export default {
    data() {
        return {
            book: null,
            searchRes: null,
            currentNum: 1,
            keyword: null,
            currentText: null
        }
    },
    async created() {
        this.book = await bookProvider.getBookInfo();
        this.searchRes = await bookProvider.findText('夏天')
    },
    mounted() {
        bookViewer = this;
        this.$emitter.on("bootstrap-loaded", (data) => {
            console.log('update carousel here')
            $('#myCarousel').carousel(0)
            $('#myCarousel').on('slide.bs.carousel', function (event) {
                const img = $(event.relatedTarget).children("img")
                if (img.attr('src') != img.attr('data-src')) {
                    img.attr("src", img.attr('data-src'))
                }
                console.log('slide.bs.carousel', event.to)
                bookViewer.currentNum = event.to + 1
            })
        });

        this.$emitter.on('show-selected', (item, keyword) => {
            if (this.keyword != keyword) {
                this.keyword = keyword
                $(`#myCarousel canvas`).each((i, el) => {
                    const ctx = el.getContext('2d')
                    ctx.clearRect(0, 0, el.width, el.height)
                })
            }
            if (this.currentNum != item._source.page) {
                this.currentNum = item._source.page
                const lastActive = $('.carousel-item.active')
                $('#myCarousel').carousel(item._source.page-1)
                lastActive.removeClass('active')
            }
            /* ------------------ draw highlight line -------------------- */
            const img = $(`#c-item-${item._source.page} img`)
            let canvas = $(`#c-item-${item._source.page} canvas`)
            if (canvas.length == 0) {
                const parentWidth = img.parent().width()
                const leftPercent = (parentWidth - img.width()) / parentWidth / 2 * 100
                $(`#c-item-${item._source.page}`)
                    .append(`<canvas width="${img.width()}" height="${img.height()}"
                    style="position: absolute; left: ${leftPercent}%; top: 0%"></canvas>`)
                canvas = $(`#c-item-${item._source.page} canvas`)
            }
            const cEle = canvas[0]
            const iEle = img[0]
            const ctx = cEle.getContext('2d')
            
            if (this.currentText != item._source.text) {
                ctx.clearRect(0, 0, cEle.width, cEle.height)
                this.currentText = item._source.text
            }

            highLightText(6, ctx, {width: iEle.width, height: iEle.height},
                    {width: iEle.naturalWidth, height: iEle.naturalHeight}, item._source.Polygon)
        });

        $( window ).on( "resize", () => {
            resizeCanvas();
        });
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
    <div id="myCarousel" class="carousel slide sticky-top" data-interval="false">
        <div class="carousel-inner">
            <div :id="['c-item-' + n]" v-for="n in book?.pageCount" class="carousel-item" :class="{active: isActive(n)}" >
                <img :src="imageUrl(n)" :data-src="imageUrl(n)" v-if="n == currentNum">
                <img :data-src="imageUrl(n)" v-else>
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
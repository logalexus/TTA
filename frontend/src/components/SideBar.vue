<template>
    <div class="col-md-auto sidebar">
        <div class="sidebar-sticky">
            <ul class="list">
                <Stream />
                <Stream />
                <Stream />
                <Stream />
                <Stream />
                <Stream />
                <Stream />
                <Stream />
                <Stream />
                <Stream />
                <Stream />
                <Stream />
            </ul>
        </div>
    </div>
</template>

<script>
import Stream from "@/components/Stream.vue";
export default {
    name: 'Sidebar',
    data: function () {
        return {
            streams: [
                {
                    id: 111,
                    time: 1556411080,
                },
            ],
        }
    },
    components: { Stream, },
}
</script>

<style scoped>
.sidebar {
    height: 100%;
    top: 0;
    left: 0;
    bottom: 0;
    /* background-color: #e7e7e7; */
    padding: 0;
}

.sidebar-sticky {
    position: relative;
    top: 0;
    height: calc(100vh - 30px);
    overflow-x: hidden;
    overflow-y: auto;
}

.list {
    list-style-type: none;
    padding: 0;
}
</style>
<template>
    <div class="sidebar">
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
    width: 500px;
}

.sidebar-sticky {
    position: relative;
    height: calc(100vh - 115px);
    overflow-x: hidden;
    overflow-y: auto;
}

.list {
    list-style-type: none;
    padding: 0;
}
</style>
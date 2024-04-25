<template>
    <div class="sidebar">
        <div class="sidebar-sticky">
            <ul class="list">
                <transition-group name="list" tag="p">
                    <Stream v-for="stream in streams" :key="stream.id" :stream="stream" />
                </transition-group>
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
            streams: [],
        }
    },
    methods: {
        addStream(stream) {
            this.streams.unshift(stream);
            console.log(stream);
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

.list-item {
    display: inline-block;
    margin-right: 10px;
}

.list-enter-active,
.list-leave-active {
    transition: 0.8s ease;
}

.list-enter-from,
.list-leave-to {
    opacity: 0;
    transform: translateX(100px);
}
</style>
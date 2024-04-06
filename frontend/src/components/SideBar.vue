<template>
    <nav class="col-md-3 d-none d-md-block bg-light sidebar">
        <div class="sidebar-sticky">
            <ul class="nav flex-column">
                <Stream v-for="stream in streams" :key="stream.id" :id="stream.id" :time="stream.time"></Stream>
            </ul>
        </div>
    </nav>

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
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    z-index: 100;
    /* Behind the navbar */
    padding: 48px 0 0;
    /* Height of navbar */
    box-shadow: inset -1px 0 0 rgba(0, 0, 0, .1);
}

.sidebar-sticky {
    position: relative;
    top: 0;
    height: calc(100vh - 48px);
    padding-top: .5rem;
    overflow-x: hidden;
    overflow-y: auto;
    /* Scrollable contents if viewport is shorter than content. */
}


.sidebar .nav-link {
    font-weight: 500;
    color: #333;
}

.sidebar .nav-link .feather {
    margin-right: 4px;
    color: #999;
}

.sidebar .nav-link.active {
    color: #007bff;
}

.sidebar .nav-link:hover .feather,
.sidebar .nav-link.active .feather {
    color: inherit;
}

.sidebar-heading {
    font-size: .75rem;
    text-transform: uppercase;
}
</style>
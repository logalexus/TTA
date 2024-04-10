<template>
    <div id="app">
        <NavBar />
        <div class="container-fluid">
            <div class="row main">
                <SideBar/>
                <Content/>
            </div>
        </div>

    </div>

</template>

<script>
import Content from '@/components/Content.vue';
import SideBar from '@/components/SideBar.vue';
import Stream from '@/components/Stream.vue';
import NavBar from '@/components/NavBar.vue';

export default {
    components: {
        Content,
        SideBar,
        Stream,
        NavBar,
    },
}
</script>

<style>
#app {
    font-family: "Space Grotesk", sans-serif;
    background-color: #e9ebf7;
}

.body {
    
}

.main {
    padding-top: 30px;
}
</style>
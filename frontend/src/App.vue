<template>
    <div id="app">
        <div class="sidebar">
            <h4 class="text-center">TCP Packages</h4>
            <ul class="list-group">
                <li class="list-group-item">
                    Package 1
                </li>
            </ul>
        </div>
        <div class="content">
            <h4 class="text-center">Viewer</h4>
            <div v-if="selectedPackageIndex !== null">
                <h4 class="text-center">Package {{ selectedPackageIndex + 1 }}</h4>
                <p>Content for package {{ selectedPackageIndex + 1 }}</p>
            </div>
            <div v-else>
                <p class="text-center">Select a package to view its content.</p>
            </div>
        </div>
    </div>

</template>

<script>
import Content from '@/components/Content.vue';
import SideBar from '@/components/SideBar.vue';
export default {
    components: {
        Content,
        SideBar,
    },
}
</script>

<style>
.sidebar {
    height: 100%;
    width: 250px;
    position: fixed;
    top: 0;
    left: 0;
    background-color: #f8f9fa;
    padding-top: 20px;
}

/* стили для контента */
.content {
    margin-left: 250px;
    padding: 20px;
}
</style>
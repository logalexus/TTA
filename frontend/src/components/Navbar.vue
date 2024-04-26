<template>
    <div class="navbar-main">
        <span class="text-logo">VVS</span>
        <span class="descriprion">TCP Traffic analyzer</span>
    </div>
    <div class="navbar-control">
        <button class="toggle-button" @click="toggleWs">
            <img v-if="isLive" src="../assets/pause.svg" alt="run">
            <img v-else src="../assets/run.svg" alt="run">
        </button>
    </div>
</template>

<script>
export default {
    props: {
        isLive: Boolean(),
    },
    methods: {
        toggleWs() {
            this.$emit("toggleWs");
        }
    },
}
</script>

<style scoped>
.navbar-main {
    height: 50px;
    display: flex;
    align-items: center;
    flex-direction: row;
    background-color: rgb(255, 255, 255);
    padding: 5px;
    gap: 10px
}

.navbar-control {
    height: 50px;
    display: flex;
    align-items: center;
    flex-direction: row;
    background-color: #f7f9fc;
    padding: 5px;
}

.toggle-button {
    border: none;
    background-color: transparent;
}

.text-logo {
    font-size: 30px;
    font-weight: 700;
    color: #406ce1;
}

.descriprion {
    font-size: 15px;
    font-weight: 500;
    color: #406be1a2;
}
</style>
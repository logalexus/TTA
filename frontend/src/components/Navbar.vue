<template>
    <div class="navbar-main">
        <span class="text-logo">TTA</span>
        <span class="descriprion">TCP Traffic Analyzer</span>
    </div>
    <div class="navbar-control">
        <button class="toggle-button" @click="$emit('toggleWs')">
            <img v-if="isLive" src="../assets/pause.svg" alt="run">
            <img v-else src="../assets/run.svg" alt="run">
        </button>
        <div class="port-select-group">
            <input class="port-input" maxlength="5" type="text" value="5000">
            <button class="port-button">Select</button>
        </div>
        <button class="button" @click="$emit('show-patterns')">Patterns</button>
    </div>
</template>

<script>

export default {
    props: {
        isLive: Boolean(),
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

.port-input{
    width: 60px;
    border: 1px solid #406ce1;
    border-radius: 4px 0px 0px 4px;
    text-align: center;
}

.port-button{
    border-color: transparent;
    background-color: #406ce1;
    color: white;
    font-weight: 500;
    border-radius: 0px 4px 4px 0px;
}

.navbar-control {
    height: 50px;
    display: flex;
    align-items: center;
    flex-direction: row;
    justify-content: space-between;
    background-color: #f7f9fc;
    padding: 5px;
}

.port-select-group{
    display: flex;
    flex-direction: row;
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

.button {
    border-color: transparent;
    border-radius: 4px;
    background-color: #406ce1;
    color: white;
    font-weight: 500;
}
</style>
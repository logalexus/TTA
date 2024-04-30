<template>
    <div class="navbar-main">
        <span class="text-logo">TTA</span>
        <span class="descriprion">TCP Traffic Analyzer</span>
    </div>
    <div class="navbar-control">
        <button class="toggle-button" @click="$emit('toggle-ws')">
            <img v-if="isLive" src="../assets/pause.svg" alt="run">
            <img v-else src="../assets/run.svg" alt="run">
        </button>
        <div class="button-group">
            <div class="port-select-group">
                <input class="port-input" maxlength="5" type="number" value="5000" v-model="port">
                <button class="port-button" @click="$emit('select-port', port)">Select port</button>
            </div>
            <button class="button" @click="$emit('update')">Update</button>
            <button class="button" @click="$emit('show-patterns')">Patterns</button>
            <button class="button" @click="$emit('clear-db')">Clear DB</button>
        </div>

    </div>
</template>

<script>

export default {
    props: {
        isLive: Boolean(),
    },
    emits: ["toggle-ws", "show-patterns", "select-port", "update"],
    data() {
        return {
            port: null,
        }
    },
    mounted() {
        this.loadPort()
    },
    methods: {
        loadPort() {
            this.$http.get(`port`)
                .then(response => {
                    this.port = Number(response.data)
                })
                .catch(e => {
                    console.error('Failed to load portion of streams:', e);
                });
        },

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

.button-group {
    display: flex;
    flex-direction: row;
    gap: 5px;
}

.port-input {
    width: 70px;
    border: 1px solid #406ce1;
    border-radius: 4px 0px 0px 4px;
    text-align: center;
}

.port-button {
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

.port-select-group {
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
<template>
    <li class="pattern">
        <div class="info-element">
            <div>{{ pattern.patternName }}</div>
            <div class="color-view"></div>
        </div>
        <div>{{ pattern.patternRegex }}</div>
        <button v-if="enabled" class="button button-activated" @click="enabled = false">Disable</button>
        <button v-else class="button button-diactivated" @click="enabled = true">Enable</button>
    </li>
</template>

<script>
export default {
    props: {
        pattern: {
            patternName: String(),
            patternRegex: String(),
            patternColor: String(),
        },
    },
    data() {
        return {
            enabled: false,
        }
    }
}
</script>

<style scoped>
.pattern {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    height: 40px;
    border: 1px solid rgb(200, 200, 200);
    border-radius: 5px;
    margin: 2px;
    padding-left: 5px;
    padding-right: 5px;
}

.info-element {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 5px
}

.color-view {
    height: 15px;
    width: 15px;
    background-color: red;
    border-radius: 10px;
}

.button {
    border-color: transparent;
    border-radius: 4px;
    background-color: #406ce1;
    color: white;
    font-weight: 500;
}

.button-activated {
    background-color: #e14040;
}

.button-diactivated {
    background-color: #3aba3a;
}
</style>
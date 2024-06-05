<template>
    <li class="pattern">
        <div class="info-element">
            <div class="text">{{ pattern.name }}</div>
            <div class="color-view" :style="{ 'background-color': pattern.color }"></div>
        </div>
        <div class="text">{{ pattern.regex }}</div>
        <div class="control">
            <!-- <button v-if="enabled" class="button button-activated" @click="enabled = false">Disable</button>
            <button v-else class="button button-diactivated" @click="enabled = true">Enable</button> -->
            <button class="button remove-button" @click="$emit('remove-pattern', pattern)">Remove</button>
        </div>
    </li>
</template>

<script>
export default {
    props: {
        pattern: {
            name: String(),
            regex: String(),
            color: String(),
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
    height: auto;
    min-height: 40px;
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

.control {
    display: flex;
    flex-direction: row;
    gap: 2px;
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

.remove-button {
    background-color: #e14040;
}

.text {
    max-width: 300px;
    overflow-wrap: break-word;
}
</style>
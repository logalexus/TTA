<template>
    <span class="label suspicious" :style="{ 'background-color': suspicious.color }">{{ suspicious.name }}</span>
</template>

<script>
export default {
    props: {
        suspicious: {
            name: String(),
            color: String(),
        }
    }
}
</script>

<style scoped>
.label {
    color: #fff;
    text-align: center;
}

.suspicious {
    background-color: #d62518;
    padding: 0px 4px 0px 4px;
    border-radius: 4px;
    font-size: 12px;
}
</style>
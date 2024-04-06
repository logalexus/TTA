<template>
    <li class="nav-item">
        <router-link class="nav-link" active-class="active">
            #{{ id }}<br />
            {{ time }}
        </router-link>
    </li>
</template>

<script>
export default {
    name: "Stream",
    props: ["id", "time"],
}
</script>

<style>

</style>
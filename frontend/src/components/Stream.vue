<template>
    <li class="cookie-card">
        <span class="title">Stream #1</span>
        <p class="description"></p>
        <div class="actions">
            <button class="accept"></button>
        </div>
    </li>
</template>

<script>
export default {
    name: "Stream",
    props: ["id", "time"],
}
</script>

<style>
.cookie-card {
    max-width: 320px;
    padding: 5px;
    background-color: #ffffff;
    border-radius: 5px;
    box-shadow: 20px 20px 30px rgba(0, 0, 0, .05);
    margin: 2px;
}

.title {
    font-weight: 600;
    color: rgb(31 41 55);
}


.accept {
    font-family: "Space Grotesk", sans-serif;
    line-height: 1rem;
    background-color: rgb(17 24 39);
    border-radius: 0.5rem;
    color: #fff;
    padding-left: 1rem;
    padding-right: 1rem;
    padding-top: 0.625rem;
    padding-bottom: 0.625rem;
    border: none;
    transition: all .15s cubic-bezier(0.4, 0, 0.2, 1);
}

.accept:hover {
    background-color: rgb(55 65 81);
}

.accept:focus {
    outline: 2px solid transparent;
    outline-offset: 2px;
}
</style>
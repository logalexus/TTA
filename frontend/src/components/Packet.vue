<template>
    <div :class="{'packet-incoming': packet.incoming, 'packet-outgoing': !packet.incoming}">
        <div>
            #{{ packet.id }} Packet at 10.09.2024
        </div>
        <p class="pt-2 pb-2 mb-3">
            POST /status
            HOST 1.1.1.1
        </p>
    </div>
</template>

<script>
export default {
    props: {
        packet: {
            id: Number(),
            incoming: Boolean(),
        }
    }
}
</script>

<style scoped>
.packet-outgoing {
    background: rgb(231, 248, 253);
    box-shadow: 0 0 5px 5px rgb(231, 248, 253);
}

.packet-incoming {
    background: rgb(254, 234, 231);
    box-shadow: 0 0 5px 5px rgb(254, 234, 231);
}

p {
    font-family: "Ubuntu Mono", "Lucida Console", monospace;
    font-size: 100%;
    margin-bottom: 10px;
    padding-bottom: 5px;
    word-break: break-word;
}
</style>
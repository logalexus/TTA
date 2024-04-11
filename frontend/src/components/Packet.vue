<template>
    <div class="packet" :class="{'packet-incoming': packet.incoming, 'packet-outgoing': !packet.incoming}">
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
}

.packet-incoming {
    background: rgb(254, 234, 231);
}

.packet {
    border-radius: 4px;
    padding: 10px;
    margin: 5px;
}
p {
    font-family: "Ubuntu Mono", "Lucida Console", monospace;
    font-size: 100%;
    word-break: break-word;
}
</style>
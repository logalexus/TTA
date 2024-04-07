<template>
    <div class="col-sm-9 ml-sm-auto px-4 content">
        <Packet v-for="packet in packets"
				:key="packet.id"
				:packet="packet"/>
    </div>
</template>

<script>
import Packet from "@/components/Packet.vue"
export default {
    data() {
        return {
            packets: [
                {id: 1, incoming: true},
                {id: 2, incoming: false},
            ],
        };
    },

    components: {
        Packet,
    }
}
</script>

<style scoped>
.content {
    padding: 20px;
}
</style>
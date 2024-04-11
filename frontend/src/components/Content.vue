<template>
    <div class="content">
        <div class="header">
            <span class="protocol">HTTP Stream #1</span>
        </div>
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
    background-color: white;
    padding: 10px;
    width: calc(100% - 500px);
    border-radius: 4px;
    margin-top: 5px;
    margin-bottom: 5px;
}

.protocol {
    color: #fff;
    background-color: #2964e3;
    padding: 0px 4px 0px 4px;
    border-radius: 4px;
    font-size: 12px;
}
</style>
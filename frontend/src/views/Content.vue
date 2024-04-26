<template>
    <div class="content">
        <div class="header">
            <span class="protocol">HTTP Stream {{ stream_id }}</span>
        </div>
        <Packet v-for="packet in packets" :key="packet.id" :packet="packet" />
    </div>
</template>

<script>
import Packet from "@/components/Packet.vue"
export default {
    name: "Content",
    props: {
        stream_id: Number(),
    },
    data() {
        return {
            packets: [],
        };
    },
    mounted() {
        this.loadPackets(this.stream_id);
    },
    watch: {
        '$route.params.stream_id': function () {
            this.packets = [];
            this.loadPackets(this.stream_id);
        },
    },
    methods: {
        loadPackets(stream_id) {
            this.$http.get(`packets?stream_id=${stream_id}`
            ).then(response => {
                console.log(response.data)
                const data = response.data;
                this.packets.push(...data);
            }).catch(e => {
                console.error('Failed to load portion of packets:', e);
            });
        }
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
    overflow-y: auto;
    height: calc(100vh - 115px);
}

.protocol {
    color: #fff;
    background-color: #2964e3;
    padding: 0px 4px 0px 4px;
    border-radius: 4px;
    font-size: 12px;
}
</style>
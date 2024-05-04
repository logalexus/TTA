<template>
    <li>
        <router-link class="stream-item nav-link"
            :to="{ name: 'stream', params: { stream_id: this.stream.id }, query: this.$route.query }">
            <span class="label protocol">{{ stream.protocol }}</span>
            <div class="stream-info">
                <span class="label status-label">#{{ stream.id }}</span>
                <div class="info">
                    <span class="ip">{{ stream.preview }}</span>
                    <div class="ip-addresses">
                        <span class="ip">{{ stream.ipsrc }}:{{ stream.portsrc }}</span>
                        <span class="arrow">➔</span>
                        <span class="ip">{{ stream.ipdst }}:{{ stream.portdst }}</span>
                    </div>
                    <div v-show="stream.suspicious.length > 0" class="suspicious-info">
                        <div class="ip">Suspicious:</div>
                        <Suspicious v-for="suspicious in stream.suspicious" :suspicious="suspicious"/>
                    </div>
                    <div class="timestamp">{{ dateToText(stream.start_timestamp) }}</div>
                </div>
            </div>
        </router-link>
    </li>
</template>

<script>
import Suspicious from '@/components/Suspicious.vue';
export default {
    name: "Stream",
    props: {
        stream: {
            id: Number(),
            protocol: String(),
            start_timestamp: Number(),
            end_timestamp: Number(),
            ipsrc: String(),
            ipdst: String(),
            portsrc: Number(),
            portdst: Number(),
            status: Number(),
            preview: String(),
            suspicious: Array(),
        }
    },
    methods: {
        dateToText(unixTimestamp) {
            const date = new Date(unixTimestamp * 1000);
            return date.toLocaleString('ru-RU');
        },
    },
    components: {
        Suspicious,
    }
}
</script>

<style scoped>
.nav-link {
    color: #333;
    text-decoration: none;
}

.stream-item {
    background-color: #ffffff;
    border-radius: 4px;
    box-shadow: 20px 20px 30px rgba(0, 0, 0, .05);
    margin: 5px;
    min-height: 80px;
    display: flex;
    gap: 5px;
}

.stream-info {
    padding: 5px;
    width: 100%;
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 10px;
}

.label {
    color: #fff;
    text-align: center;
}

.protocol {
    background-color: #2196F3;
    font-size: 15px;
    font-weight: 600;
    letter-spacing: 0.5px;
    line-height: 20px;
    height: auto;
    width: 20px;
    writing-mode: vertical-lr;
    transform: rotate(-180deg);
    border-radius: 0px 4px 4px 0;
}

.status-label {
    background-color: #444444;
    padding: 0px 4px 0px 4px;
    border-radius: 4px;
}

.info {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.suspicious-info {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    align-items: center;
    gap: 5px
}

.suspicious {
    background-color: #d62518;
    padding: 0px 4px 0px 4px;
    border-radius: 4px;
    font-size: 12px;
}

.ip-addresses {
    display: flex;
    align-items: center;
    margin-bottom: 4px;
}

.arrow {
    margin: 0 8px;
}

.timestamp {
    font-size: 10px;
    color: #999;
}
</style>
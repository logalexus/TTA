<template>
    <div id="app">
        <Navbar @toggleWs="toggleWs" :isLive="isLive" @show-patterns="showPatternsModal = true" />
        <div class="row">
            <Sidebar ref="sidebar" />
            <transition name="fade" mode="out-in">
                <router-view name="content" />
            </transition>

        </div>
        <PatternsModal v-show="showPatternsModal" @close-modal="showPatternsModal = false" />
    </div>

</template>

<script>
import Sidebar from '@/components/Sidebar.vue';
import Stream from '@/components/Stream.vue';
import Navbar from '@/components/Navbar.vue';
import PatternsModal from '@/views/PatternsModal.vue'
import config from '@/config.js';

export default {
    components: {
        Sidebar,
        Stream,
        Navbar,
        PatternsModal,
    },
    data() {
        return {
            isLive: false,
            websocket: null,
            db: null,
            showPatternsModal: true,
        };
    },
    mounted() {
        this.loadStreams();
        this.connectWs();
    },
    methods: {
        connectWs() {
            if (this.websocket !== null) return;
            this.websocket = new WebSocket(config.apiWs);
            this.websocket.onopen = () => {
                this.isLive = true;
                console.info('[WS] Connected');
            };
            this.websocket.onclose = (ev) => {
                console.info('[WS] Disconnected', ev.code, ev.reason);
                this.isLive = false;
                this.websocket = null;
            };
            this.websocket.onmessage = (ev) => {
                const parsed = JSON.parse(ev.data);

                switch (parsed.type) {
                    case 'NEW_STREAM': {
                        this.$refs.sidebar.addStream(parsed.data)
                        break;
                    }
                    default: {
                        console.error('[WS] Event is not implemented!', parsed);
                        break;
                    }
                }
            };
            this.websocket.onerror = (ev) => {
                console.warn('[WS] Error', ev);
                setTimeout(this.connectWs, 3000);
                console.info('[WS] Reconnecting...');
            };

        },
        disconnectWs() {
            this.websocket?.close();
            this.websocket = null;
            this.isLive = false;
            console.info('[WS] Closed');
        },
        toggleWs() {
            if (!this.isLive) {
                this.connectWs();
            }
            else {
                this.disconnectWs();
            }

        },
        loadStreams() {
            this.$http.get(`streams`)
                .then(response => {
                    console.log(response.data);
                    Object.values(response.data).forEach(value => {
                        this.$refs.sidebar.addStream(value)
                    });
                })
                .catch(e => {
                    console.error('Failed to load portion of streams:', e);
                });
        },
    }

}
</script>

<style>
#app {
    font-family: "Space Grotesk", sans-serif;
    background-color: #e9ebf7;
}

.row {
    display: flex;
    flex-flow: row nowrap;
    width: 100%;
}
</style>
<template>
    <div id="app">
        <Navbar @toggle-ws="toggleWs" :isLive="isLive" @show-patterns="showPatternsModal = true"
            @select-port="selectPort" @clear-db="clearDB" @update="loadStreams"/>
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
            showPatternsModal: false,
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
                this.$toast.info("Connected")
            };
            this.websocket.onclose = (ev) => {
                console.info('[WS] Disconnected', ev.code, ev.reason);
                this.$toast.info("Disconnected")
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
                this.$toast.error("Error")
                setTimeout(this.connectWs, 3000);
                console.info('[WS] Reconnecting...');
                this.$toast.info("Reconnecting...")
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
            this.$refs.sidebar.clearStreams()
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
        selectPort(port) {
            console.log(port);
            if (port == null) {
                this.$toast.error("Port cannot be empty")
                return
            }
            if (!Number.isInteger(port)) {
                this.$toast.error("Port must be a number")
                return
            }
            this.$http.post(`port/select?port=${port}`)
                .then(response => {
                    this.$toast.success("Port selected")
                    this.$refs.sidebar.clearStreams()
                    this.loadStreams()
                })
                .catch(e => {
                    this.$toast.error(e.response.data.detail || "An error occurred")
                });
        },
        clearDB() {
            this.$http.post(`db/clear`)
                .then(response => {
                    this.$toast.success("Database cleared")
                    this.$refs.sidebar.clearStreams()
                    this.$router.push('/');
                })
                .catch(e => {
                    this.$toast.error(e.response.data.detail || "An error occurred")
                });
        }
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
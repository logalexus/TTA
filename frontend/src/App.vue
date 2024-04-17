<template>
    <div id="app">
        <Navbar @toggleWs="toggleWs" />
        <div class="row">
            <Sidebar />
            <Content />
        </div>
    </div>

</template>

<script>
import Content from '@/components/Content.vue';
import Sidebar from '@/components/Sidebar.vue';
import Stream from '@/components/Stream.vue';
import Navbar from '@/components/Navbar.vue';
import SockJS from 'sockjs-client';

export default {
    components: {
        Content,
        Sidebar,
        Stream,
        Navbar,
    },
    data() {
        return {
            isLive: false,
            websocket: null,
            db: null,
        };
    },
    methods: {
        connectWs() {
            if (this.websocket !== null) return;
            this.websocket = new SockJS(this.$http.defaults.baseURL + '/ws');
            this.websocket.onopen = () => {
                this.isLive=true;
                console.info('[WS] Connected');
            };
            this.websocket.onclose = (ev) => {
                console.info('[WS] Disconnected', ev.code, ev.reason);
                this.websocket = null;
                if (ev.code === 1008) {
                    console.info('[WS] Security timeout, reconnecting...');
                    // this.connectWs();
                }
                if (ev.code !== 1000) {
                    // setTimeout(this.connectWs, 3000);
                    console.info('[WS] Reconnecting...');
                }
            };
            this.websocket.onmessage = (ev) => {
                const parsed = JSON.parse(ev.data);

                switch (parsed.type) {
                    case 'NEW_STREAM': {
                        this.$refs.sidebar.addStreamFromWs(parsed.value);
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
            };

        },
        disconnectWs() {
            this.websocket.close();
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
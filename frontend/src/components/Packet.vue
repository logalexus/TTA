<template>
    <div class="packet" :class="{ 'packet-incoming': packet.incoming, 'packet-outgoing': !packet.incoming }">
        <div>
            #{{ packet.id }} Packet at {{ packet.timestamp }}
        </div>
        <p class="pt-2 pb-2 mb-3" v-html="stringdata"></p>
    </div>
</template>

<script>
export default {
    props: {
        packet: {
            id: Number(),
            ipsrc: String(),
            ipdst: String(),
            portsrc: Number(),
            portdst: Number(),
            timestamp: Number(),
            incoming: Boolean(),
            payload: String(),
            protocol: String(),
            status: Number(),
        }
    },
    computed: {
        stringdata() {
            // const dataString = this.atou(this.packet.payload);
            // const dump = this.highlightPatterns(dataString);
            return this.escapeHtml(this.packet.payload)
                .split('\n')
                .join('<br>');
        },
    },
    methods: {
        atou(b64) {
            const text = atob(b64);
            const length = text.length;
            const bytes = new Uint8Array(length);
            for (let i = 0; i < length; i++) {
                bytes[i] = text.charCodeAt(i);
            }
            const decoder = new TextDecoder();
            return decoder.decode(bytes);
        },
        escapeHtml(in_) {
            return in_.replace(/(<span style="background-color: #(?:[A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})">|<\/span>)|[&<>"'/]/g, ($0, $1) => {
                const entityMap = {
                    '&': '&amp;',
                    '<': '&lt;',
                    '>': '&gt;',
                    '"': '&quot;',
                    '\'': '&#39;',
                    '/': '&#x2F;',
                };

                return $1 ? $1 : entityMap[$0];
            });
        },

    },

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
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
            timestamp: Number(),
            incoming: Boolean(),
            payload: String(),
            pattern_match: Array(),
        }
    },
    computed: {
        stringdata() {
            const highlighted = this.highlightPatterns(this.packet.payload);
            return this.escapeHtml(highlighted)
                .split('\n')
                .join('<br>');
        },
    },
    methods: {
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
        highlightPatterns(raw) {
            let offset = 0;
            this.packet.pattern_match
                .sort((a, b) => a.start_match - b.start_match)
                .forEach(match => {
                    const firstTag = `<span style="background-color: ${match.color}">`;
                    const secondTag = '</span>';

                    const positionStart = match.start_match + offset;
                    raw = raw.substring(0, positionStart) + firstTag + raw.substring(positionStart);
                    offset += firstTag.length;

                    const positionEnd = match.end_match + offset;
                    raw = raw.substring(0, positionEnd) + secondTag + raw.substring(positionEnd);
                    offset += secondTag.length;
                });
            return raw;
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
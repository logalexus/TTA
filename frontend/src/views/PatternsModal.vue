<template>
    <div class="modal-overlay">
        <div class="modal-window">
            <div class="modal-header">
                <h6>Patterns</h6>
                <button class="close-btn" @click="$emit('close-modal')">
                    <img class="close-img" src="@/assets/closeIcon.svg" alt="" />
                </button>
            </div>
            <div class="patterns-list">
                <ul class="list-group">
                    <Pattern v-for="pattern in patterns" :pattern="pattern" @remove-pattern="removePattern" />
                </ul>
            </div>
            <div class="modal-header">
                <h6>Create</h6>
            </div>
            <div class="patterns-create">
                <div class="mb-3">
                    <label for="namePattern" class="form-label">Name</label>
                    <input type="text" class="form-control" id="namePattern" placeholder="SQLI" v-model="name">
                </div>
                <div class="mb-3">
                    <label for="regexPattern" class="form-label">Regular expression</label>
                    <input type="text" class="form-control" id="regexPattern" placeholder="T[1-9A-Z]+" v-model="regex">
                </div>
                <div class="mb-3">
                    <label for="colorPattern" class="form-label">Highlight color</label>
                    <input type="color" class="form-control" id="colorPattern" v-model="color">
                </div>
                <button @click="addPattern" class="button">Add</button>
            </div>
        </div>
    </div>
</template>

<script>
import Pattern from "@/components/Pattern.vue"
export default {
    data() {
        return {
            name: "",
            regex: "",
            color: "#ff0000",
            patterns: []
        }
    },
    mounted() {
        this.loadPatterns();
    },
    methods: {
        addPattern() {
            const pattern = {
                name: this.name,
                regex: this.regex,
                color: this.color,
            };

            this.$http.post(`pattern/add`, pattern)
                .then(response => {
                    this.patterns.push(pattern)
                })
                .catch(e => {
                    this.$toast.error(e.response.data.detail || "An error occurred")
                });
        },
        removePattern(pattern) {
            this.$http.post(`pattern/remove?name=${pattern.name}`)
                .then(response => {
                    this.patterns = this.patterns.filter((el) => { return el.name != pattern.name })
                })
                .catch(e => {
                    this.$toast.error(e.response.data.detail || "An error occurred")
                });
        },
        loadPatterns() {
            this.$http.get(`patterns`)
                .then(response => {
                    Object.values(response.data).forEach(value => {
                        this.patterns.push(value)
                    });
                })
                .catch(e => {
                    console.error('Failed to load portion of patterns:', e);
                });
        },
    },
    components: {
        Pattern
    }
}
</script>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    display: flex;
    justify-content: center;
    background-color: #000000a4;
}

.patterns-list {
    height: 220px;
    overflow-y: auto;
    overflow-x: hidden;
}

.patterns-create {
    display: flex;
    flex-direction: column;
    align-items: ;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    width: 100%;
}

.modal-window {
    text-align: center;
    background-color: white;
    height: 700px;
    width: 1000px;
    margin-top: 5%;
    padding: 20px;
    border-radius: 4px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.close-btn {
    border: none;
    background-color: transparent;
}

.button {
    border-color: transparent;
    border-radius: 4px;
    background-color: #406ce1;
    color: white;
    font-weight: 500;
}


h6 {
    font-weight: 500;
    font-size: 28px;
}

p {
    font-size: 16px;
    margin: 20px 0;
}
</style>
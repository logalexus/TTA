<template>
    <li class="stream-item">
        <span class="label protocol">HTTP</span>
        <div class="stream-info">
            <span class="label status-label">200</span>
            <div class="info">
                <div class="ip-addresses">
                    <span class="ip">172.17.0.1:33996</span>
                    <span class="arrow">➔</span>
                    <span class="ip">172.17.0.1880</span>
                </div>
                <div class="suspicious-info">
                    <div class="ip">Suspicious:</div>
                    <span class="label suspicious">XSS</span>
                    <span class="label suspicious">SQL Injection</span>
                </div>
                <div class="timestamp">01/05/2023, 4:58:13:207 AM</div>
            </div>
        </div>
    </li>
</template>

<script>
export default {
    name: "Stream",
    props: ["id", "time"],
}
</script>

<style scoped>
.stream-item {
    background-color: #ffffff;
    border-radius: 4px;
    box-shadow: 20px 20px 30px rgba(0, 0, 0, .05);
    margin: 5px;
    height: 80px;
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
    height: 100%;
    width: 20px;
    writing-mode: vertical-lr;
    transform: rotate(-180deg);
    border-radius: 0px 4px 4px 0;
}

.status-label {
    background-color: #4CAF50;
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
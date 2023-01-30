import store from '@/store';
import axios from 'axios';
import VueCookies from 'vue-cookies'

const socket = new WebSocket(
    `wss://q-a-board-api.herokuapp.com/ws/`
)

socket.onopen = async function (e) {
    e;
    socket.send(VueCookies.get('qab_at'))
    await axios.get('/notifications/').then(response => {
        store.state.notifications = response.data
    })
};

socket.addEventListener('message', async (e) => {
    const data = JSON.parse(e.data);
    if (data.type === "NOTIFICATION") {
        await axios.get('/notifications/').then(response => {
            store.state.notifications = response.data
        })
    }
})

socket.onclose = function (e) {
    console.error(e);
    console.error("Chat socket closed unexpectedly");
};

export default socket;

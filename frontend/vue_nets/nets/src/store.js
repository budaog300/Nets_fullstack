import { createStore } from 'vuex';

const store = createStore({
    state: {
        veterans: [],
        sports: []
    },
    mutations: {
        setVeterans(state, veterans) {
            state.veterans = veterans;
        },
        setSports(state, sports) {
            state.sports = sports;
        }
    },
    actions: {
        async fetchVeterans({ commit }) {
            const response = await fetch('http://localhost:8000/sport/api/v1/veterans/');
            const data = await response.json();
            commit('setVeterans', data);
        },
        async fetchSports({ commit }) {
            const response = await fetch('http://localhost:8000/sport/api/v1/sports/');
            const data = await response.json();
            commit('setSports', data);
        }
    },
    getters: {
        getVeteranById: (state) => (id) => {
            return state.veterans.find(veteran => veteran.id === id);
        },
        getSportNameById: (state) => (id) => {
            const sport = state.sports.find(sport => sport.id === id);
            return sport ? sport.name : 'Неизвестный спорт';
        }
    }
});

export default store

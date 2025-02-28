<template>
    <NavigationPanel />
    <Table 
        title="Ветераны"        
        :items="items"
        :rowKeys="['get_full_name', 'gender', 'age_group', 'photo', 'sport', 'club', 'achievements']"
        :formatFunc="formatValue"
        apiUrl="http://localhost:8000/sport/api/v1/veterans/"
        :headerToFieldMap="headerToFieldMap"
        :foreignKeysMap="foreignKeysMap"
    />
       
</template>

<script>
import NavigationPanel from './NavigationPanel.vue';
import Table from './Table.vue';

export default {
    components: {
        NavigationPanel,
        Table,
    },
    data() {
        return {
            items: [],
            sports: {},
            clubs: {},
            headerToFieldMap: { 
                'ФИО': 'get_full_name',
                'Пол': 'gender',
                'Возрастная группа': 'age_group',
                'Фото': 'photo',
                'Вид спорта': 'sport',
                'Клуб': 'club',
                'Награда': 'achievements',
            },
            foreignKeysMap: {},
        }
    },
   
    methods: {
       
        async fetchData() {
            const sportData = [];
            const clubData = [];
            let pageNumber1 = 1;
            let pageNumber2 = 1;
         
            while (true) {
                try {
                    const resSport = await this.$axios.get(`http://localhost:8000/sport/api/v1/sports/?page=${pageNumber1}`); 
                    console.log("Fetched sports:", resSport.data);
                    if (resSport.data.results && resSport.data.results.length > 0) {
                        sportData.push(...resSport.data.results);
                        pageNumber1++;
                    } else {
                        break; 
                    }
                } catch (error) {
                    console.error("Error fetching sports:", error);
                    break;
                }
            }
            
            this.sports = sportData.reduce((acc, sport) => {
                acc[sport.id] = sport.name; 
                return acc;
            }, {});

           
            while (true) {
                try {
                    const resClub = await this.$axios.get(`http://localhost:8000/sport/api/v1/clubs/?page=${pageNumber2}`); 
                    console.log("Fetched clubs:", resClub.data);
                    if (resClub.data.results && resClub.data.results.length > 0) {
                        clubData.push(...resClub.data.results);
                        pageNumber2++;
                    } else {
                        break; 
                    }
                } catch (error) {
                    console.error("Error fetching clubs:", error);
                    break;
                }
            }        
            this.clubs = clubData.reduce((acc, club) => {
                acc[club.id] = club.name; 
                return acc;
            }, {});
 
            this.foreignKeysMap = {
                sport: Object.entries(this.sports).map(([id, name]) => ({ value: id, label: name })),
                club: Object.entries(this.clubs).map(([id, name]) => ({ value: id, label: name })), 
                gender: [
                    { value: 'male', label: 'Мужской' },
                    { value: 'female', label: 'Женский' },
                ],               
            };
        },
        formatValue(key, value) {
            if (key === 'gender') {
                return value === 'male' ? 'Мужской' : value === 'female' ? 'Женский' : 'Не указано';
            }
            if (key === 'sport') {
                return this.sports[value] || 'Нет спорта'
            }
            if (key === 'club') {
                return this.clubs[value] || 'Нет клуба'
            }
            
            return value || 'Не указано';
        }, 
    },
    async mounted() {
        await this.fetchData(); 
    }
}
</script>


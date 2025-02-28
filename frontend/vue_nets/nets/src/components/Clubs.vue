<template>
    <NavigationPanel />
    <Table 
        title="Клубы ветеранов спорта"        
        :items="items"
        :rowKeys="['name', 'director', 'time_create', 'address']"
        :formatFunc="formatValue"
        apiUrl="http://localhost:8000/sport/api/v1/clubs/"
        :headerToFieldMap="headerToFieldMap"      
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
            headerToFieldMap: { 
                'Название': 'name',
                'Руководитель': 'director',
                'Год основания': 'time_create',
                'Адрес': 'address',
            },
        }
    },
    methods: {
       
        formatValue(key, value) {            
            if (key === 'time_create' && value) {
                return this.formatDate(value);
            }
            return value || 'Не указано';
        },     
        formatDate(dateString) {
            if (!dateString) return 'Не указано';
            const date = new Date(dateString);
            return date.toLocaleDateString('ru-RU', {
                year: '2-digit',
                month: '2-digit',
                day: 'numeric',
            });
        }
        
    },
    async mounted() {
      
    }
}
</script>


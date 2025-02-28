<template>
    <NavigationPanel />
    <Table 
        title="Категории"        
        :items="items"
        :rowKeys="['name']"
        :formatFunc="formatValue"
        apiUrl="http://localhost:8000/sport/api/v1/category/"
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
                    'Категория': 'name',                
                },
            }
        },
        methods: {
        
            formatValue(key, value) {
                if (key === 'director' && value) {
                    return value.get_full_name; 
                }
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
        mounted() {
        
        }
    }
</script>
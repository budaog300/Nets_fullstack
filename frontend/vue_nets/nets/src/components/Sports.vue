<template>
    <NavigationPanel />
    <Table 
        title="Виды спорта"       
        :items="items"
        :rowKeys="['name', 'cat']"
        :formatFunc="formatValue"
        :categories="categories"
        apiUrl="http://localhost:8000/sport/api/v1/sports/"
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
                categories: {},
                headerToFieldMap: { 
                    'Название': 'name',
                    'Категория': 'cat',
                },
                foreignKeysMap: {},
            }
        },
       
        methods: {
            async fetchData() {
                const categoriesData = [];
                let pageNumber = 1;
               
                while (true) {
                    try {
                        const response = await this.$axios.get(`http://localhost:8000/sport/api/v1/category/?page=${pageNumber}`);
                        if (response.data.results && response.data.results.length > 0) {
                            categoriesData.push(...response.data.results);
                            pageNumber++;
                        } else {
                            break; 
                        }
                    } catch (error) {
                        console.error("Error fetching categories:", error);
                        break; 
                    }
                }
                this.categories = categoriesData.reduce((acc, category) => {
                    acc[category.id] = category.name; 
                    return acc;
                }, {});

                this.foreignKeysMap = {
                    cat: Object.entries(this.categories).map(([id, name]) => ({ value: id, label: name })),
                };

            },
            formatValue(key, value) {
                if (key === 'cat') {
                    console.log("Items with categories:", this.categories);
                    console.log("Items with categories value for 'cat':", value);
                    return this.categories[value] || 'Нет категории';
                }
                return value || 'Не указано';
            },
        },
        async mounted() {
            await this.fetchData(); 
            
        }
    }
</script>

<template>
    <div class="search-container">
        <input type="text" id="searchInput" v-model="searchText" placeholder="Поиск..." @input="onSearchInput">
        <button v-if="searchText" @click="clearInput" class="clear-button">×</button>
    </div>
    <p class="search-info" v-if="searchText">Вы ввели: {{ searchText }}</p>

    <!-- Контейнер для кнопок фильтров -->
    <div class="filter-buttons-container">
        <button @click="openFilter" class="filter-button apply-button">Фильтры</button>
        <button @click="clearFilters" class="filter-button clear-button1">Очистить фильтры</button>
    </div>
    <div v-if="isFilterOpen" class="dialog-overlay">
        <div class="dialog-content">
            <div class="filter-container">
                <h3>Фильтры</h3>
                <div
                    v-for="(header, field) in headerToFieldMap" 
                    :key="header"  
                    class="filter-item"       
                >
                    <label class="filter-label" v-if="header !== 'photo' && header !== 'achievements'">{{ field }}: </label>

                    <select 
                        v-if="isForeignKey(header)"
                        v-model="filters[header]" 
                        class="filter-input"
                    >
                        <option value=""></option>
                        <option 
                            v-for="option in foreignKeysMap[header]" 
                            :key="option.value" 
                            :value="option.value"
                        >
                            {{ option.label }}
                        </option>
                    </select>

                    <input 
                        v-if="fieldType(header) === 'text' && header !== 'achievements' && !isForeignKey(header)" 
                        type="text" 
                        v-model="filters[header]" 
                        class="filter-input"
                        placeholder="Введите значение"
                    >
                    <input 
                        v-else-if="fieldType(header) === 'date'" 
                        type="date" 
                        v-model="filters[header]"
                        class="filter-input"
                    >             
                </div> 
                <div class="filter-actions">
                    <button @click="applyFilters" class="filter-button apply-button">Применить</button>  <!-- Кнопка Применить  -->
                    <button @click="closeFilter" class="filter-button clear-button">Закрыть</button>  <!-- Кнопка Закрыть  -->
                </div>
            </div>
        </div>
    </div> 
    <div class="table_container">
        <h1>{{ title }}</h1>
        <div v-if="items.length > 0" class="info_message">
            По вашему запросу найдено {{ items.length }} запись(ей)
        </div>
        <!-- Таблица -->
        <table class="table-con">
            <thead>
                <tr>
                    <th>№</th>
                    <th 
                        v-for="(header, index) in tableHeaders" 
                        :key="index"  
                        @click="getSort(header)"
                        :class="{ active: sortBy === headerToFieldMap[header] }"
                    >
                        {{ header }}
                        <span v-if="sortBy === headerToFieldMap[header]">
                            {{ sortOrder === 'asc' ? '↑' : '↓' }}
                        </span>
                    </th>
                    <th v-if="isAuthenticated">
                        Actions
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item, index) in items" :key="item?.id" :class="{ even: index % 2 === 0, odd: index % 2 !== 0 }">
                    <td class="center">{{ getRowNumber(index) }}</td>                    
                    <td v-for="key in rowKeys" :key="key">
                        <div v-if="key === 'get_full_name'">
                            <div v-if="item[key]">{{ getFullName(item) || 'Не указано' }}</div>
                        </div>
                        <div v-else-if="key === 'photo'" class="photo-cell" @click="openPopup(item[key])">
                            <div v-if="item[key]">Фото ветерана</div>
                            <div v-else>Фото нет</div>
                        </div>
                        <div v-else>
                            {{ formatFunc(key, item[key]) || 'Не указано' }}
                        </div>
                    </td>
                    <td v-if="isAuthenticated">
                        <button @click="openEditDialog(item)" class="icon-button edit-button"><i class="fa-solid fa-pencil"></i></button>   <!-- Кнопка Редактировать  -->
                        <button @click="deleteItem(item.id)" class="icon-button delete-button"><i class="fa-solid fa-trash"></i></button>    <!-- Кнопка Удалить  -->
                    </td>
                </tr>
            </tbody>
        </table>
       
        <!-- Кнопка добавления новой записи -->
        <button v-if="isAuthenticated" @click="openCreateDialog" class="add-button">
            <i class="fa-solid fa-plus"></i> Добавить запись
        </button>

        <!-- Пагинация -->
        <div class="pagination-container">
            <div class="select-container">
                Items per Page:
                <select v-model="pageSize" @change="changePageSize($event)">
                    <option v-for="size in pageSizes" :key="size" :value="size">
                        {{ size }}
                    </option>
                </select>
            </div>
            <div class="pagination" v-if="total > 0 && totalPages > 1">
                <button @click="prevPage" :disabled="page === 1">Назад</button>
                <span 
                    v-for="pageNum in totalPages" 
                    :key="pageNum"
                    :class="{ active: page === pageNum }"
                    @click="changePage(pageNum)"
                >
                    {{ pageNum }}
                </span>
                <button @click="nextPage" :disabled="page >= totalPages">Вперед</button>
            </div>
        </div>
        <div v-if="isDialogOpen" class="dialog-overlay">
            <div class="dialog-content">
                <h3>{{ dialogTitle }}</h3>         
                <form @submit.prevent="handleSave">                   
                    <div class="filter-container">
                        <div
                            v-for="(header, field) in headerToFieldMap" 
                            :key="header"  
                            class="filter-item"       
                        >
                            <label v-if="header !== 'get_full_name' && header !== 'time_create'" class="filter-label">{{ field }}<span v-if="!isEditing && header != 'photo'">*</span>: </label>

                            <select 
                                v-if="isForeignKey(header)"
                                v-model="form[header]" 
                                class="filter-input"
                                required="true"
                            >
                                <option value=""></option>
                                <option 
                                    v-for="option in foreignKeysMap[header]" 
                                    :key="option.value" 
                                    :value="option.value"
                                >
                                    {{ option.label }}
                                </option>
                            </select>
                            
                            <div v-if="fieldType(header) === 'text' && header === 'get_full_name'" class="filter-fio">   
                                    <div class="full-name-field">
                                        <div class="filter-item">
                                            <label class="filter-label">Фамилия<span v-if="!isEditing && header != 'photo'">*</span>: </label>
                                            <input v-model="form.last_name" type="text" placeholder="Введите фамилию" class="filter-input" required="true">
                                        </div>
                                    </div>

                                    <div class="full-name-field">
                                        <div class="filter-item">
                                            <label class="filter-label">Имя<span v-if="!isEditing && header != 'photo'">*</span>: </label>
                                            <input v-model="form.first_name" type="text" placeholder="Введите имя" class="filter-input" required="true">
                                        </div>
                                    </div>

                                    <div class="full-name-field">
                                        <div class="filter-item">
                                            <label class="filter-label">Отчество: </label>
                                            <input v-model="form.patronymic" type="text" placeholder="Введите отчество" class="filter-input">
                                        </div>
                                    </div>                           
                            </div>
                        
                            <input 
                                v-if="fieldType(header) === 'text' && !isForeignKey(header) && header !== 'get_full_name'"
                                type="text" 
                                v-model="form[header]" 
                                class="filter-input"
                                placeholder="Введите значение"
                                required="true"
                            >   

                            <input 
                                v-if="fieldType(header) === 'file'"  
                                type="file" 
                                @change="onFileChange" 
                                class="filter-input"                            
                            />

                        </div> 
                    
                    </div>
                    <div class="actions">
                        <button type="submit">{{ isEditing ? 'Сохранить' : 'Добавить' }}</button>   <!--Кнопка Сохранить/Добавить -->
                        <button @click="closeDialog">Отмена</button>     <!--Кнопка Отмена -->
                    </div>
                </form>
            </div>
        </div>
        <!-- PopUp -->
        <PopupImage :imageUrl="currentImage" :isVisible="isPopupVisible" @close="isPopupVisible = false" />
    </div>
</template>

<script>
import PopupImage from './PopupImage.vue';
import { updateTokens } from '../services/userService';

export default {
    name: 'Table',
    components: {       
        PopupImage,      
    },  
    props: {
        title: {
            type: String,
            required: true
        },
        headers: {
            type: Array,
            required: true
        },
        items: {
            type: Array,
            default: () => []
        },
        rowKeys: {
            type: Array,
            required: true
        },
        formatFunc: {
            type: Function,
            default: (value) => value
        },
        apiUrl: {
            type: String,
            required: true
        },      
        headerToFieldMap: { 
            type: Object,
            required: true,
        },
        fieldTypeMap: {
            type: Object,
            default: () => ({
                'time_create': 'date', 
                'photo': 'file',               
            }),
        },        
        foreignKeysMap: {
            type: Object,
            default: () => ({}),
        },
       
    },
    data() {
        return {
            url: ``,           
         
            searchText: '',
            filters: {},
            isFilters: false,
            isFilterOpen: false,

            items: [],          
            isPopupVisible: false,
            currentImage: null,

            page: 1,
            total: 0,      
            pageSizes: [2, 3, 5],   
            pageSize: 2,

            sortBy: null,
            sortOrder: 'asc',

            form: {},
            isDialogOpen: false,
            isEditing: false
        }
    },   
    computed: {
        tableHeaders() {
            return Object.keys(this.headerToFieldMap); 
        },
        // Вычисляем общее количество страниц
        totalPages() {
            //const pageSize = this.items.length; 
            return Math.ceil(this.total / this.pageSize);
        },
        dialogTitle() {
            return this.isEditing ? 'Редактирование записи' : 'Добавление новой записи';
        },
        isAuthenticated() {
            return localStorage.getItem('accessToken') !== null; 
        },
    },
    created() {   
        this.fetchData();
        //this.getData(this.page);      
    },
 
    methods: {    
        getFullName(item) {
            return `${item.last_name} ${item.first_name} ${item.patronymic || ''}`.trim(); 
        },  

        async getData(pageNumber, orderingParam = '', search = '') {
            console.log("Fetching data for page:", pageNumber);
            try {            
                this.url = `${this.apiUrl}?page=${pageNumber}&page_size=${this.pageSize}` 
                
                if (orderingParam) {
                    this.url += `&ordering=${orderingParam}`
                }

                if (search) {
                     this.url += `&search=${encodeURIComponent(search)}`
                }
              
                for (const [field, value] of Object.entries(this.filters)) {
                    if (value) {
                        this.url += `&${field}=${encodeURIComponent(value)}`;
                    }
                }

                const response = await this.$axios.get(this.url);
                console.log("Data received:", response.data); 
                this.items = response.data.results;
                this.total = response.data.count;               
            } catch (error) {
                console.error("Ошибка получения данных:", error);
            }
        },
       
        openEditDialog(item) {
            this.isDialogOpen = true
            this.isEditing = true
            console.log("Форма:", this.form);
            this.form = { ...item };           
        },

        openCreateDialog() {
            this.isDialogOpen = true
            this.isEditing = false
            this.form = { ...item };
            this.form = {};           
        },

        closeDialog() {
            this.isDialogOpen = false         
            this.form = {}        
        },      

        handleSave() {
            console.log("data:", this.form);
            if (this.isEditing && !this.form.id) {
                console.error('ID записи не указан');
                alert('Не удалось найти ID записи для редактирования.');
                return; 
            }

            if (!this.isAuthenticated) {
                console.error("Пользователь не авторизован!");  
                this.$router.push({ name: "login" });             
                return; 
            }
             
            const dataToSend = {
                ...this.form,                
            };
           
            if (!this.form.photo || typeof this.form.photo === 'string') {
                delete dataToSend.photo;
            }           
           
            if (this.isEditing) {
                this.editItem(dataToSend); 
                
            } else {
                this.createItem(this.form);                 
            }
            this.closeDialog(); 
            
        },

        async createItem(data){
            console.log("Данные для отправки:", data);                 
            console.log("this.form.photo:", this.form.photo);        
            let url = `${this.apiUrl}`     
            const token = localStorage.getItem('accessToken')             
            if (!this.isAuthenticated) {
                console.error("Пользователь не авторизован!"); 
                this.$router.push({ name: "login" });                 
                return; 
            }              
            try {
                const response = await this.$axios.post(url, data, {
                    headers: {
                        'Content-Type': 'multipart/form-data',  
                        'Authorization': `Bearer ${token}`                              
                    }
                });
                console.log("response.data:", data);  
                this.items.push(response.data);
                this.fetchData();                                      
            }
            catch (error) {
                console.error("Ошибка создания:", error);                
            } 
        },

        async editItem(data) {  
            console.log("editdata:", data);                 
            let url = `${this.apiUrl}${data.id}/`  
            const token = localStorage.getItem('accessToken')               
            if (!this.isAuthenticated) {
                console.error("Пользователь не авторизован!");  
                this.$router.push({ name: "login" });             
                return; 
            } 
            try {      
                const response = await this.$axios.put(url, data, {
                    headers: {
                        'Content-Type': 'multipart/form-data', 
                        'Authorization': `Bearer ${token}`                           
                    }
                });

                const index = this.items.findIndex(item => item.id === response.data.id);
                if (index !== -1) {
                    this.items[index] = { ...this.items[index], ...response.data };
                }
                console.log("editresponse.data:", data);
            }
            catch (error) {
                console.error("Ошибка изменения:", error.response ? error.response.data : error.message);
            } 
                                 
        },

        async deleteItem(id) {
            console.log("ID записи для удаления:", id);
            let url = `${this.apiUrl}${id}/`  
            const token = localStorage.getItem('accessToken')   
            if (!this.isAuthenticated) {
                console.error("Пользователь не авторизован!");     
                this.$router.push({ name: "login" });             
                return; 
            }       
            if (confirm("Вы уверены, что хотите удалить эту запись?")) {
                try {
                    const response = await this.$axios.delete(url, {
                        headers: {
                            'Content-Type': 'multipart/form-data', 
                            'Authorization': `Bearer ${token}`                           
                        }
                    });
                    if (response){
                        this.page = 1
                        this.fetchData();                       
                    }
                }
                catch (error) {
                    console.error("Ошибка удаления:", error);
                }
            }
           
        },        
        
        // Расчет размера страницы
        getRowNumber(index) {
            return (this.page - 1) * this.pageSize + index + 1;
        },

        // Переход на предыдущую страницу
        prevPage() {            
            if (this.page > 1) {
                this.page--;
                this.fetchData();
            }
        },

        // Переход на следующую страницу
        nextPage() {
            if (this.page < this.totalPages) {
                this.page++;
                this.fetchData();
            }
        },

        // Смена страницы по номерам
        changePage(page) {
            this.page = page;     
            this.fetchData();      
        },

        // Смена размера страницы
        changePageSize(event) {
            this.pageSize = parseInt(event.target.value);
            this.page = 1;           
            this.fetchData();   
        },

        // Сортировка
        getSort(header) {
            const field = this.headerToFieldMap[header]
            if (this.sortBy === field) {
                this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc'; 
            } else {
                this.sortBy = field;
                this.sortOrder = 'asc'; 
            }
            this.fetchData();
        },
        
        // Поиск
        onSearchInput() {           
            this.page = 1
            this.fetchData();
        },

        // Очистка поля ввода
        clearInput() {
            this.searchText = ""
            this.fetchData();
        },

        // Фильтрация
        openFilter() {
            console.log("Фильтры:", this.filters)
            this.isFilterOpen = true
            //this.filters = {}
        },

        closeFilter() {
            console.log("Фильтры после close:", this.filters)
            this.isFilterOpen = false 
        
            //this.filters = {}   
            this.page = 1;
            this.fetchData();    
        },
      
        applyFilters() {
            console.log("Фильтры до close:", this.filters)
            this.isFilters = true
            this.page = 1;
            this.fetchData();
            this.closeFilter()
        },

        clearFilters() {         
            if (this.isFilters) {
                this.filters = {}                  
            }
            this.page = 1;
            this.fetchData();
        },

        // Popup
        openPopup(imageUrl) {
            this.currentImage = imageUrl; 
            this.isPopupVisible = true; 
        },
        
        fieldType(field) {          
            return this.fieldTypeMap[field] || 'text'; 
        },               

        isForeignKey(header) {
            return this.foreignKeysMap.hasOwnProperty(header);
        },

        onFileChange(event) {
            const file = event.target.files[0];
            console.log(file)
            if (file) {
                this.form.photo = file;         
            }
        },

        fetchData() {
            const orderingParam = this.sortOrder === 'asc' ? this.sortBy : `-${this.sortBy}`;
            this.getData(this.page, orderingParam, this.searchText);
        },
      
    },
   
    mounted() {
       //this.getData(this.page);  
       
    }
}
</script>

<style>

</style>
<template>
    <div v-if="isVisible" class="popup">
        <div class="popup-content">
            <span class="close" @click="closePopup">&times;</span>
            <img :src="imageUrl" alt="Popup Image" />
        </div>
    </div>
</template>

<script>
export default {
    props: {
        imageUrl: {
            type: String,
            required: true,
        },
        isVisible: {
            type: Boolean,
            required: true,
        }
    },
    methods: {
        closePopup() {
            this.$emit('close');
        }
    }
}
</script>

<style>
.popup {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.popup-content {
    position: relative;
    width: 50%;
    height: 50%;
}

.popup-content img {
    max-width: 50%;
    max-height: 50%;
}

.close {
    position: absolute;
    top: 10px;
    right: 20px;
    color: white;
    font-size: 30px;
    cursor: pointer;
}
</style>

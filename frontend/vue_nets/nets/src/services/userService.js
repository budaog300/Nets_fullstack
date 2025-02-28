import axios from 'axios';

const profileUrl = "http://localhost:8000/users/api/v1/profile/";
const logoutUrl = "http://localhost:8000/users/api/v1/logout/";

export const getUserProfile = async () => {
    const token = localStorage.getItem("accessToken");
    if (!token) {
        throw new Error("Токен не найден.");
    }
  
    const response = await axios.get(profileUrl, {
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'multipart/form-data',
        },
    });
    
    return response.data;
}

export const updateUserProfile = async (data) => {
    const token = localStorage.getItem("accessToken");
    if (!token) {
        throw new Error("Токен не найден.");
    }
    try {
        const response = await axios.put(profileUrl, data, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'multipart/form-data',
            },
        });
      
        return response.data;
    }
    catch (error) {
        console.error("Ошибка изменения:", error.response ? error.response.data : error.message);
    }
}

export const logoutUser = async () => {
    try {
        await axios.post(logoutUrl, {
            refresh_token: localStorage.getItem('refreshToken'),
        });
    }
    catch (error) {
        console.error('Ошибка выхода:', error);
    }
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    
    return true;
}

export const updateTokens = async () => {
    try {
        const response = await axios.post('http://localhost:8000/users/api/v1/token/refresh/', 
            { refresh: localStorage.getItem('refreshToken')}
        ) 

        localStorage.setItem('accessToken', response.data.access);
        localStorage.setItem('refreshToken', response.data.refresh);
        console.log("Токены обновлены:", response.data);

        return true
    }
    catch (error) {
        console.error('Ошибка при обновлении токена:', error);  
        return false;
    }  
   
} 
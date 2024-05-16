import axios from 'axios';

export async function fetchDishes(userId) {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/dishes?uid=${userId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching dishes:', error);
    return [];
  }
}

export async function addDish(name, image, favourite, userId) {
  try {
    const formData = new FormData();
    formData.append('name', name);
    formData.append('image', image);
    formData.append('favourite', favourite);
    formData.append('uid', userId);

    const response = await axios.post('http://127.0.0.1:8000/dishes/add', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    return response.data;
  } catch (error) {
    console.error('Error adding dish:', error);
    return null;
  }
}

export async function deleteDish(dishId) {
  try {
    await axios.delete(`http://127.0.0.1:8000/dishes/delete?did=${dishId}`);
    console.log('Dish deleted');
  } catch (error) {
    console.error('Error deleting dish:', error);
  }
}

export async function fetchUserProfile(userId) {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/me?uid=${userId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching user profile:', error);
    return null;
  }
}

export async function addIngredients(payload) {
  try {
    const response = await axios.post('http://127.0.0.1:8000/ingredients/add', payload, {
      headers: {
        'Content-Type': 'application/json'
      }
    });

    return response.data;
  } catch (error) {
    console.error('Error adding ingredients:', error);
    return null;
  }
}

export async function fetchIngredients(userId, dishId) {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/ingredients/select?uid=${userId}&did=${dishId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching ingredients:', error);
    return [];
  }
}

export async function getDishIdByName(userId, dishName) {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/dishes/select?uid=${userId}&dishname=${dishName}`);
    return response.data.dish_id; // 返回 dish_id
  } catch (error) {
    console.error('Error fetching dish ID:', error);
    return null;
  }
}

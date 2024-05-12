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

export async function deleteDish(userId, dishId) {
  try {
    await axios.delete(`http://127.0.0.1:8000/ingredients/delete?uid=${userId}&did=${dishId}`);
    console.log('Dish deleted');
  } catch (error) {
    console.error('Error deleting dish:', error);
  }
}

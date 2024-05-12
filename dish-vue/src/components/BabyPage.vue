<template>
  <div>
    <h1>Baby</h1>
    <p>User ID: {{ userId }}</p>

    <h2>Add Dish</h2>
    <form @submit.prevent="addDish">
      <label for="name">Name:</label>
      <input type="text" id="name" v-model="name" placeholder="Dish Name">

      <label for="image">Image:</label>
      <input type="file" id="image" @change="onFileChange">

      <label for="favourite">Favourite:</label>
      <input type="checkbox" id="favourite" v-model="favourite">

      <button type="submit">Add Dish</button>
    </form>

    <div v-if="dishes.length">
      <h2>User's Dishes:</h2>
      <ul>
        <li v-for="dish in dishes" :key="dish.id">
          <span>{{ dish.name }}</span>
          <img v-if="dish.image" :src="'data:image/jpeg;base64,' + dish.image" alt="Dish Image"
            style="max-width: 100px;">
          <button @click="deleteDish(dish.id)">Delete</button>
        </li>
      </ul>
    </div>

  </div>
</template>

<script>
import { fetchDishes, addDish, deleteDish } from '../services/api';

export default {
  data() {
    return {
      userId: null,
      name: '',
      image: null,
      favourite: false,
      dishes: [],
    };
  },
  created() {
    this.userId = this.$route.params.userId;
    this.fetchUserDishes();
  },
  methods: {
    async fetchUserDishes() {
      this.dishes = await fetchDishes(this.userId);
    },
    async addDish() {
      await addDish(this.name, this.image, this.favourite, this.userId);
      this.fetchUserDishes();
      this.name = '';
      this.image = null;
      this.favourite = false;
    },
    async deleteDish(dishId) {
      await deleteDish(this.userId, dishId);
      this.fetchUserDishes();
    },
    onFileChange(event) {
      this.image = event.target.files[0];
    },
  },
};
</script>
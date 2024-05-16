<template>
    <div class="add-dish-page">
      <h2>增加宝宝辅食</h2>
      <form @submit.prevent="addDish">
        <label for="name">Name:</label>
        <input type="text" id="name" v-model="name" placeholder="Dish Name">
  
        <label for="image">Image:</label>
        <input type="file" id="image" @change="onFileChange">
  
        <label for="favourite">Favourite:</label>
        <input type="checkbox" id="favourite" v-model="favourite">
  
        <button type="submit">Add Dish</button>
      </form>
    </div>
  </template>
  
  <script>
  import { addDish } from '../services/api';
  
  export default {
    data() {
      return {
        userId: null,
        name: '',
        image: null,
        favourite: false,
      };
    },
    created() {
      this.userId = this.$route.params.userId;
    },
    methods: {
      async addDish() {
        await addDish(this.name, this.image, this.favourite, this.userId);
        this.name = '';
        this.image = null;
        this.favourite = false;
      },
      onFileChange(event) {
        this.image = event.target.files[0];
      },
    },
  };
  </script>
  
  <style>
  .add-dish-page {
    background-color: #B5D8CF;
    padding: 20px;
    border-radius: 10px;
    max-width: 600px;
    margin: auto;
  }
  </style>
  
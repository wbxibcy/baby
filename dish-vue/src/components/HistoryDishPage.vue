<template>
  <div class="history-dish-page">
    <el-container>
      <el-header class="header">
        <el-input v-model="searchQuery" placeholder="搜索菜品..." class="search-input" clearable>
          <template #append>
            <el-button @click="searchDishes" icon="el-icon-search"></el-button>
          </template>
        </el-input>
        <el-select v-model="filter" @change="applyFilter" placeholder="显示" class="filter-select">
          <el-option label="全部" value="all"></el-option>
          <el-option label="收藏" value="favourite"></el-option>
        </el-select>
      </el-header>

      <el-main>
        <el-row :gutter="20" class="dishes-row">
          <el-col :span="24">
            <el-card v-for="dish in filteredDishes" :key="dish.id" class="dish-card">
              <div class="card-content">
                <span class="dish-name" @click="viewIngredients(dish)">{{ dish.name }}</span>
                <el-image v-if="dish.image" :src="'data:image/jpeg;base64,' + dish.image" alt="Dish Image"
                  class="dish-image" @click="viewIngredients(dish)"></el-image>
                <div class="card-actions">
                  <el-button type="danger" size="mini" @click="deleteDish(dish.id)">删除</el-button>
                  <el-button type="primary" size="mini" @click="editDish(dish)">编辑</el-button>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </el-container>

    <!-- Modal dialog for displaying ingredients -->
    <el-dialog :visible.sync="showModal" title="食材信息" width="30%">
      <ul>
        <li v-for="ingredient in ingredients" :key="ingredient.name">
          <span>{{ ingredient.name }}: {{ ingredient.quantity }} {{ ingredient.unit }}</span>
        </li>
      </ul>
      <span slot="footer" class="dialog-footer">
        <el-button @click="closeModal">关闭</el-button>
        <el-button type="primary" @click="openAddIngredientsModal">继续添加食材</el-button>
      </span>
    </el-dialog>

    <!-- Modal dialog for editing dish -->
    <el-dialog :visible.sync="showEditModal" title="编辑菜品" width="30%">
      <el-form>
        <el-form-item label="名字">
          <el-input v-model="editDishData.name"></el-input>
        </el-form-item>
        <el-form-item label="图片">
          <input type="file" @change="handleImageChange" />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="closeEditModal">关闭</el-button>
        <el-button type="primary" @click="updateDish">更新</el-button>
      </span>
    </el-dialog>

    <!-- Modal dialog for adding ingredients -->
    <el-dialog :visible.sync="showAddIngredientsModal" title="添加食材" width="30%">
      <div v-for="(ingredient, index) in newIngredients" :key="index">
        <el-form-item label="食材名字">
          <el-input v-model="ingredient.name"></el-input>
        </el-form-item>
        <el-form-item label="数量">
          <el-input v-model="ingredient.quantity" type="number"></el-input>
        </el-form-item>
        <el-form-item label="单位">
          <el-input v-model="ingredient.unit"></el-input>
        </el-form-item>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addIngredientField">添加更多食材</el-button>
        <el-button type="primary" @click="submitNewIngredients">提交</el-button>
        <el-button @click="closeAddIngredientsModal">关闭</el-button>
      </span>
    </el-dialog>
  </div>
</template>


<style>
html,
body {
  height: 100%;
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
}

.history-dish-page {
  background: url('../assets/history-background.png') no-repeat center center fixed;
  background-size: cover;
  height: 100vh;
  /* Ensure the background covers the entire viewport */
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background: rgba(255, 255, 255, 0.7);
  /* Semi-transparent background */
  border-radius: 10px;
}

.filter-select {
  margin-right: 10px;
  min-width: 100px;
  /* Adjust size as needed */
}

.search-input {
  flex-grow: 1;
  max-width: 50%;
  /* Adjust the width to 50% */
  margin: 0 auto;
  /* Center the search input */
}


.dishes-row {
  margin-top: 20px;
}

.dish-card {
  margin-bottom: 20px;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  background: rgba(255, 255, 255, 0.8);
  /* Semi-transparent background */
}

.card-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.dish-name {
  cursor: pointer;
  flex-grow: 1;
}

.dish-image {
  max-width: 100px;
  margin-left: 10px;
  margin-right: 10px;
  cursor: pointer;
}

.card-actions {
  display: flex;
  flex-direction: column;
}

.card-actions .el-button {
  margin-top: 5px;
}

/* Modal dialog styles */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
}

.modal-content h3 {
  margin-top: 0;
}

.modal-content ul {
  list-style: none;
  padding: 0;
}

.modal-content li {
  margin-bottom: 10px;
}

.modal-content button {
  margin-top: 10px;
}
</style>


<script>
import {
  fetchDishes,
  deleteDish,
  fetchIngredients,
  fetchFavouriteDishes,
  searchDishes,
  updateDish,
  addIngredients
} from '../services/api';

export default {
  data() {
    return {
      userId: null,
      dishes: [],
      favouriteDishes: [],
      searchResults: [],
      filter: 'all',
      searchQuery: '',
      showModal: false,
      showEditModal: false,
      showAddIngredientsModal: false,
      ingredients: [],
      currentDishId: null,
      editDishData: {
        id: null,
        name: '',
        image: null
      },
      newIngredients: [
        { name: '', quantity: '', unit: '' }
      ]
    };
  },
  computed: {
    filteredDishes() {
      if (this.searchQuery) {
        return this.searchResults;
      } else if (this.filter === 'favourite') {
        return this.favouriteDishes;
      }
      return this.dishes;
    }
  },
  created() {
    this.userId = this.$route.params.userId;
    this.fetchUserDishes();
    this.fetchFavouriteDishes();
  },
  methods: {
    async fetchUserDishes() {
      this.dishes = await fetchDishes(this.userId);
    },
    async fetchFavouriteDishes() {
      this.favouriteDishes = await fetchFavouriteDishes(this.userId);
    },
    async deleteDish(dishId) {
      await deleteDish(dishId);
      this.fetchUserDishes();
      this.fetchFavouriteDishes();
    },
    async viewIngredients(dish) {
      this.currentDishId = dish.id;
      this.ingredients = await fetchIngredients(this.userId, dish.id);
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
    async searchDishes() {
      if (this.searchQuery) {
        this.searchResults = await searchDishes(this.userId, this.searchQuery);
      } else {
        this.searchResults = [];
      }
    },
    applyFilter() {
      // Filter logic can be applied here if needed
    },
    editDish(dish) {
      this.editDishData.id = dish.id;
      this.editDishData.name = dish.name;
      this.editDishData.image = null; // Clear the current image
      this.showEditModal = true;
    },
    closeEditModal() {
      this.showEditModal = false;
    },
    handleImageChange(event) {
      this.editDishData.image = event.target.files[0];
    },
    async updateDish() {
      const { id, name, image } = this.editDishData;
      const result = await updateDish(id, name, image);
      if (result && result.message === 'Update successful') {
        this.fetchUserDishes();
        this.fetchFavouriteDishes();
        this.closeEditModal();
      } else {
        alert('更新失败');
      }
    },
    openAddIngredientsModal() {
      this.newIngredients = [{ name: '', quantity: '', unit: '' }];
      this.showAddIngredientsModal = true;
    },
    closeAddIngredientsModal() {
      this.showAddIngredientsModal = false;
    },
    addIngredientField() {
      this.newIngredients.push({ name: '', quantity: '', unit: '' });
    },
    async submitNewIngredients() {
      const payload = {
        uid: this.userId,
        did: this.currentDishId,
        ingredients: this.newIngredients.map(ingredient => ({
          ...ingredient,
          quantity: Number(ingredient.quantity) // Ensure quantity is a number
        }))
      };

      const result = await addIngredients(payload);
      if (result) {
        this.viewIngredients({ id: this.currentDishId }); // Reload ingredients information
        this.closeAddIngredientsModal();
      } else {
        alert('添加食材失败');
      }
    }
  },
};
</script>

<template>
  <el-container class="add-dish-page">
    <el-main>
      <!-- Steps Bar -->
      <el-steps :active="step - 1" :finish-status="isFinished ? 'success' : 'wait'" class="steps">
        <el-step title="Step 1" description="填写菜品信息"></el-step>
        <el-step title="Step 2" description="添加食材"></el-step>
        <el-step title="Step 3" description="完成"></el-step>
      </el-steps>

      <div v-if="step === 1" class="form-container">
        <el-form @submit.prevent="nextStep" label-width="100px">
          <el-form-item label="名称">
            <el-input v-model="name" placeholder="Dish Name" required></el-input>
          </el-form-item>
          <el-form-item label="图片">
            <input type="file" @change="onFileChange" required>
          </el-form-item>
          <el-form-item label="收藏">
            <el-checkbox v-model="favourite"></el-checkbox>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" native-type="submit">下一步</el-button>
          </el-form-item>
        </el-form>
      </div>

      <div v-if="step === 2" class="form-container">
        <h3>添加食材</h3>
        <el-form @submit.prevent="submitIngredients" label-width="100px">
          <div v-for="(ingredient, index) in ingredients" :key="index" class="ingredient">
            <el-form-item label="名称">
              <el-input v-model="ingredient.name" placeholder="Ingredient Name" required></el-input>
            </el-form-item>
            <el-form-item label="数量">
              <el-input-number v-model="ingredient.quantity" placeholder="Quantity" required></el-input-number>
            </el-form-item>
            <el-form-item label="单位">
              <el-input v-model="ingredient.unit" placeholder="Unit" required></el-input>
            </el-form-item>
            <el-button type="danger" @click="removeIngredient(index)">删除</el-button>
          </div>
          <el-form-item>
            <el-button type="primary" @click="addNewIngredient">添加更多食材</el-button>
            <el-button type="primary" native-type="submit">提交食材</el-button>
            <el-button type="default" @click="skipIngredients">跳过食材</el-button>
          </el-form-item>
        </el-form>
      </div>

      <div v-if="step === 3" class="form-container">
        <h3>菜品添加完成!</h3>
        <el-button type="primary" @click="goToHomePage">返回主页</el-button>
      </div>

      <!-- Modal Dialog -->
      <el-dialog :title="modalTitle" v-model:visible="showModal" width="30%">
        <p>{{ modalMessage }}</p>
        <template #footer>
          <el-button type="primary" @click="goToHomePage">返回主页</el-button>
        </template>
      </el-dialog>
    </el-main>
  </el-container>
</template>

<style>
html,
body {
  height: 100%;
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
}

.add-dish-page {
  background: url('../assets/addpage-background.png') no-repeat center center fixed;
  background-size: cover;
  height: 100vh; /* Ensures the container takes the full height of the viewport */
  display: flex;
  align-items: center;
  justify-content: center;
}

.el-main {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.steps {
  width: 80%;
  max-width: 800px;
  margin-bottom: 40px;
  display: flex;
  justify-content: center;
}

.form-container {
  background-color: rgba(255, 255, 255, 0.9);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.ingredient {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  align-items: center;
  margin-bottom: 20px;
  width: 100%;
}

.ingredient > .el-form-item {
  flex: 1;
  min-width: 150px;
  margin-right: 20px;
}

.ingredient > .el-button {
  align-self: flex-start;
  margin-top: 28px;
}

.el-form-item {
  width: 100%;
}
</style>

<script>
import { addDish, addIngredients, getDishIdByName } from '../services/api';
import { ElSteps, ElStep, ElForm, ElFormItem, ElInput, ElCheckbox, ElButton, ElDialog, ElInputNumber } from 'element-plus';

export default {
  components: {
    ElSteps,
    ElStep,
    ElForm,
    ElFormItem,
    ElInput,
    ElCheckbox,
    ElButton,
    ElDialog,
    ElInputNumber
  },
  data() {
    return {
      userId: null,
      name: '',
      image: null,
      favourite: false,
      step: 1,
      showModal: false,
      dishId: null,
      ingredients: [
        { name: '', quantity: '', unit: '' }
      ],
      modalTitle: '',
      modalMessage: '',
      isFinished: false,
    };
  },
  created() {
    this.userId = this.$route.params.userId;
  },
  methods: {
    async nextStep() {
      try {
        const response = await addDish(this.name, this.image, this.favourite, this.userId);
        if (response) {
          const dishId = await getDishIdByName(this.userId, this.name);
          if (dishId) {
            this.dishId = dishId;
            this.step = 2;
          } else {
            this.showErrorModal('获取菜品ID失败，请重试。');
          }
        } else {
          this.showErrorModal('添加菜品失败，请重试。');
        }
      } catch (error) {
        console.error('Error adding dish:', error);
        this.showErrorModal('添加菜品时发生错误，请重试。');
      }
    },
    onFileChange(event) {
      this.image = event.target.files[0];
    },
    addNewIngredient() {
      this.ingredients.push({ name: '', quantity: '', unit: '' });
    },
    removeIngredient(index) {
      this.ingredients.splice(index, 1);
    },
    async submitIngredients() {
      try {
        const payload = {
          uid: this.userId,
          did: this.dishId,
          ingredients: this.ingredients.map(ingredient => ({
            ...ingredient,
            quantity: Number(ingredient.quantity)
          }))
        };
        console.log('Submitting ingredients:', payload);
        const response = await addIngredients(payload);
        if (response) {
          this.step = 3; // Move to step 3
          this.isFinished = true;
          this.showSuccessModal();
        } else {
          this.showErrorModal('添加食材失败，请重试。');
        }
      } catch (error) {
        console.error('Error adding ingredients:', error);
        this.showErrorModal('添加食材时发生错误，请重试。');
      }
    },
    skipIngredients() {
      this.step = 3; // Move to step 3
      this.isFinished = true;
      this.showSuccessModal();
    },
    stayOnPage() {
      this.showModal = false;
    },
    goToHomePage() {
      this.$router.push({ name: 'BabyPage', params: { userId: this.userId } });
    },
    showErrorModal(message) {
      this.modalTitle = '错误';
      this.modalMessage = message;
      this.showModal = true;
    },
    showSuccessModal() {
      this.modalTitle = '恭喜你添加成功!';
      this.modalMessage = '你想留在这个页面还是返回主页?';
      this.showModal = true;
    }
  },
};
</script>

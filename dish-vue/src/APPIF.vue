<template>
    <div class="common-layout">
      <el-container>
        <el-header class="header">Header</el-header>
        <el-main class="main">
          <div>
            <el-radio-group v-model="size" aria-label="size control">
              <el-radio-button value="large">large</el-radio-button>
              <el-radio-button value="default">default</el-radio-button>
              <el-radio-button value="small">small</el-radio-button>
            </el-radio-group>
            <el-radio-group v-model="labelPosition" aria-label="position control">
              <el-radio-button value="left">Left</el-radio-button>
              <el-radio-button value="right">Right</el-radio-button>
              <el-radio-button value="top">Top</el-radio-button>
            </el-radio-group>
          </div>
          <br />
          <el-form
            ref="form"
            style="max-width: 600px"
            label-width="auto"
            :label-position="labelPosition"
            :size="size"
          >
            <el-form-item label="Activity name">
              <el-input/>
            </el-form-item>
            <!-- 其他表单项 -->
            <el-form-item>
              <el-button type="primary">Create</el-button>
              <el-button>Cancel</el-button>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
    </div>
  </template>
  
  <script>
//   import { reactive, ref } from 'vue'
  
//   const size = ref('default')
//   const labelPosition = ref('right')
  </script>
  
  <style>
  .common-layout {
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .el-container {
    width: 80%;
    height: 80%;
    border: 1px solid #ccc;
    border-radius: 5px;
    overflow: hidden;
  }
  
  .header {
    background-color: #409eff;
    color: #fff;
    text-align: center;
    padding: 20px;
  }
  
  .main {
    padding: 20px;
  }
  </style>
  
<template>
  <div id="app">
    <el-container>
      <el-header style="background: #409EFF; color: white; display: flex; align-items: center; padding: 0 20px;">
        <h2 style="margin: 0;">🎯 GEO 自动获客系统</h2>
      </el-header>
      <el-main>
        <LeadsView />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import LeadsView from './views/Leads.vue'
</script>
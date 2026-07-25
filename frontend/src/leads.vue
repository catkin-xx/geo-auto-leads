<template>
  <div>
    <!-- 筛选栏 -->
    <el-card style="margin-bottom: 20px;">
      <el-form :inline="true">
        <el-form-item label="城市">
          <el-select v-model="filters.city" placeholder="全部" clearable>
            <el-option label="南京" value="南京" />
            <el-option label="苏州" value="苏州" />
            <el-option label="广州" value="广州" />
            <el-option label="深圳" value="深圳" />
          </el-select>
        </el-form-item>
        <el-form-item label="行业">
          <el-select v-model="filters.industry" placeholder="全部" clearable>
            <el-option label="家电维修" value="家电维修" />
            <el-option label="开锁" value="开锁" />
            <el-option label="家政" value="家政" />
            <el-option label="美甲美睫" value="美甲美睫" />
            <el-option label="黄金回收" value="黄金回收" />
          </el-select>
        </el-form-item>
        <el-form-item label="最低评分">
          <el-input-number v-model="filters.min_score" :min="0" :max="100" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchLeads">查询</el-button>
          <el-button @click="batchScore">批量评分</el-button>
          <el-button type="success" @click="batchOutreach">一键触达</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 客户列表 -->
    <el-card>
      <el-table :data="leads" style="width: 100%" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" />
        <el-table-column prop="name" label="名称" min-width="150
<template>
  
  <div>
    <el-tree
      :data="fileTree"
      node-key="id"
      default-expand-all
      highlight-current
      @node-click="handleNodeClick"
    />
  </div>
</template>

<script>
import plantumlEncoder from 'plantuml-encoder';
export default {
  name: "PlantUMLRight",
  data() {
    return {
      fileTree: [
        {
          id: 1,
          label: "项目根目录",
          children: [
            {
              id: 2,
              label: "src",
              children: [
                { id: 3, label: "components", children: [] },
                { id: 4, label: "views", children: [] },
                { id: 5, label: "App.vue" },
              ],
            },
            { id: 6, label: "public", children: [{ id: 7, label: "index.html" }] },
            { id: 8, label: "package.json" },
          ],
        },
      ],
    };
  },
  methods: {
    handleNodeClick(node) {
      console.log("选中节点:", node);
    },
  },
  
};
</script>

<style scoped>
.scaled-image {
    transition: transform 0.3s ease;
    transform-origin: left; /* 缩放中心 */
}
/* 遮罩层 */
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 50%;
  width: 50%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  color: white;
}

/* 对话框内容 */
.dialog-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  border: none;
  background: red;
  color: white;
  font-size: 16px;
  cursor: pointer;
}
</style>

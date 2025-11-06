<template>
  <div class="mainContainer">
    <div class="mainContainer1">
      <div class="left" :style="{ width: leftWidth + 'px' }">
        <LeftPart @left-done='handleLeftDone' />
      </div>


      <!-- 拖拽条（左边界） -->
    <div class="drag-handle drag-left" @mousedown="startDragging('left')"></div>

      <div class="main">
        <MainPart ref="Main"/>
      </div>


      <!-- 拖拽条（右边界） -->
    <div class="drag-handle drag-right" @mousedown="startDragging('right')"></div>
      
      <div class="right" :style="{ width: rightWidth + 'px' }">
        <RightPart />
      </div>
    </div>
  </div>
</template>

<script>
import LeftPart from '@/components/new/leftPart.vue';
import MainPart from '@/components/new/mainPart.vue';
import RightPart from '@/components/new/rightPart.vue';


export default {
  name: 'HomePage',
  components: {
    LeftPart,
    MainPart,
    RightPart,
    
  },
  data()
  {
    return {
      leftWidth: 250,
      rightWidth: 1000,
      isDragging: false,
      dragSide: null,
      startX: 0,
      startWidth: 0,
    };
  },
  methods: {
    handleLeftDone() {
      console.log('left done --- Home')
      this.$refs.Main.showTable();
    },
    startDragging(side) {
      this.isDragging = true;
      this.dragSide = side;
      this.startX = event.clientX;
      this.startWidth = side === 'left' ? this.leftWidth : this.rightWidth;

      document.addEventListener("mousemove", this.onDrag);
      document.addEventListener("mouseup", this.stopDragging);
    },
    onDrag(event) {
      if (!this.isDragging) return;

      const delta = event.clientX - this.startX;
      if (this.dragSide === 'left') {
        this.leftWidth = Math.max(150, this.startWidth + delta); // 最小宽度限制
      } else if (this.dragSide === 'right') {
        this.rightWidth = Math.max(150, this.startWidth - delta); // 注意右侧是减去 delta
      }
    },
    stopDragging() {
      this.isDragging = false;
      document.removeEventListener("mousemove", this.onDrag);
      document.removeEventListener("mouseup", this.stopDragging);
    },
  },
}
</script>

<style scoped>
/* 主容器布局 */
.mainContainer {
  height: 100%;
  width: 100%;
  display: inline-block;
  overflow-y: auto;
  background-color: #F1F0E8;
}

.mainContainer1 {
  height: 100%;
  width: 100%;
  display: flex;
}

.left {
  width: 20%;
  height: 99%;
  display: flex;
  margin: 0.2%;
  border: 1px solid #2973B2;
;
}

.main {
  width: 40%;
  height: 99%;
  display: flex;
  margin: 0.2%;
  border: 1px solid #2973B2;
}

.right {
  width: 40%;
  height: 99%;
  display: flex;
  margin: 0.2%;
  border: 1px solid #2973B2;
}

/* 拖拽条样式 */
.drag-handle {
  width: 5px;
  background-color: rgba(0, 0, 0, 0.1);
  cursor: ew-resize;
  height: 100%;
  z-index: 10;
}

</style>

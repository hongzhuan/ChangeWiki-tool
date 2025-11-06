<template>
    <div class="mainContainer">
        <div class="top" :style="{ height: topHeight + 'px' }">
            <strong class="title">架构变更视图</strong>
            <ArchitectureChange />
        </div>

        <!-- 拖拽条 -->
        <div class="vertical-drag" @mousedown="startVerticalDrag"></div>

        <div class="bottom">

            <strong class="title">架构变更分析结果展示</strong>
            <TableShow ref="table"/>
        </div>
    </div>
</template>

<script>
import ArchitectureChange from '@/components/new/main/architectureChange.vue';
import AnalysisProgress from '@/components/new/main/analysisProgress.vue';
import TableShow from '@/components/new/main/TableShow.vue';

export default {
    name: 'MainPart',
    components: {
        ArchitectureChange,
        AnalysisProgress,
        TableShow
    },
    data() {
        return {
        topHeight: 500, // 初始高度（px）
        isDragging: false,
        startY: 0,
        startHeight: 0,
        };
    },
    methods: {
        showTable(){
            console.log('Home --- Main')
            this.$refs.table.convertData();
        },
        startVerticalDrag(event) {
        this.isDragging = true;
        this.startY = event.clientY;
        this.startHeight = this.topHeight;
        document.addEventListener("mousemove", this.onVerticalDrag);
        document.addEventListener("mouseup", this.stopVerticalDrag);
        },
        onVerticalDrag(event) {
        if (!this.isDragging) return;
        const delta = event.clientY - this.startY;
        const newHeight = this.startHeight + delta;
        this.topHeight = Math.max(100, Math.min(newHeight, window.innerHeight - 100));
        },
        stopVerticalDrag() {
        this.isDragging = false;
        document.removeEventListener("mousemove", this.onVerticalDrag);
        document.removeEventListener("mouseup", this.stopVerticalDrag);
        },
    },
}
</script>

<style scoped>
.mainContainer {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column; /* 竖直方向布局 */
    overflow-x: auto;       /* 横向滚动 */
    width: 100%;
}

.top {
    width: 100%;
    flex: 1;
    overflow-x: auto;
    display: flex;
    flex-direction: column;
}

.bottom {
    /* width: 100%;
    flex: 1;
    overflow-x: auto; */
    /* display: flex; */
    /* flex-direction: column; */
    width: 100%;
    flex: 1;
    overflow-x: auto;
}

.title {
    color: black;
    font-size: 1.5rem;
    margin: 2% 0 0 2%;
    margin-left: 10px;
    display: flex;
    font-family: 'Microsoft YaHei';
    padding: 5px;
}
.vertical-drag {
  height: 6px;
  background-color: #ccc;
  cursor: ns-resize;
  user-select: none;
}
</style>
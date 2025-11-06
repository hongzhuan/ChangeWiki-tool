<template>
    <div class="mainContainer">
         <h2 style="font-family: 'Microsoft YaHei';color:black;font-size: 1.5rem">📦 任务执行进度</h2>
    
        <!-- 按钮居中对齐 -->
        <div class="button-container">
        <button @click="startTask" class="start-button" :disabled="isComplete">开始执行任务</button>
        </div>
        <div>
            <!-- 树形任务进度展示 -->
            <el-tree
            :data="tasks"
            :props="treeProps"
            node-key="id"
            default-expand-all
            class="task-tree"
            >
                <template slot-scope="{ data }">
                    <div class="task-node">
                    <div class="task-header">
                        <span class="task-name">{{ data.name }}</span>
                        <span class="progress-label" :class="{'completed': data.progress === 100}">{{ data.progress }}%</span>
                    </div>
                    <el-progress :percentage="data.progress" :status="data.progress === 100 ? 'success' : ''" class="progress-bar"></el-progress>
                    </div>
                </template>
            </el-tree>
        </div>
        
        <!-- 任务完成提示 -->
        <br />
        <p v-if="isComplete" class="success-message">🎉 所有任务执行完成！</p>
    </div>
</template>

<script>
import io from 'socket.io-client';
export default {
    name: 'AnalysisProgress',
    data() {
        return {
        socket: null,
        tasks: [],
        isComplete: false,
        treeProps: {
            label: "name",
            children: "children"
        }
        };
    },
    methods: {
        startTask() {
        fetch("http://localhost:5000/start")
            .then(response => response.json())
            .then(data => console.log(data));
        
        this.isComplete = false;
        }
    },
    mounted() {
        this.socket = io("http://localhost:5000");

        this.socket.on("progress_update", (data) => {
        this.tasks = data.tasks;
        });

        this.socket.on("progress_complete", () => {
        this.isComplete = true;
        this.socket.disconnect();
        });
    }
}
</script>

<style scoped>
.mainContainer {
    width: 100%;
    height: 100%;
    display: flex;
    background: #BCCCDC;
    /* max-width: 500px;
    margin: 20px auto; */
    /* text-align: center; */
}
/* 树形任务进度 */
.task-tree {
  text-align: left;
  padding-left: 20px;
  height: 100%;
}

.start-button {
  padding: 8px 16px;
  background-color: #2973B2;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  height: 40px;
  width: 125px;
  margin-top: 10px;
  margin-left: 10px;
}
.start-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
.start-button:hover {
  background-color: #9ACBD0;
  transform: translateY(-2px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}
.task-node {
  display: flex;
  justify-content: space-between;
  width: 120%;
}
.progress-label {
  margin-left: 4px;
  font-weight: bold;
  color: #666;
}
.completed {
  color: green;
}
.success-message {
  color: green;
  font-weight: bold;
}
</style>
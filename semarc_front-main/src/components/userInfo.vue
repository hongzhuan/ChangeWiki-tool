<!-- filepath: src/components/userInfo.vue -->
<template>
  <div class="user-info-container">
    <h2 style=" color: black; border-color: black; font-family: 'Courier New', Courier, monospace;">用户信息</h2>
    <div class="info-row">
      <span style=" color: black; border-color: black; font-size: 1.2rem; font-family: 'Courier New', Courier, monospace;" class="info-label">用户名：</span>
      <span style=" color: black; border-color: black; font-size: 1.2rem; font-family: 'Courier New', Courier, monospace;" v-if="!editing">{{ username }}</span>
      <input v-else v-model="editUsername" />
    </div>
    <div class="info-row">
      <span style=" color: black; border-color: black; font-size: 1.2rem; font-family: 'Courier New', Courier, monospace;" class="info-label">密码：</span>
      <span style=" color: black; border-color: black; font-size: 1.2rem; font-family: 'Courier New', Courier, monospace;" v-if="!editing">{{ Password }}</span>
      <input v-else type="password" v-model="Password" />
    </div>
    <div class="info-row">
      <span style=" color: black; border-color: black; font-size: 1.2rem; font-family: 'Courier New', Courier, monospace;" class="info-label">邮箱：</span>
      <span style=" color: black; border-color: black; font-size: 1.2rem; font-family: 'Courier New', Courier, monospace;" v-if="!editing">{{ email }}</span>
      <input v-else v-model="editEmail" />
    </div>
    <div class="btn-group">
      <button style=" width: 60%; color: black; border-color: black; font-size: 1.2rem; font-family: 'Courier New', Courier, monospace;" class="btn" v-if="!editing" @click="startEdit">编辑信息</button>
      <button style=" width: 60%; color: black; border-color: black; font-size: 1.2rem; font-family: 'Courier New', Courier, monospace;" class="btn" v-else @click="saveEdit">保存</button>
      <button style=" width: 60%; color: black; border-color: black; font-size: 1.2rem; font-family: 'Courier New', Courier, monospace;" class="btn" @click="goBack">返回</button>
    </div>
    <p v-if="success" style="color:green">{{ success }}</p>
    <p v-if="error" style="color:red">{{ error }}</p>
  </div>
</template>

<script>


export default {
  data() {
    return {
      username: localStorage.getItem("username") || "未设置",
      Password: localStorage.getItem("password") || "未设置",
      email: localStorage.getItem("email") || "未设置",
      editing: false,
      editUsername: "",
      editEmail: "",
      success: "",
      error: ""
    };
  },
  async created() {
    /* 打开页面立即从后端拿真实信息 */
    try {
      const res = await fetch(`http://localhost:5000/api/user/${this.username}`)
      if (res.ok) {
        const data = await res.json()
        this.username = data.username
        this.password = data.password
        this.email = data.email || '未设置'
      }
    } catch (e) {
      console.error('获取用户信息失败', e)
    }
  },
  methods: {
    startEdit() {
      this.editing = true;
      this.editUsername = this.username;
      this.editEmail = this.email;
      this.success = "";
      this.error = "";
    },
    async saveEdit() {
      this.success = ''
      this.error = ''

      if (!this.editUsername.trim() || !this.editEmail.trim()) {
        this.error = '用户名和邮箱不能为空'
        return
      }
      if (!this.validateEmail(this.editEmail)) {
        this.error = '邮箱格式不正确'
        return
      }

      try {
        const res = await fetch(`http://localhost:5000/api/user/${this.username}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            newUsername: this.editUsername,
            newPassword: this.Password,   // 允许留空表示不改
            newEmail: this.editEmail
          })
        })
        const data = await res.json()
        if (res.ok) {
          /* 更新本地变量与 localStorage */
          this.username = this.editUsername
          this.email = this.editEmail
          localStorage.setItem('username', this.username)
          localStorage.setItem('email', this.email)
          if (this.Password) {
            localStorage.setItem('password', this.Password)
          }
          this.editing = false
          this.success = data.message
        } else {
          this.error = data.message || '保存失败'
        }
      } catch (err) {
        this.error = '网络错误，请稍后重试'
      }
    },
    validateEmail(email) {
      return /^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/.test(email);
    },
    goBack() {
      this.$router.back();
    }
  }
};
</script>

<style scoped>
.user-info-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 10px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  position: relative;
  overflow: hidden;
  cursor: pointer;
}
.info-row {
  margin: 16px 0;
  font-size: 18px;
  display: flex;
  align-items: center;
}
.info-label {
  font-weight: bold;
  margin-right: 8px;
  min-width: 60px;
}
.info-row input {
  padding: 6px 10px;
  font-size: 16px;
  border: 1px solid #bbb;
  border-radius: 4px;
}
.btn-group {
  margin-top: 24px;
  display: flex;
  gap: 16px;
}
.btn {
  padding: 8px 24px;
  font-size: 1.1rem;
  color: black;
  border: 1px solid black;
  border-radius: 6px;
  background: #fff;
  cursor: pointer;
  font-family: 'Courier New', Courier, monospace;
}
.btn:hover {
  background: #f0f0f0;
}


</style>
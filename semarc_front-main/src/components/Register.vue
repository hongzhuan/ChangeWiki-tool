<!-- filepath: src/components/Register.vue -->
<template>
  <div class="register-container">
    <h2>用户注册</h2>
    <input v-model="username" placeholder="用户名" />
    <input v-model="password" type="password" placeholder="密码（至少6位）" />
    <input v-model="email" placeholder="邮箱" />
    <button class="btn" style=" width: 10%; color: black; border-color: black; font-size: 1.2rem; font-family: 'Courier New', Courier, monospace;" @click="register">注册</button>
    <button class="btn" style=" width: 10%; color: black; border-color: black; font-size: 1.2rem; font-family: 'Courier New', Courier, monospace;" @click="goToLogin">返回登录</button>
    <p v-if="error" style="color:red">{{ error }}</p>
    <p v-if="success" style="color:green">{{ success }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      email: '',
      error: '',
      success: ''
    }
  },
  methods: {
    validateEmail(e) {
      return /^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/.test(e)
    },
    async register() {
      this.error = ''
      this.success = ''
      if (!this.username.trim() || !this.password.trim() || !this.email.trim()) {
        this.error = '所有字段不能为空'
        return
      }
      if (this.password.length < 6) {
        this.error = '密码长度不能少于6位'
        return
      }
      if (!this.validateEmail(this.email)) {
        this.error = '邮箱格式不正确'
        return
      }

      try {
        const res = await fetch('http://localhost:5000/api/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: this.username,
            password: this.password,
            email: this.email
          })
        })
        const data = await res.json()
        if (res.status === 201) {
          this.success = '注册成功！即将跳转到登录页面...'
          setTimeout(() => this.$router.push('/'), 1500)
        } else {
          this.error = data.message || '注册失败'
        }
      } catch (e) {
        this.error = '网络错误，请稍后重试'
      }
    },
    goToLogin() {
      this.$router.push('/')
    }
  }
}
</script>


<style scoped>
.register-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  position: relative;
  overflow: hidden;
  cursor: pointer;
}
.register-container input {
  margin: 8px 0;
  padding: 8px;
  width: 220px;
}
.register-container button {
  margin-top: 12px;
  padding: 8px 24px;
}
</style>
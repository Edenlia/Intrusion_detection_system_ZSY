<template>
  <q-page class="flex" style="background: #f0f2f5">
    <div class=" full-width column bg-white q-ma-md" style="height: 650px">
      <div class="col-2 text-h4 q-ma-md">修改密码</div>
      <q-form class="col-6 column q-ml-md" style="width: 30%"
              @submit="change_password">
        <q-input
          class="col-3"
          filled
          v-model="username"
          label="用户名"/>
        <q-input
          class="col-3"
          filled
          v-model="password"
          label="密码"/>
        <q-input
          class="col-3"
          filled
          v-model="confirm"
          label="确认密码"/>
        <div class="col-1"></div>
        <q-btn class="full-width col-2" label="确认修改" type="submit" color="blue"></q-btn>
      </q-form>
    </div>
  </q-page>
</template>

<script>
export default {
  name: "Email"
}
</script>

<style scoped>

</style>

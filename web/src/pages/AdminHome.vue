<template>
  <q-page class="flex" style="background:#112347">
    <div class=" full-width column q-mx-md q-py-xs" style="height: 650px">
      <q-table
        class="my-sticky-header-table"
        color="primary"
        card-class=" "
        table-class="text-grey-8"
        table-header-class="text-brown"
        title="用户信息"
        :rows=rows
        :columns=columns
        row-key="id"
        flat
        bordered
        @row-click="go_analytics_detail"
      >
      </q-table>
    </div>
    <!--    <div class=" full-width column q-mx-md q-py-xs">-->
    <!--      <q-table-->
    <!--        class="my-sticky-header-table"-->
    <!--        color="primary"-->
    <!--        card-class="bg-amber-2 text-brown"-->
    <!--        table-class="text-grey-8"-->
    <!--        table-header-class="text-brown"-->
    <!--        title="已查看入侵信息"-->
    <!--        :rows=rows2-->
    <!--        :columns=columns-->
    <!--        row-key="id"-->
    <!--        flat-->
    <!--        bordered-->
    <!--        @row-click="go_case_detail"-->
    <!--      ></q-table>-->
    <!--    </div>-->
  </q-page>
</template>
<script>
import {api} from "boot/axios";
import {Notify} from "quasar";

export default {
  name: "Case",
  created(){
    this.get_user_data()
  },
  data(){
    return{
      columns: [
        {
          name: 'id',
          required: true,
          label: '用户编号',
          align: 'left',
          field: row => row.id,
          sortable: true
        },
        { name: 'user_name', align: 'center', label: '用户名', field: 'user_name'},
        { name: 'permission', label: '权限类型', field: 'permission'},
        { name: 'camera_num', label: '摄像头数量', field: 'camera_num' },
        { name: 'date_time', label: '注册时间', field: 'date_time' },
      ],
      rows: []
    }
  },
  methods:{
    go_analytics_detail(evt, row){
      this.$router.push('/admin_user_analytics/' + row.id)
    },
    get_user_data(){
      let _this = this
      api.post("http://172.30.68.249:8000/api/log/query_all/", {

      }).then(function(response){
        console.log(response)
        let res = response.data
        if(res.status === "Success"){
          let user_list = res.user_list
          console.log(user_list)
          for(let i = 0; i < user_list.length; i++){
            let row = {}
            row.id = user_list[i].id
            row.user_name = user_list[i].username
            row.permission = user_list[i].permission === 0? '用户':'管理员'
            row.camera_num = user_list[i].camera_num
            row.date_time = user_list[i].date_time
            _this.rows.push(row)
          }
        }else{
          Notify.create(
            {
              type: 'negative',
              message: '未知错误'
            }
          )
        }
      }).catch(function (error){
        console.log(error)
        Notify.create(
          {
            type: 'negative',
            message: '内部错误'
          })
      })
    }
  }
}
</script>

<style lang="sass" scoped>
.my-sticky-header-table
  /* height or max-height is important */
  height: 850px
  .q-table__top,
  .q-table__bottom,
  thead tr:first-child th
  /* bg color is important for th; just specify one */
  thead tr th
    position: sticky
    z-index: 1
  thead tr:first-child th
    top: 0
  /* this is when the loading indicator appears */
  &.q-table--loading thead tr:last-child th
    /* height of all previous header rows */
    top: 48px
</style>

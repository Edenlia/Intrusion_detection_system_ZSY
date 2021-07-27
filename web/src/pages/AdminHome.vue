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
export default {
  name: "Case",
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
        { name: 'detected_camera', align: 'center', label: '用户名', field: 'camera_name'},
        { name: 'case_type', label: '权限类型', field: 'case_type', sortable: true },
        { name: 'level', label: '摄像头数量', field: 'level' },
        { name: 'data_time', label: '注册时间', field: 'data_time' },
      ],
      rows: [
        {
          id: '000001',
          camera_name: 'user1',
          case_type: '用户',
          level: 4,
          data_time: '2021/07/27/12:01:29',
        },
        {
          id: '000002',
          camera_name: 'user2',
          case_type: '用户',
          level: 4,
          data_time: '2021/07/27/12:09:39',
        },
        {
          id: '000003',
          camera_name: 'admin1',
          case_type: 'admin',
          level: 0,
          data_time: '2021/07/27/12:31:29',
        },
        {
          id: '000001',
          camera_name: 'user1',
          case_type: '用户',
          level: 4,
          data_time: '2021/07/27/13:01:29',
        },
        {
          id: '000001',
          camera_name: 'user1',
          case_type: '用户',
          level: 4,
          data_time: '2021/07/27/13:01:29',
        },
        {
          id: '000001',
          camera_name: 'user1',
          case_type: '用户',
          level: 4,
          data_time: '2021/07/27/13:01:29',
        },
        {
          id: '000001',
          camera_name: 'user1',
          case_type: '用户',
          level: 4,
          data_time: '2021/07/27/13:01:29',
        },
        {
          id: '000001',
          camera_name: 'user1',
          case_type: '用户',
          level: 4,
          data_time: '2021/07/27/13:01:29',
        },
        {
          id: '000001',
          camera_name: 'user1',
          case_type: '用户',
          level: 4,
          data_time: '2021/07/27/13:01:29',
        },
        {
          id: '000001',
          camera_name: 'user1',
          case_type: '用户',
          level: 4,
          data_time: '2021/07/27/13:01:29',
        },
        {
          id: '000001',
          camera_name: 'user1',
          case_type: '用户',
          level: 4,
          data_time: '2021/07/27/13:01:29',
        },
        {
          id: '000001',
          camera_name: 'user1',
          case_type: '用户',
          level: 4,
          data_time: '2021/07/27/13:01:29',
        },
        {
          id: '000001',
          camera_name: 'user1',
          case_type: '用户',
          level: 4,
          data_time: '2021/07/27/13:01:29',
        },
        {
          id: '000001',
          camera_name: 'user1',
          case_type: '用户',
          level: 4,
          data_time: '2021/07/27/13:01:29',
        },
        {
          id: '000001',
          camera_name: 'user1',
          case_type: '用户',
          level: 4,
          data_time: '2021/07/27/13:01:29',
        },
        {
          id: '000001',
          camera_name: 'user1',
          case_type: '用户',
          level: 4,
          data_time: '2021/07/27/13:01:29',
        },
        {
          id: '000001',
          camera_name: 'user1',
          case_type: '用户',
          level: 4,
          data_time: '2021/07/27/13:01:29',
        },
        {
          id: '000001',
          camera_name: 'user1',
          case_type: '用户',
          level: 4,
          data_time: '2021/07/27/13:01:29',
        },
        {
          id: '000001',
          camera_name: 'user1',
          case_type: '用户',
          level: 4,
          data_time: '2021/07/27/13:01:29',
        },
        {
          id: '000001',
          camera_name: 'user1',
          case_type: '用户',
          level: 4,
          data_time: '2021/07/27/13:01:29',
        },
      ],

    }
  },
  methods:{
    go_analytics_detail(evt, row){
      this.$router.push('/admin_user_analytics/' + row.id)
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

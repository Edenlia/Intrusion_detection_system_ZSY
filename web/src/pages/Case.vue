<template>
  <q-page class="flex" style="background: #f0f2f5">
    <div class=" full-width column bg-white q-mx-md q-py-xs" style="height: 320px">
      <q-table
        class="my-sticky-header-table"
        title="未查看异常"
        :rows=rows
        :columns=columns
        row-key="id"
        flat
        bordered
        @row-click="go_case_detail"
      >
      </q-table>
    </div>
    <div class=" full-width column bg-white q-mx-md q-py-xs" style="height: 320px">
      <q-table
        class="my-sticky-header-table"
        title="已查看异常"
        :rows=rows
        :columns=columns
        row-key="id"
        flat
        bordered
        @row-click="go_case_detail"
      ></q-table>
    </div>
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
          label: '异常编号',
          align: 'left',
          field: row => row.id,
          sortable: true
        },
        { name: 'detected_camera', align: 'center', label: '检测到异常的摄像头', field: 'camera_name'},
        { name: 'case_type', label: '异常类型', field: 'case_type', sortable: true },
        { name: 'level', label: '异常等级', field: 'level' },
        { name: 'data_time', label: '发生时间', field: 'data_time' },
        { name: 'operation', label: '操作', field: 'operation' }
      ],
      rows: [
        {
          id: '1',
          camera_name: 'hhh',
          case_type: 3,
          level: 5,
          data_time: 'hhhhhh',
          operation: 87
        },
        {
          id: '2',
          camera_name: 'hhh',
          case_type: 3,
          level: 5,
          data_time: 'hhhhhh',
          operation: 87
        },
      ]
    }
  },
  methods:{
    go_case_detail(evt, row){
      this.$router.push('/case_detail/' + row.id)
    }
  }
}
</script>

<style lang="sass" scoped>
.my-sticky-header-table
  /* height or max-height is important */
  height: 310px

  .q-table__top,
  .q-table__bottom,
  thead tr:first-child th
    /* bg color is important for th; just specify one */
    background-color: #c1f4cd

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


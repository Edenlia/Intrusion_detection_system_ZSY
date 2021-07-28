<template>
  <q-page class="flex bg-black">
    <div class=" full-width column bg-black" style="height: 760px">
      <!--      style="height: 650px"-->
      <q-btn style="width: 100px;" class="bg-blue absolute-top-left" label="返回" @click="back"></q-btn>
      <div class="col row ">
        <div class="col-6 column">
          <div class="title1 col-1 justify-center">一个月内统计数据</div>
          <div class="col">
            <v-chart class="chart" :option="option1"></v-chart>
          </div>
        </div>
        <div class="col-6 column">
          <div class="title1 col-1 justify-center">一个月内统计数据</div>
          <div class="col">
            <v-chart class="chart" :option="option2"></v-chart>
            <!--            <img style="width: 577px; height: 268px" :src="img_exist(camera_urls[1])">-->
          </div>
        </div>
      </div>
      <div class="col row">
        <div class="col-6 column">
          <div class="title1 col-1 justify-center">一周内每天入侵出现次数</div>
          <div class="col">
            <!--            <img style="width: 577px; height: 268px" :src="img_exist(camera_urls[2])">-->
            <v-chart class="chart" :option="option3"></v-chart>

          </div>
        </div>
        <div class="col-6 column">
          <div class="title1 col-1 justify-center">一周内4个监控区域入侵出现次数数据</div>
          <div class="col">
            <!--            <img style="width: 577px; height: 268px" :src="img_exist(camera_urls[3])">-->
            <v-chart class="chart" :option="option4"></v-chart>

          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import {use} from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import {PieChart} from "echarts/charts";
import {BarChart} from "echarts/charts";
import {LineChart} from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  ToolboxComponent,
  LegendComponent,
  GridComponent,
} from "echarts/components";
import VChart, {THEME_KEY} from "vue-echarts";
import axios from "axios";
import {Notify} from "quasar";
use([
  CanvasRenderer,
  PieChart,
  BarChart,
  LineChart,
  TitleComponent,
  TooltipComponent,
  ToolboxComponent,
  LegendComponent,
  GridComponent,
]);
export default {
  name: "HelloWorld",
  props: ['id'],
  components: {
    VChart
  },
  provide: {
    [THEME_KEY]: "dark"
  },
  created(){
    this.get_admin_data()
  },
  data() {
    return {
      option1: {
        title: {
          text: "入侵者年龄段",
          left: "center"
        },
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
          orient: "vertical",
          left: "right",
          data: [
            "18岁以下",
            "18--45岁",
            "45--65岁",
            "65岁以上",
          ]
        },
        series: [
          {
            name: "入侵者年龄段",
            type: "pie",
            radius: "55%",
            center: ["50%", "60%"],
            data: [
              {value: 335, name: "18岁以下"},
              {value: 310, name: "18--45岁"},
              {value: 234, name: "45--65岁"},
              {value: 135, name: "65岁以上"},
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)"
              }
            }
          }
        ]
      },
      option2: {
        title: {
          text: "入侵者性别比例",
          left: "center"
        },
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
          orient: "vertical",
          left: "right",
          data: [
            "男",
            "女",
          ]
        },
        series: [
          {
            name: "性别比例",
            type: "pie",
            radius: "55%",
            center: ["50%", "60%"],
            data: [
              {value: 107, name: "男"},
              {value: 100, name: "女"},
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)"
              }
            }
          }
        ]
      },
      // 分割线
      option3 : {
        tooltip: {
          trigger: 'axis',
          axisPointer: {            // 坐标轴指示器，坐标轴触发有效
            type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: [
          {
            type: 'category',
            data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            axisTick: {
              alignWithLabel: true
            }
          }
        ],
        yAxis: [
          {
            type: 'value'
          }
        ],
        series: [
          {
            name: '统计数量',
            type: 'bar',
            barWidth: '60%',
            data: [17, 24,31, 18,22, 72, 67]
          }
        ]
      },
      option4: {
        title: {
          text: '堆叠区域图'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            label: {
              backgroundColor: '#6a7985'
            }
          }
        },
        legend: {
          data: ['未使用', '未使用', '未使用', '未使用']
        },
        toolbox: {
          feature: {
            saveAsImage: {}
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: [
          {
            type: 'category',
            boundaryGap: false,
            data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
          }
        ],
        yAxis: [
          {
            type: 'value'
          }
        ],
        series: [
          {
            name: '一号区域',
            type: 'line',
            stack: '总量',
            areaStyle: {},
            emphasis: {
              focus: 'series'
            },
            data: [0, 0, 0, 0, 0, 0, 0]
          },
          {
            name: '二号区域',
            type: 'line',
            stack: '总量',
            areaStyle: {},
            emphasis: {
              focus: 'series'
            },
            data: [0, 0, 0, 0, 0, 0, 0]
          },
          {
            name: '三号区域',
            type: 'line',
            stack: '总量',
            areaStyle: {},
            emphasis: {
              focus: 'series'
            },
            data: [0, 0, 0, 0, 0, 0, 0]
          },
          {
            name: '四号区域',
            type: 'line',
            stack: '总量',
            label: {
              show: true,
              position: 'top'
            },
            areaStyle: {},
            emphasis: {
              focus: 'series'
            },
            data: [0, 0, 0, 0, 0, 0, 0]
          },
        ]
      },
    };
  },
  methods:{
    back(){
      this.$router.go(-1)
    },
    get_admin_data(){
      let _this = this
      let user_id = this.id
      // console.log(user_id)
      console.log(this.id)
      axios.post(" http://172.30.68.249:8000/api/count/count_user/", {
        id : user_id
      }).then(function(response){
        console.log(response)
        let res = response.data
        console.log(res.case_month.e0_18)
        if(res.status === "Success"){
          _this.option1.series[0].data[0].value = res.case_month.e0_18
          _this.option1.series[0].data[1].value = res.case_month.e18_45
          _this.option1.series[0].data[2].value = res.case_month.e45_65
          _this.option1.series[0].data[3].value = res.case_month.e65_100
          _this.option2.series[0].data[0].value = res.case_month.male
          _this.option2.series[0].data[1].value = res.case_month.female
          _this.option3.series[0].data[0] = res.case.monday
          _this.option3.series[0].data[1] = res.case.tuesday
          _this.option3.series[0].data[2] = res.case.wednesday
          _this.option3.series[0].data[3] = res.case.thursday
          _this.option3.series[0].data[4] = res.case.friday
          _this.option3.series[0].data[5] = res.case.saturday
          _this.option3.series[0].data[6] = res.case.sunday
          let camera_list = res.case_list
          for(let i = 0; i < camera_list.length; i++){
            _this.option4.legend.data[i] = camera_list[i].camera_name
            _this.option4.series[i].name = camera_list[i].camera_name
            _this.option4.series[i].data[0] = camera_list[i].monday
            _this.option4.series[i].data[1] = camera_list[i].tuesday
            _this.option4.series[i].data[2] = camera_list[i].wednesday
            _this.option4.series[i].data[3] = camera_list[i].thursday
            _this.option4.series[i].data[4] = camera_list[i].friday
            _this.option4.series[i].data[5] = camera_list[i].saturday
            _this.option4.series[i].data[6] = camera_list[i].sunday

          }
          // console.log(res.register_list[0].monday)
          // _this.option4.series[0].data[0] = res.register_list[0].monday
          // console.log(1)
          // _this.option4.series[0].data[1] = res.register_list[0].tuesday
          // console.log(1)
          // _this.option4.series[0].data[2] = res.register_list[0].wednesday
          // console.log(1)
          // _this.option4.series[0].data[3] = res.register_list[0].thursday
          // console.log(1)
          // _this.option4.series[0].data[4] = res.register_list[0].friday
          // console.log(1)
          // _this.option4.series[0].data[5] = res.register_list[0].saturday
          // console.log(1)
          // _this.option4.series[0].data[6] = res.register_list[0].sunday
          // // console.log(1)
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

  },
};
</script>

<style scoped>
.chart {
  height: 320px;
  width: 600px;
}
.title1{
  font-size: 30px;
  color: #fff;
  background: #1976D2;
  display: flex;
  align-items: center;
}
</style>

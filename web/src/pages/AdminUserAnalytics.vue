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
          data: ['一号区域', '二号区域', '三号区域', '四号区域']
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
            data: [120, 132, 101, 134, 90, 230, 210]
          },
          {
            name: '二号区域',
            type: 'line',
            stack: '总量',
            areaStyle: {},
            emphasis: {
              focus: 'series'
            },
            data: [220, 182, 191, 234, 290, 330, 310]
          },
          {
            name: '三号区域',
            type: 'line',
            stack: '总量',
            areaStyle: {},
            emphasis: {
              focus: 'series'
            },
            data: [150, 232, 201, 154, 190, 330, 410]
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
            data: [320, 332, 301, 334, 390, 330, 320]
          },
        ]
      },
    };
  },
  methods:{
    back(){
      this.$router.go(-1)
    }
  }
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

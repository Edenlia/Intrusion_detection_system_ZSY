<template>
  <q-page class="flex bg-black">

    <div class=" full-width column bg-black " style="height: 720px">
      <div class="col-6 row ">
        <div class="col-6 column">
          <div class="title1 col-1 justify-center">近30天早中晚入侵者数量统计(所有用户)</div>
          <div class="col">
            <v-chart class="chart" :option="option1"></v-chart>
          </div>
        </div>
        <div class="col-6  column">
          <div class="title1 col-1 justify-center">近30天早中晚入侵车数量统计(所有用户)</div>
          <div class="col">
            <v-chart class="chart" :option="option2"></v-chart>
          </div>
        </div>
      </div>
      <div class="col-6 row ">
        <div class="col-6 column">
          <div class="title1 col-1 justify-center">近一周每天入侵数量统计(所有用户)</div>
          <div class="col">
            <v-chart class="chart" :option="option3"></v-chart>
          </div>
        </div>
        <div class="col-6 column">
          <div class="title1 col-1 justify-center">近一周每天新注册的用户数量</div>
          <div class="col">
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
          text: "早中晚入侵数据对比",
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
            "04:00-11:00",
            "11:00-18:00",
            "18:00-04:00",
          ]
        },
        series: [
          {
            name: "入侵者年龄段",
            type: "pie",
            radius: "55%",
            center: ["50%", "60%"],
            data: [
              {value: 335, name: "04:00-11:00"},
              {value: 310, name: "11:00-18:00"},
              {value: 234, name: "18:00-04:00"},
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
      option2 :{
        title: {
          text: "早中晚入侵数据对比",
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
            "04:00-11:00",
            "11:00-18:00",
            "18:00-04:00",
          ]
        },
        series: [
          {
            name: "入侵者年龄段",
            type: "pie",
            radius: "55%",
            center: ["50%", "60%"],
            data: [
              {value: 335, name: "04:00-11:00"},
              {value: 310, name: "11:00-18:00"},
              {value: 234, name: "18:00-04:00"},
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
            data: [806, 710, 640, 843, 800, 1139, 1201]
          }
        ]
      },

      option4:  {
        title: {
          text: '区域折线图'
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
          data: ['注册用户数量']
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
            name: '注册用户数量',
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
            data: [16, 11, 15, 27, 34, 28, 31]
          },
        ]
      },
    };
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

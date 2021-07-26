<template>
  <q-page class="flex" style="background: #f0f2f5">
    <div class=" full-width column bg-white q-ma-md" style="height: 650px">
      <div class="col-6 row q-py-md">
        <div class="col-6 q-px-md column">
          <v-chart class="chart" :option="option_pie_user"></v-chart>
        </div>
        <div class="col-6 q-px-md column">

        </div>
      </div>
      <div class="col-6 row q-py-md">
        <div class="col-6 q-px-md column">

        </div>
        <div class="col-6 q-px-md column">

        </div>
      </div>
    </div>
  </q-page>

</template>

<script>
import { ref } from 'vue' ;
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { PieChart, LineChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent
} from "echarts/components";
import VChart, { THEME_KEY } from "vue-echarts";

use([
  CanvasRenderer,
  PieChart,
  LineChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent
]);

export default {
  setup(){
    return{
      slide: ref('style')
    }
  },
  name: "HelloWorld",
  components: {
    VChart
  },
  provide: {
    [THEME_KEY]: "dark"
  },
  data() {
    return {
      option_pie_user: {
        title: {
          text: "Sources",
          left: "center"
        },
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
          orient: "vertical",
          left: "left",
          data: [
            "Direct",
            "Email",
            "Ad Networks",
            "Video Ads",
            "Search Engines"
          ]
        },
        series: [
          {
            name: "Traffic Sources",
            type: "pie",
            radius: "55%",
            center: ["50%", "60%"],
            data: [
              { value: 335, name: "Direct" },
              { value: 310, name: "Email" },
              { value: 234, name: "Ad Networks" },
              { value: 135, name: "Video Ads" },
              { value: 1548, name: "Search Engines" }
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
      option_pie_admin:{},
      option_bar_user:{},
      option_bar_admin:{}
    };
  }
};
</script>

<style scoped>
.chart {
  height: 400px;
  width: 600px;
}
</style>

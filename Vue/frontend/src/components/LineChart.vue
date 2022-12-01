<template>
  <LineChartGenerator
    :chart-options="chartOptions"
    :chart-data="chartData"
    :chart-id="chartId"
    :dataset-id-key="datasetIdKey"
    :width="width"
    :height="height"
  />
</template>
<script>
import { Line as LineChartGenerator } from "vue-chartjs/legacy";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  CategoryScale,
  PointElement,
} from "chart.js";
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  CategoryScale,
  PointElement
);
import { mapState } from "vuex";
export default {
  name: "LineChart",
  components: {
    LineChartGenerator,
  },
  data() {
    return {
      chartId: "line-chart",
      datasetIdKey: "label",
      width: 400,
      height: 400,
      // chartData: {
      //   labels: ["2022-06-01", "2022-07-01", "2022-08-01"],
      //   datasets: [
      //     {
      //       label: "금리",
      //       backgroundColor: "blue",
      //       data: [7.17983, 8.21018, 0.56848],
      //       tension: 0.3
      //     },
      //     {
      //       label: "코로나",
      //       backgroundColor: "red",
      //       data: [33.32972, 100, 10.34851],
      //       tension: 0.3
      //     },
      //     {
      //       label: "누리호",
      //       backgroundColor: "green",
      //       data: [40.73772, 1.89189, 0.13467],
      //       tension: 0.3
      //     },
      //   ],
      // },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
      },
    };
  },
  computed: {
    ...mapState(["chartData"]),
  }
};
</script>

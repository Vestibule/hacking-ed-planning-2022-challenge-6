<script setup lang="ts">
import * as echarts from 'echarts';
import axios from 'axios';
import { ref, onMounted, watch } from 'vue';

enum Charts {
  SCHOOL_ATTENDANCY_BY_YEAR = 'SCHOOL_ATTENDANCY_BY_YEAR',
  SCHOOL_ATTENDANCY_BY_COUNTRY = 'SCHOOL_ATTENDANCY_BY_COUNTRY',
}

const countries = [
  'Argentina',
  'Bolivia',
  'Brasil',
  'Chile',
  'Colombia',
  'Costa Rica',
  'Ecuador',
  'El Salvador',
  'Guatemala',
  'Honduras',
  'México',
  'Nicaragua',
  'Panamá',
  'Paraguay',
  'Perú',
  'República Dominicana',
  'Uruguay',
  'Venezuela',
];

let chart: any = null;
let schoolAttendancyByYearChart: any = null;

const year = ref('0');
const country = ref(null as string | null);
const schoolAttendance = ref([]);
const schoolAttendanceByYear = ref([]);
const chartToDisplay = ref(Charts.SCHOOL_ATTENDANCY_BY_COUNTRY as Charts);

const reloadDataset = async () => {
  const res = await axios.get('http://127.0.0.1:8000/by-gender', {
    params: {
      year: year.value,
    },
  });
  schoolAttendance.value = res.data;
};

const reloadAttendencyByYear = async () => {
  const res = await axios.get('http://127.0.0.1:8000/by-country', {
    params: {
      country: country.value,
    },
  });
  schoolAttendanceByYear.value = res.data;
};

watch(schoolAttendanceByYear, (newSchoolAttendance) => {
  const maleByCountry = newSchoolAttendance.filter(
    (row: any) => row.sex === 'M'
  );
  const femaleByCountry = newSchoolAttendance.filter(
    (row: any) => row.sex === 'F'
  );

  schoolAttendancyByYearChart.setOption({
    color: ['#91cc75', '#ee6666'],
    tooltip: {},
    xAxis: {
      // data: maleByCountry.map((row: any) => Date.parse(row.year)),
      // interval: 1000 * 60 * 60 * 24 * 365,
      type: 'time',
    },
    yAxis: {},
    series: [
      {
        name: 'Male',
        type: 'line',
        data: maleByCountry.map((row: any) => [
          Date.parse(row.year),
          row.value,
        ]),
        smooth: true,
      },
      {
        name: 'Female',
        type: 'line',
        data: femaleByCountry.map((row: any) => [
          Date.parse(row.year),
          row.value,
        ]),
        smooth: true,
      },
    ],
  });
});

watch(schoolAttendance, (newSchoolAttendance) => {
  const maleByCountry = newSchoolAttendance.filter(
    (row: any) => row.sex === 'M'
  );
  const femaleByCountry = newSchoolAttendance.filter(
    (row: any) => row.sex === 'F'
  );

  chart.setOption({
    color: ['#91cc75', '#ee6666'],
    tooltip: {},
    xAxis: {
      axisLabel: {
        interval: 0,
      },
      data: maleByCountry.map((row: any) => row.country),
      type: 'category',
    },
    yAxis: {},
    series: [
      {
        name: 'Male',
        type: 'bar',
        data: maleByCountry.map((row: any) => row.value),
      },
      {
        name: 'Female',
        type: 'bar',
        data: femaleByCountry.map((row: any) => row.value),
      },
    ],
  });
});

watch(year, () => {
  reloadDataset();
  chartToDisplay.value = Charts.SCHOOL_ATTENDANCY_BY_COUNTRY;
});

watch(country, () => {
  reloadAttendencyByYear();
  chartToDisplay.value = Charts.SCHOOL_ATTENDANCY_BY_YEAR;
});

onMounted(async () => {
  const res = await axios.get('http://127.0.0.1:8000/by-gender');
  const schoolAttendance = res.data;

  const maleByCountry = schoolAttendance.filter((row: any) => row.sex === 'M');
  const femaleByCountry = schoolAttendance.filter(
    (row: any) => row.sex === 'F'
  );

  schoolAttendancyByYearChart = echarts.init(
    document.getElementById('chartSchoolAttendancyByYear') as HTMLElement
  );

  chart = echarts.init(document.getElementById('chartElement') as HTMLElement);
  chart.setOption({
    color: ['#91cc75', '#ee6666'],
    tooltip: {},
    xAxis: {
      axisLabel: {
        interval: 0,
      },
      data: maleByCountry.map((row: any) => row.country),
      type: 'category',
    },
    yAxis: {},
    series: [
      {
        name: 'Male',
        type: 'bar',
        data: maleByCountry.map((row: any) => row.value),
      },
      {
        name: 'Female',
        type: 'bar',
        data: femaleByCountry.map((row: any) => row.value),
      },
    ],
  });
});
</script>

<template>
  <div class="flex">
    <div class="h-screen w-1/4 py-2 px-4 flex flex-col space-y-2 shadow">
      <div class="flex flex-col space-y-2">
        <h3 class="text-xl text-center">By year</h3>
        <button
          @click="year = '0'"
          class="w-24 h-8 border rounded"
          :class="
            year === '0' &&
            chartToDisplay === Charts.SCHOOL_ATTENDANCY_BY_COUNTRY
              ? 'bg-slate-200'
              : 'bg-slate-50'
          "
        >
          All
        </button>
        <button
          @click="year = '2015'"
          class="w-24 h-8 border rounded"
          :class="
            year === '2015' &&
            chartToDisplay === Charts.SCHOOL_ATTENDANCY_BY_COUNTRY
              ? 'bg-slate-200'
              : 'bg-slate-50'
          "
        >
          2015
        </button>
        <button
          @click="year = '2016'"
          class="w-24 h-8 border rounded"
          :class="
            year === '2016' &&
            chartToDisplay === Charts.SCHOOL_ATTENDANCY_BY_COUNTRY
              ? 'bg-slate-200'
              : 'bg-slate-50'
          "
        >
          2016
        </button>
        <button
          @click="year = '2017'"
          class="w-24 h-8 border rounded"
          :class="
            year === '2017' &&
            chartToDisplay === Charts.SCHOOL_ATTENDANCY_BY_COUNTRY
              ? 'bg-slate-200'
              : 'bg-slate-50'
          "
        >
          2017
        </button>
        <button
          @click="year = '2018'"
          class="w-24 h-8 border rounded"
          :class="
            year === '2018' &&
            chartToDisplay === Charts.SCHOOL_ATTENDANCY_BY_COUNTRY
              ? 'bg-slate-200'
              : 'bg-slate-50'
          "
        >
          2018
        </button>
      </div>
      <div class="flex flex-col space-y-2 overflow-scroll">
        <h3 class="text-xl text-center">By country</h3>
        <button
          v-for="iteratedCountry in countries"
          :key="iteratedCountry"
          @click="country = iteratedCountry"
          class="w-24 border rounded"
          :class="
            country === iteratedCountry &&
            chartToDisplay === Charts.SCHOOL_ATTENDANCY_BY_YEAR
              ? 'bg-slate-200'
              : 'bg-slate-50'
          "
        >
          {{ iteratedCountry }}
        </button>
      </div>
    </div>
    <canvas
      :class="
        chartToDisplay !== Charts.SCHOOL_ATTENDANCY_BY_COUNTRY ? 'hidden' : ''
      "
      id="chartElement"
      width="1400"
      height="600"
    ></canvas>
    <canvas
      :class="
        chartToDisplay !== Charts.SCHOOL_ATTENDANCY_BY_YEAR ? 'hidden' : ''
      "
      id="chartSchoolAttendancyByYear"
      width="1400"
      height="600"
    ></canvas>
  </div>
</template>
